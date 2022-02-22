
# collections模块
collections是Python内建的一个集合模块，提供了许多有用的集合类（容器）


```python
from collections import namedtuple,deque,Counter,defaultdict,OrderedDict
```

## namedtuple类
`collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)`  
**命名元组**，返回可以使用字段名字而非下标索引（当然也是可以的）来访问元素内容的tuple子类，子类实例拥有包含`typename`和`field_names`字段值在内的文档字符串（执行`__doc__`方法），应用`__str__`或`__repr__`方法则可以获得`field_name=value`格式的全部字段数据，具有较好的可读性。举个例子，假设我们使用元组`(用户名,性别,年龄)`存储用户信息，譬如`man=tuple('戴阳','male',22)`，需要通过`man[0]`访问用户姓名、`man[1]`访问用户性别、`man[2]`访问用户年龄，在垒代码的时候，难免会感到困惑，`man[1]`是年龄还是性别来着？我们将tuple“升级”，使用其子类namedtuple来创建一个命名元组，从而避免该问题：
```python
namedtuple_man=namedtuple('man',['name','sex','age'])
man=namedtuple_man('戴阳','male',22)
```
于是可以通过`man.name`获得用户姓名、`man.sex`获得用户性别、`man.age`获得用户年龄  
要获得关于`namedtuple`的基本使用信息，可以使用`namedtuple.__doc__`  
`field_names`参数可以是字符串序列，譬如`['x','y']`，每个字符串代表一个字段，或者，`field_names`还可以是包含全部字段的单个字符串，各个字段之间以空格或逗号相隔，譬如`'x y'`或`'x,y'`  
任何有效的python标识符都可以作为字段名，除了以下划线开头的（防止与属性方法冲突）或者python的保留关键字，如`class`、`for`、`return`、`global`、`pass`或`raise`  
如果`rename`参数为True，非法的字段名将被自动转换为位置意义的名字，例如`['abc','def','ghi','abc']`被转换为`['abc', '_1', 'ghi', '_3']`，消除了非法的关键字`def`以及重复命名的`abc`  
`defaults`参数可以为None，或者缺省值的序列，由于拥有缺省值的参数总是排在没有缺省值的参数后面，即缺省值总是最先应用于最靠右的参数上，譬如我们的字段名分别为`['x','y','z']`，且缺省值为`(1,2)`，那么`x`仍需要为之传递值，因为`x`不具有缺省值，而`y`的缺省值为`1`，`z`的缺省值为2  
`module`指定所创建的命名元组所属模块  
`typename`并不很重要（除非你是要判断两个命名元组是否属于同一类，使用`isinstance`即可，对于上述示例，`type(man)`的结果是`__main__.man`），重要的是将创建的namedtuple子类赋给哪个变量，因为后者更多地应用在实际使用中，一般它们名字相同且富有意义，譬如：
```python
Point=namedtuple('Point', ['x', 'y'])
```
你看到了，命名元组方便地创建一个名为`Point`的类，并交付给变量`Point`，这很好地达成了一致，于是我们可以像使用一般类那样创建类实例，`p1=Point(1,2)`，就像这样（等同）：
```python
class Point():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
p1=Point(1,2)
```
可见它是多么方便，这实在令人感叹  
除了从元组继承的方法之外，命名元组还支持三个额外的方法和两个属性。为防止与字段名称冲突，方法和属性名称以下划线开头：  
`classmethod somenamedtuple._make(iterable)`  
从现有序列生成命名元组。继续上面的`Point`示例：
```python
t=[3,4]
p2=Point._make(t) #Point(x=3, y=4)
```
`somenamedtuple._asdict()`  
返回字段名到对应值的映射的新字典。
```python
p1._asdict() #OrderedDict([('x', 1), ('y', 2)])
```
注意：Changed in version 3.1: Returns an OrderedDict instead of a regular dict.  
`somenamedtuple._replace(**kwargs)`  
返回一个更些了某些字段后的新的命名元组实例。
```python
p1._replace(x=3) #Point(x=3, y=2)
```
`somenamedtuple._fields`：列出字段名称的字符串元组。用于内省和从现有命名元组创建新的命名元组类型
```python
p1._fields #('x', 'y')
Point3D=namedtuple('Point3D',Point._fields+('z',))
```
`somenamedtuple._field_defaults`：字段到缺省值的映射字典（已失效）
```python
Account=namedtuple('Account',['type','balance'],defaults=[0])
Account._field_defaults #{'balance': 0}
```
要获取某字段的值，使用`getattr()`方法：
```python
getattr(p1,'x') #3
```
要将一个字典转换成命名元组，使用`**`操作符（解包）：
```python
p3={'x': 5, 'y': 6}
Point(**p3) #Point(x=5, y=6)
```
由于命名元组是常规python类，因此可以进行子类化轻松添加或更改功能，下面我们为“点”这个类添加计算两点距离的方法：
```python
class Point(namedtuple('Point','x y')):
    __slots__=()
    def dist(self,point):
        return sqrt(pow(point.x-self.x,2)+pow(point.y-self.y,2))
p=Point(1,2)
p.dist(Point(4,6)) #5.0
```
注意：The subclass shown above sets `__slots__` to an empty tuple. This helps keep memory requirements low by preventing the creation of instance dictionaries.  
命名元组以及其字段的文档字符串是可定制的（可写的）：
```python
Point.__doc__+='坐标点'
Point.x.__doc__='点的x坐标分量'
Point.y.__doc__='点的y坐标分量'
```
注意：Changed in version 3.5: Property docstrings became writeable.


