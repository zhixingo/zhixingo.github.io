import numpy as np
from functools import reduce

def slide_wins(a,winsize,steps=(1,1),flag=1):
    '''
    parameters:
        a: a panel(2D array) for window sliding, in fact it can be 3D, you can see it as a container of some 
                panels, the 0 axis length of a is the number of panels, i do the same operation on these 
                panels just like on the 2D array a.
        winsize: a tuple of the sliding window's height and width.
        steps: a tuple of the sliding strides in vertical and horizontal directions. Default: (1,1).
        flag: 0 or 1, please see return value [wins]. Default: 1.
    returns:
        wins: a 2D array contains all sub windows, each row represents a subwin. Note that the sliding 
                window moves from left to right and then from top to bottom by default value of flag
                , if you want to move from top to bottom firstly and then from left to right, set flag 
                to 0. If a is 3D, wins should be 3D too, each layer represents the subwins of the corresponding 
                layer in a.
        (rows,cols): the row index and column index indicates the left-top position coordinate of all sub windows.
    examples:
        slide_wins(np.arange(24).reshape(4,-1),(2,4),(2,2))
    '''
    if len(a.shape)==3:
        ah,aw=a[0].shape
    elif len(a.shape)==2:
        ah,aw=a.shape
    else:
        raise ValueError('a must be 2D or 3D.')
    if winsize[0]>ah or winsize[1]>aw:
        raise ValueError('winsize must be limited in %s.'%str((ah,aw)))
    
    rows=range(ah-winsize[0]+1)[::steps[0]] #rows代表了滑窗左上角在垂直方向上的刻度，len(rows)表示垂直方向滑窗数量
    cols=range(aw-winsize[1]+1)[::steps[1]] #cols代表了滑窗左上角在水平方向上的刻度，len(cols)表示水平方向滑窗数量
    x,y=np.meshgrid(rows,cols) #获取所有滑窗的左上角位置坐标
    
    t=np.stack((x,y))
    if flag==1:
        t=np.swapaxes(t,0,2)
    elif flag==0:
        t=np.transpose(t,(1,2,0))
    t=t.reshape(-1,2)
    t=np.ravel_multi_index(t.T,(ah,aw)) #该函数接受两个参数，第一个是元素坐标，第二个是数组形状，函数返回该位置在展平后的数组中的序号，可以同时计算多个位置坐标，譬如要计算(1,1)、(1,4)、(2,3)在数组A_5*5中的序号，则ravel_multi_index([[1,1,2],[1,4,3]],(5,5))
    
    q=(np.arange(winsize[1])[None,:]+np.array([aw*i for i in range(winsize[0])])[:,None]).flatten() #获取第一个滑窗所有元素在展平后数组中的序号
    
    index=t[:,None]+q[None,:]
    
    if len(a.shape)==3:
        wins=a.reshape(-1)[index+np.array([i*a.shape[1]*a.shape[2] for i in range(a.shape[0])])[:,None,None]]
    elif len(a.shape)==2:
        wins=a.flatten()[index] #每一行代表一个滑窗的内容，滑窗顺序是从左上角依次沿着向右以及向下顺序得到的，如果你想沿着先向下然后向右的顺序，只需要改变ravel_multi_index的第一个参数中坐标的顺序
    return wins,(rows,cols)
    
def conv(arr,kernel,steps=(1,1),ratio=1,integer=np.rint):
    '''arr是原始数组（形状意义参考slide_wins函数），kernel是卷积核（可以是2D可以是3D，如果是3D的，深度必须同arr的0轴长度，如果是2D的但是arr是三维的，kernel将被广播为三维，另外我没有对这些参数进行必要的检查，譬如kernel是三维的而arr是二维，这是不被允许的，请调用者自行确保），ratio是乘子系数，即卷积核实际上是kernel=ratio*kernel，默认的ratio值为1，这表示仅仅对窗口做了加权和（卷积核相当于一个权重矩阵），一般ratio取值为卷积核的大小的倒数（譬如卷积核尺寸是m*n，那么大小就是m*n，再如果卷积核是m*n*d，d是depth，那么大小就是m*n*d），如果取值None，那么ratio的值就是这么取的。integer参数表示对结果进行指定类型的取整操作，可以是以下数值：np.int、np.rint（四舍五入）、np.floor、np.ceil、np.trunc（截取整数部分），如果取值None，则原样输出（浮点数）'''
    dim=len(arr.shape)
    
    if dim==3 and len(kernel.shape)==2:
        kernel=np.broadcast_to(kernel,(arr.shape[0],*kernel.shape))
    if ratio==None:
        ratio=1/reduce(lambda x,y:x*y,kernel.shape)
    
    winsize=kernel.shape[-2:]
    wins,_=slide_wins(arr,winsize,steps)
    if dim==2:
        mul=wins*kernel.flatten()
        aver=np.sum(mul,axis=1)*ratio
    elif dim==3:
        kernel=kernel.reshape(kernel.shape[0],-1)[:,None,:]
        kernel=np.broadcast_to(kernel,(kernel.shape[0],wins.shape[1],kernel.shape[2]))
        mul=wins*kernel
        aver=np.sum(np.sum(mul,axis=2),axis=0)*ratio
    ret=aver.reshape(len(_[0]),len(_[1]))
    
    if integer!=None:
        if integer!=np.int:
            ret=integer(ret)
        ret=ret.astype(np.int)
    return ret
    
