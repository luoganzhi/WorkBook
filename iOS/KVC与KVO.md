# KVO
### key value observing
- 用于监听某个对象属性值改变
- 对一个对象使用observing, 会在runime时候,动态生成一个NSKVONotifying_class 类文件, 继承于源文件, 里面主要重写了四个方法,重写监听属性set方法, 重写class 方法, dealloc, _isKVOA
- 对象调用方法的时候,先通过isa指针找到新生成的类, 找到对象方法, 对象方法内部伪代码如下
    ```
    [self willChangeValueForkey:@"key"]
    // 原来要实现的set方法
    [self didChangeValueForKey:@"key"]
    
    // didChangeValueForKey 内部会调用 observer的 observerValueForKey方法,通知属性发生改变
    
> 重点是runtime时动态生成了一个文件,成为对象的类文件

# KVC
### key value coding

<img src=" https://github.com/luoganzhi/WorkBook/blob/master/iOS/image/kvc.png" width="300" align=center>
 
 ### 本质
 默认的点语法,其实调用的是`setValueForKey` 方法,消息传递机制,默认会按照如图所示传递消息,先查询`setKey`方法,然后`_setKey`方法,在看`accessInstanceVariablesDirectly`返回值,默认为yes,如果为yes代表能够直接访问成员变量,就按照_key,_isKey,key,isKey顺序查找,最后都没找到,就报错.
 
 > 如何手动触发KVO?
 >> 手动调用willChangeValueForKey和didChangeValueForKey
 
 直接修改成员变量不会触发kvo,因为没有通过消息传递机制,如`object->age = 30`不会触发.
 
 