```python
Account = namedtuple('Account', 'owner balance transaction_count')
default_account = Account('<owner name>', 0.0, 0)
johns_account = default_account._replace(owner='John')
janes_account = default_account._replace(owner='Jane')
```

## deque类
`class collections.deque([iterable[, maxlen]])`  
**双端队列**（double-ended queue），返回一个从`iterable`初始化得到的一个deque对象（从左至右扫描`iterable`使用`deque.append`方法构建起deque），和原生list相比，最大的优点是实现了快速从队列头插入和取出元素的操作（线程安全），时间复杂度为O(1)，原生列表一般用作栈的数据结构，即在尾部（栈顶）插入（`append(elem)`）和取出（`pop()`），虽然它也支持在头部增（`insert(0,elem)`）取（'pop(0)'）元素，但是时间复杂度为O(n)  
如果未指定`maxlen`或为None，则deque可能会增长到任意长度。否则，请为双端队列限定最大长度。一旦有限长度的双端队列已满，当添加新项时，从另一端丢弃相应数量的项  
`append(x)`  
从deque的右端添加新元素  
`appendleft(x)`  
从deque的左端添加新元素  
`clear()`  
清空整个deque序列  
`copy()`  
创建deque的浅拷贝副本（New in version 3.5.）  
`count(x)`  
统计deque中元素值等于x的项个数（New in version 3.2.）  
`extend(iterable)`  
对iterable逐元素append至deque的右端
```python
d=deque([1,2,3])
d.extend([4,5,6]) #deque([1, 2, 3, 4, 5, 6])
```
`extendleft(iterable)`  
对iterable逐元素append至deque的左端
```python
d.extendleft([0,-1,-2]) #deque([-2, -1, 0, 1, 2, 3, 4, 5, 6])
```
`index(x[, start[, stop]])`  
返回元素x在deque中的位置索引（只返回第一个匹配成功的位置下标），`start`和`stop`都是可选参数，表示在deque的`[start,stop)`区间进行查找，如果找不到则抛出ValueError异常，当缺省时，`start=0`，`stop=maxlen-1`（New in version 3.5.）  
`insert(i, x)`  
将x插入到deque的i位置处，如果该插入导致溢出（长度超出maxlen），将抛出IndexError异常（New in version 3.5.）  
`pop()`  
从deque的右端移除一个元素并返回之，如果无元素，将抛出IndexError异常  
`popleft()`  
从deque的左端移除一个元素并返回之，如果无元素，将抛出IndexError异常  
`remove(value)`  
从左至右扫描deque，移除第一个和value匹配成功的元素，如果没有找到则抛出ValueError异常  
`reverse()`  
原址逆序该deque，返回None（New in version 3.2.）  
`rotate(n=1)`  
当`n`为负数时，将deque左起向右连续n个元素整个剪切追加到右端，看起来就是一个右旋操作；当`n`为正数时，将deque右起向左连续n个元素整个剪切粘贴到deque的左端，看起来就是一个左旋操作。当n=-1时，`d.rotate(-1)=d.append(d.popleft())`，当n=1时，`d.rotate(1)=d.appendleft(d.pop())`
```python
d.rotate(3) #deque([4, 5, 6, -2, -1, 0, 1, 2, 3])
d.rotate(-3) #deque([1, 2, 3, 4, 5, 6, -2, -1, 0])
```
deque提供了一个只读属性`maxlen`（Maximum size of a deque or None if unbounded. New in version 3.1.）  
除了上述操作，deque还支持iteration、pickling、len(d)、reversed(d)、copy.copy(d)、copy.deepcopy(d)、成员测试的`in`操作，以及索引操作如`d[-1]`，但是只有在头尾的索引时间复杂度才为`O[1]`，对于中间元素的索引则为`O(n)`，若要快速的随机索引，应使用列表    
有限长deque提供了同unix中的`tail`类似的尾部过滤操作：
```python
def tail(filename, n=10):
    'Return the last n lines of a file'
    with open(filename) as f:
        return deque(f, n)
```
使用（有限）deque的另一种方法是通过向右追加并弹出左侧来尽力维护一系列最近添加的元素  
可以使用存储在双端队列中的输入迭代器来实现循环调度。值从位置零处的当前活动迭代器中产生。如果当前活动迭代器已经耗尽，则使用`popleft`删除它；否则，使用`rotate`方法将位于deque最后的迭代器调度到deque的首部（位于首部的迭代器为当前活动迭代器）：
```python
def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    iterators = deque(map(iter, iterables))
    while iterators:
        try:
            while True:
                yield next(iterators[0])
                iterators.rotate(-1)
        except StopIteration:
            # Remove an exhausted iterator.
            iterators.popleft()
```