def media_filter(arr):
    '''中值滤波器，允许处理多通道图像，且返回仍是多通道的图像，说明见opencv/图像的噪声抑制.ipynb'''
    dim=len(arr.shape)
    wins,_=slide_wins(arr,(3,3),(1,1))
    if dim==2:
        t=np.sort(wins,axis=1)
        t=t[:,4]
        ret=t.reshape(len(_[0]),len(_[1]))
    elif dim==3:
        t=np.sort(wins,axis=2)
        t=t[:,:,4]
        ret=t.reshape(3,len(_[0]),len(_[1]))
    return ret
    
def knn_smooth(arr,size=3,k=5,integer=np.rint):
    '''KNN平滑滤波器，只处理单通道图像（灰度图），size参数表示滑窗的尺寸为size*size，其只能为奇数，譬如3（最小取值）、5、7，具体说明见opencv/图像的噪声抑制.ipynb'''
    if len(arr.shape)!=2 or size%2==0:
        return
    wins,_=slide_wins(arr,(size,size),(1,1))
    h,w=wins.shape
    t=int(w/2)
    q=np.arange(0,h*w,w)
    index=np.argsort(np.abs(wins-wins[:,t][:,None]),axis=1)[:,:k]+q[:,None]
    kdots=wins.reshape(-1)[index] #获取每个滑窗中在数值上与中心位置的待处理像素最接近的前k个点
    ret=np.sum(kdots,axis=1)/k
    ret=ret.reshape(len(_[0]),len(_[1]))
    
    if integer!=None:
        if integer!=np.int:
            ret=integer(ret)
        ret=ret.astype(np.int)
    return ret
    
def min_gray_var(arr,integer=np.rint,num=1,accelerate=True):
    '''最小灰度方差平滑滤波器，只允许处理单通道图像，具体说明见opencv/图像的噪声抑制.ipynb。accelerate参数是后添的，表示是否加速计算，加速版本见min_gray_var2，num参数控制平滑滤波的执行次数，有时候仅仅执行一次效果并不好，为了方便写代码，只有在accelerate为True时，num参数才起作用'''
    if accelerate:
        t=arr
        for i in range(num):
            t=min_gray_var2(t,integer)
        return t
        
    wins,_=slide_wins(arr,(5,5),(1,1))
    z=[[1,2,3,6,7,8,12],[5,6,10,11,12,15,16],[8,9,12,13,14,18,19],[12,16,17,18,21,22,23],[0,1,5,6,7,11,12],[3,4,7,8,9,12,13,14],[11,12,15,16,17,20,21],[12,13,17,18,19,23,24],[6,7,8,11,12,13,16,17,18]]
    vars=np.zeros((wins.shape[0],9))
    for i,e in enumerate(z):
        vars[:,i]=np.var(wins[:,e],axis=1)
    m=np.argmin(vars,axis=1)
    ret=np.zeros((wins.shape[0],))
    for i,win in enumerate(wins): #此处的for循环大大拉长了执行时间，其实这里还是可以使用矩阵优化的，见min_gray_var2
        ret[i]=np.mean(win[z[m[i]]])
    ret=ret.reshape(len(_[0]),len(_[1]))
    
    if integer!=None:
        if integer!=np.int:
            ret=integer(ret)
        ret=ret.astype(np.int)
    return ret
    
def sigma_filter(arr,size=5,integer=np.rint):
    '''Sigma平滑滤波器，只允许处理单通道图像，size参数表示滑窗尺寸为size*size，且size必须为奇数，同knn_smooth，具体说明见opencv/图像的噪声抑制.ipynb'''
    wins,_=slide_wins(arr,(size,size),(1,1))
    h,w=wins.shape
    t=int(w/2)
    p=wins[:,t]
    sigma=np.std(wins,axis=1)
    ret=np.zeros((h,))
    for i,win in enumerate(wins): #又是for循环，应该确实无法避免，但速度尼玛也太慢了
        ret[i]=np.mean(win[(win>=(p[i]-2*sigma[i]))&(win<=(p[i]+2*sigma[i]))])
    ret=ret.reshape(len(_[0]),len(_[1]))
    
    if integer!=None:
        if integer!=np.int:
            ret=integer(ret)
        ret=ret.astype(np.int)
    return ret
    
