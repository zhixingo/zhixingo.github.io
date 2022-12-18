### 决策树绘制
treeinfo={
    'tearRate':{
        'reduced':'no lenses',
        'normal':{
            'astigmatic':{
                'yes':{
                    'prescript':{
                        'hyper':{
                            'age':{
                                'pre':'no lenses',
                                'presbyopic':'no lenses',
                                'young':'hard'
                            }
                        },
                        'myope':'hard'
                    }
                },
                'no':{
                    'age':{
                        'pre':'soft',
                        'presbyopic':{
                            'prescript':{
                                'hyper':'soft',
                                'myope':'no lenses'
                            }
                        },
                        'young':'soft'
                    }
                }
            }
        }
    }
}
#treeinfo={'家族':{'家庭1':'戴阳','家庭2':{'戴晓东':{'家庭2-1':'xxx'}}}} # test

# 打印版本
def detree(tree,prefix=''):
    treename=list(tree.keys())[0]
    branches=list(tree[treename].keys())
    if prefix!='':
        t='|'.join(prefix.split('|')[:-1])+'|'
        print(t+'    → [NODE]',treename+':') # 子树根
    else:
        print(prefix+'[NODE]',treename+':') # 子树根
        prefix='  '
    for i,branch in enumerate(branches):
        if i>0:
            print(prefix+'|')
        print(prefix+'|-[BRANCH]',branch)
        if isinstance(tree[treename][branch],dict): # 子树，递归
            detree(tree[treename][branch],prefix+'|         ')
            pass
        else: # 叶子节点
            print(prefix+'|    → [LEAF]',tree[treename][branch])
    
detree(treeinfo)

# 决策树的每个节点（NODE）可能是叶子节点（LEAF）也可能是某个子树的根节点，每个节点下可能有诸多的分支（BRANCH），但是每个分支只能指向一个节点，这是显而易见的，图中每个分支下的符号'→'表示的就是“指向”含义，如果你的“树”报错，那一定是你的树不满足该结构：父节点和子节点之间有一个分支的指向