```python
d=deque([1,2,3])
d.extend([4,5,6])
d.extendleft([0,-1,-2])
print(d)
d.append(d.popleft())
d
```

> 输出：<br>deque([-2, -1, 0, 1, 2, 3, 4, 5, 6])<br>deque([-1, 0, 1, 2, 3, 4, 5, 6, -2])

## Counter类
`class collections.Counter([iterable-or-mapping])`  
Counter类的目的是用来跟踪元素出现的次数，通俗称为“**计数器**”，返回一个无序的容器类型，以字典的形式存储（是字典的子类），其中元素作为`key`，其计数作为`value`。计数值可以是任意的Interger（包括0和负数）。Counter类和其他语言的<a href='https://www.gnu.org/software/smalltalk/manual-base/html_node/Bag.html'>bags</a>或<a href='https://en.wikipedia.org/wiki/Multiset'>multisets</a>很相似  
创建Counter实例（我们仍能更新它）：  
```python
c1=Counter() #创建一个空的Counter类实例
c2=Counter('muggledy') #从一个iterable对象（list、tuple、dict、字符串等）创建
c3=Counter({'a': 4, 'b': 2}) #从一个字典对象创建
c4=Counter(a=4, b=2) #从一组键值对创建
```
计数访问，须知，当所访问的键不存在时，返回0而非KeyError：
```python
c = Counter(['eggs', 'ham'])
c['bacon'] #0, count of a missing element is zero
```
将计数器中的某个键值设为0并不能将其从计数器中移除，若要达到这一点，应使用`del`：
```python
c['ham'] = 0                        # counter entry with a zero count
del c['ham']                        # del actually removes the entry
```
除了支持字典上的所有方法，Counter类还支持其它三种方法：  
`elements()`  
根据计数器返回一个迭代器，重复元素次数直至其计数值，对于计数小于1的元素则忽略，且不同元素出现的顺序是任意的：
```python
c = Counter(a=4, b=2, c=0, d=-2)
sorted(c.elements()) #['a', 'a', 'a', 'a', 'b', 'b']
```
`most_common([n])`  
返回n个最常见元素及其计数的列表，从最常见到最少。如果n缺省或为None，则`most_common`返回计数器中的所有元素。具有相同计数的元素是任意排序的：
```python
Counter('abracadabra').most_common(3) #[('a', 5), ('r', 2), ('b', 2)]
```
`subtract([iterable-or-mapping])`  
从迭代或从另一个映射（或计数器）中减去元素计数值。与`dict.update`类似，但是减去计数而不是更新（其实是加法）它们。输入和输出都可以是零或负数：
```python
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
c.subtract(d) #Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})
```
字典方法适用于计数器Counter除了两个例外，分别是`update`和`fromkeys`：  
`update([iterable-or-mapping])`  
从可迭代对象或从另一个映射（或计数器）中加上元素计数值。像`dict.update()`一样，但是增加计数而不是替换它们。此外，期望的可迭代对象是元素序列，而不是`(键,值)`对的序列  
`fromkeys(iterable)`  
Counter对象尚未实现此方法  
计数器常见操作：
```python
sum(c.values())                 # total of all counts
c.clear()                       # reset all counts --> Counter()
list(c)                         # list unique elements（将c中的键以列表返回）
set(c)                          # convert to a set
dict(c)                         # convert to a regular dictionary
c.items()                       # convert to a list of (elem, cnt) pairs
Counter(dict(list_of_pairs))    # convert from a list of (elem, cnt) pairs
c.most_common()[:-n-1:-1]       # n least common elements
+c                              # remove zero and negative counts
```
几个数学运算，包括加法、减法以及交并集运算，结果将排除小于1的计数值：
```python
c = Counter(a=3, b=1)
d = Counter(a=1, b=2)
c + d                       #Counter({'a': 4, 'b': 3}), add two counters together:  c[x] + d[x]
c - d                       #Counter({'a': 2}), subtract (keeping only positive counts)
c & d                       #Counter({'a': 1, 'b': 1}), intersection:  min(c[x], d[x]) # doctest: +SKIP
c | d                       #Counter({'a': 3, 'b': 2}), union:  max(c[x], d[x])
```
两个快捷的一元操作：
```python
c = Counter(a=2, b=-4, c=0)
+c #Counter({'a': 2})，c += Counter()可以达到一样的效果，但麻烦一点
-c #Counter({'b': 4})
```