def min_gray_var2(arr,integer=np.rint):
    '''最小灰度方差平滑滤波器的优化版本'''
    wins,_=slide_wins(arr,(5,5),(1,1))
    z=[[1,2,3,6,7,8,12],[5,6,10,11,12,15,16],[8,9,12,13,14,18,19],[12,16,17,18,21,22,23],[0,1,5,6,7,11,12],[3,4,7,8,9,12,13],[11,12,15,16,17,20,21],[12,13,17,18,19,23,24],[6,7,8,11,12,13,16,17,18]]
    h,w=wins.shape
    vars=np.zeros((h,9))
    for i,e in enumerate(z):
        vars[:,i]=np.var(wins[:,e],axis=1)
    m=np.argmin(vars,axis=1)
    ret=np.zeros((h,))
    
    kt=np.where(m!=8)[0] #注意np.where的返回值是一个元组，要获取索引值序列，需要先解构
    if len(kt)>0:
        ktr=np.mean(wins[kt].reshape(-1)[np.array(z[:-1])[m[kt]]+np.arange(0,len(kt)*w,w)[:,None]],axis=1)
        ret[kt]=ktr
    
    k=np.where(m==8)[0]
    if len(k)>0:
        kr=np.mean(wins[k].reshape(-1)[np.array(z[-1])+np.arange(0,len(k)*w,w)[:,None]],axis=1)
        ret[k]=kr
    
    ret=ret.reshape(len(_[0]),len(_[1]))
    
    if integer!=None:
        if integer!=np.int:
            ret=integer(ret)
        ret=ret.astype(np.int)
    return ret
    
def gauss_kernel(winsize=(3,3),sigma=(0.8,0.8),flag=0,decimal=True,s=False):
    '''winsize代表垂直和水平两个方向上的尺寸，都必须是奇数，如果是单个数值，则另一个方向尺寸取值相同，flag、sigma参数的取值含义参见jupyter/cv/opencv/图像的噪声抑制和滤波器.ipynb，decimal参数表示结果是否显示为小数，因为numpy默认是科学计数法表示，需要注意的是，一旦修改，即使函数退出也将保持该设定，是全局改变的，参数s只有在flag=1时才有意义，原本返回kernel，现在相当于返回的是ratio,kernel/ratio'''
    if isinstance(winsize,int):
        winsize=(winsize,winsize)
    if isinstance(sigma,(int,float)):
        sigma=(sigma,sigma)
    if winsize[0]%2!=1 or winsize[1]%2!=1:
        raise ValueError('尺寸必须是奇数！')
    h,w=int(winsize[0]/2),int(winsize[1]/2)
    sh,sw=sigma
    x,y=np.meshgrid(range(-w,w+1),range(-h,h+1))
    t=1/(2*np.pi*sh*sw)*np.exp(-0.5*(x*x/(sh*sh)+y*y/(sw*sw)))
    np.set_printoptions(suppress=decimal)
    if flag==0: #小数形式
        return t/np.sum(t)
    elif flag==1: #整数形式
        k=1/t[-1][0]
        t=np.floor(t*k)
        if s:
            return t,np.sum(t)
        else:
            return t/np.sum(t)
    
def gauss_blur(img,winsize=3,sigma=0.8):
    '''对图像img进行高斯模糊处理'''
    gk=gauss_kernel(winsize,sigma)
    ret=None
    if len(img.shape)==2:
        ret=conv(img,gk)
    elif len(img.shape)==3:
        for i in range(3):
            t=conv(img[:,:,i],gk)[:,:,None]
            if i==0:
                ret=t
            else:
                ret=np.concatenate((ret,t),axis=2)
    return ret


# 2019/12/15-17
if __name__=='__main__':
    
    arr=np.array([[1,1,3,4,5],[2,1,4,5,5],[2,3,5,4,5],[3,2,3,3,2],[4,5,4,1,1]])
    
    #print(arr[None,:,:].shape)
    arr=np.concatenate([arr[:,:,None],arr[:,:,None],arr[:,:,None]],axis=2)
    #k=np.array([[1,1,1],[1,1,1],[1,1,1]])
    
    print(np.rollaxis(gauss_blur(arr,3,0.8),2))