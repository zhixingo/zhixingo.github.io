
# operator模块<sup>[1]</sup>
这个模块提供了我们日常所使用的全部运算符号的函数版本，它们常用在譬如`map`、`reduce`、`filter`中以替代某些用于迭代过程的简单`lambda`函式，这些函数只实现某些最简单的运算，如加法等数值运算、大于等比较运算，全部运算操作可参见文档，下面我们会给出一些示例，注意，一般我们不使用这个模块，这有可能使得你的代码变得晦涩难懂，除非作为读者的你也倾向此道，并曾了解过该模块，否则，己所不欲勿施于人


```python
import operator
from functools import reduce
```

你有一个序列$\{x_i\}$，你想计算$x_0-x_1-x_2-...-x_n$的值，你可能这样写：`reduce(lambda x,y:x-y,x)`，但是减法(x-y)只是最简单的运算，完全可以使用减号运算符`-`对应的函数版本(`operator.sub`)代替，即：`reduce(operator.sub,x)`，简单得多有木有（reduce(sub,x)比reduce(lambda x,y:x-y,x)少写了11个字符！）  
```python
operator.sub(a, b)
operator.__sub__(a, b) # 带有下划线的变体，次选
```
`sub(9,4)`，等同于`9-4`


```python
# example 1: x1-x2-x3-...-xn
x=[12,4,3,1] # 12-4-3-1=4
[reduce(lambda x,y:x-y,x),reduce(operator.sub,x)]
```




    [4, 4]



operator模块还定义了一些工具用于属性或项目的提取，它们同样用在某些场合以代替lambda函式的功能，譬如`map`、`sorted`、`itertools.groupby`  
<font color='blue'>attrgetter</font>  
```python
operator.attrgetter(attr) # 提取对象属性
operator.attrgetter(*attrs)
```
`f = attrgetter('name')`，调用`f(b)`，返回`b.name`.  
`f = attrgetter('name', 'date')`，调用`f(b)`，返回`(b.name, b.date)`.  
`f = attrgetter('name.first', 'name.last')`，调用`f(b)`，返回`(b.name.first, b.name.last)`.  
`attrgetter`相当于：  
```python
def attrgetter(*items):
    if any(not isinstance(item, str) for item in items):
        raise TypeError('attribute name must be a string')
    if len(items) == 1:
        attr = items[0]
        def g(obj):
            return resolve_attr(obj, attr)
    else:
        def g(obj):
            return tuple(resolve_attr(obj, attr) for attr in items)
    return g

def resolve_attr(obj, attr):
    for name in attr.split("."):
        obj = getattr(obj, name)
    return obj
```
<font color='blue'>itemgetter</font>  
```python
operator.itemgetter(item) # 提取项
operator.itemgetter(*items)
```
`f = itemgetter(2)`，调用`f(r)`，返回`r[2]`.  
`g = itemgetter(2, 5, 3)`，调用`g(r)`，返回`(r[2], r[5], r[3])`.  
`item`可以是任何为`__getitem__()`所接受的类型，除了一般的序列对象拥有此方法之外，字典也有，因而item可以是任何可哈希的值。列表、元组、字符串接受索引（整型数值）和切片（slice对象）：  
```python
>>> soldier = dict(rank='captain', name='dotterbart')
>>> itemgetter('rank')(soldier)
'captain'
>>> itemgetter(1)('ABCDEFG')
'B'
>>> itemgetter(1,3,5)('ABCDEFG')
('B', 'D', 'F')
>>> itemgetter(slice(2,None))('ABCDEFG')
'CDEFG'
```
使用`itemgetter`从元组类型记录中获取指定域数据：
```python
>>> inventory = [('apple', 3), ('banana', 2), ('pear', 5), ('orange', 1)]
>>> getcount = itemgetter(1)
>>> list(map(getcount, inventory))
[3, 2, 5, 1]
>>> sorted(inventory, key=getcount)
[('orange', 1), ('banana', 2), ('apple', 3), ('pear', 5)]
```
`itemgetter`相当于：  
```python
def itemgetter(*items):
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return obj[item]
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g
```
<font color='blue'>methodcaller</font>  
```python
operator.methodcaller(name[, args...]) # 提取对象方法
```
`f = methodcaller('name')`，调用`f(b)`，返回`b.name()`.  
`f = methodcaller('name', 'foo', bar=1)`，调用`f(b)`，返回`b.name('foo', bar=1)`.  
提供的`args`参数将被传递给方法，可以是位置参数，也可以是键值对形式  
`methodcaller`相当于：
```python
def methodcaller(name, *args, **kwargs):
    def caller(obj):
        return getattr(obj, name)(*args, **kwargs)
    return caller
```

参考：
[1] https://docs.python.org/3/library/operator.html operator文档