```python
c3=Counter({'a': 4, 'b': 2})
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
c.update(d)
c
```

> 输出：<br>Counter({'a': 5, 'b': 4, 'c': 3, 'd': 2})


```python
c = Counter(a=2, b=-4, c=0)
print(+c)
-c
list(c)
```

> 输出：<br>Counter({'a': 2})<br>['a', 'b', 'c']

## defaultdict类
`class collections.defaultdict([default_factory[, ...]])`  
返回一个新的类字典对象（针对任意查询键都可以返回有效值/默认值），defaultdict是内置dict类的子类。其提供了与原生dict几乎一致的操作方法，除了下述方法以及一个实例属性（default_factory）：  
`__missing__(key)`  
该方法的语义为：对于待查找的关键字key，若不存在于字典中，表示“缺失键”，于是调用此方法（在`__getitem__`中发生此调用，需要注意的是，只有`__getitem__`会调用`__missing__`方法，这意味着，如果你使用`get`获取值，将返回None而非调用`default_factory`）。如果`default_factory`为None，将导致`KeyError`异常，异常的参数即为此`key`；如果`default_factory`不为None，将以无参形式直接调用它（`default_factory`必须是可调用对象），调用结果将作为`__missing__`的返回值，作为当前缺失键的默认值返回  
`default_factory`属性为`__missing__()`所使用，它由defaultdict实例构造器（构造函数）的第一个参数决定，如果没有传递该参数则为None  
defaultdict构造函数除第一个参数以外的剩余参数全部传递给dict的构造函数，用作构造字典的内容  
举个例子，如果你希望缺失键一律返回默认值-1，那么你可以这么做：
```python
d=defaultdict(lambda:-1,a=1,b=2,c=3) #类字典形如：{'a':1,'b':2,'c':3}
d['d'] #-1, default_factory是一个匿名函数，假设记作f，即default_factory=f，其中f=lambda:-1，在键'd'缺失的情况下，直接调用f()，并返回，于是得到-1
```
需要注意的是，在第一次查询无果的情况下，会使用`default_factory`作为返回值，但是不要以为这就完事儿了，附加操作是，defaultdict会自动将该键值对保存下来，也就是说，下一次仍查找该关键字的时候，将查询有果（上面的示例中，我们访问`d['d']`后，打印字典`d`，你会发现其中已经有了`'d':-1`的键值对）：
```python
members = [
    ['male', 'John'],
    ['male', 'Jack'],
    ['female', 'Lily'],
    ['male', 'Pony'],
    ['female', 'Lucy'],
] #这里有两类数据，标签分别为"male"（男）和"female"（女），试着将其归类
people = defaultdict(list)
for sex, name in members:
    people[sex].append(name)
people #defaultdict(list, {'female': ['Lily', 'Lucy'], 'male': ['John', 'Jack', 'Pony']})
```
该操作效果等同于使用`d.setdefault`：
```python
people={}
for k, v in members:
    people.setdefault(k, []).append(v)
people #{'female': ['Lily', 'Lucy'], 'male': ['John', 'Jack', 'Pony']}
```
实现Counter计数器的新方法，将`default_factory`设置为`int`即可（一般人的想法是使用lambda返回一个常数值0），可能有一点你不知道：你知道int()+3等于多少吗（等于3）？实际上`int()=0`（这是常量函数的一个特例），于是：
```python
s = 'mississippi'
d = defaultdict(int)
for k in s:
    d[k] += 1
sorted(d.items()) #[('i', 4), ('m', 1), ('p', 2), ('s', 4)]
```


## OrderedDict类
`class collections.OrderedDict([items])`  
**有序字典**，返回一个字典的子类实例对象，该子类具有专门用于重新排列字典顺序的方法  
`popitem(last=True)`  
该方法从有序字典中移除一个键值对并作为返回值返回，当`last`为True时，将按照后进先出（LIFO）的顺序移除，否则按照先进先出（FIFO），当对一个空字典执行该操作时，将导致KeyError异常  
`move_to_end(key, last=True)`  
当`last`为True时，将有序字典中的某一键值对移动到最后一项，否则移动为第一项
```python
d = OrderedDict.fromkeys('abcde') #所有键对应的值为None
d.move_to_end('b')
''.join(d.keys()) #'acdeb'
d.move_to_end('b', last=False)
''.join(d.keys()) #'bacde'
```
除了常见的字典操作，有序字典还支持逆序迭代操作`reversed()`  
两个有序字典之间的等式测试是顺序敏感的，而有序字典与其它非有序字典之间是不敏感的，譬如：
```python
d1=OrderedDict.fromkeys('abc')
d2=OrderedDict.fromkeys('cba')
d3=dict.fromkeys('bca')
d1==d2 #False
d1==d3 #True
```
如果你有两个有序字典，要比较相等，但是你又不希望顺序敏感，你可以用`dict`工厂函数做一下返厂操作，以得到一个普通字典：
```python
dict(d1)==d3 #True
```
有序字典对实现`functools.lru_cache`（关于LRU可以参见python/高级/文档/记忆装置.md）很有用：
```python
class LRU(OrderedDict):
    'Limit size, evicting the least recently looked-up key when full'

    def __init__(self, maxsize=128, *args, **kwds):
        self.maxsize = maxsize
        super().__init__(*args, **kwds)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]
```

2019/4/8

[1] https://docs.python.org/3/library/collections.html 官方文档  
[2] https://www.jb51.net/article/85542.htm Counter类及实例  
[3] https://www.cnblogs.com/zhizhan/p/5692668.html collections模块常用类
