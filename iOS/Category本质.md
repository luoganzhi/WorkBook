# Category

1. 使用category可以将大文件拆分为小文件
2. 可以给系统类添加Category,扩展方法等

### 系统对Category的加载处理过程
1. 系统在runtiem的时候加载一个类的所有Category数据
2. 把所有参与编译的Category的方法,属性,协议数据,合并到一个大数组中, 后面参与编译的会插入到素组的头部
3. 将合并后的分类数据, 插入到类原来的数据前面

> 所以分类方法会覆盖原来方法!!!


### load方法与initialize
##### +load方法:
1. 会在runtime加载类,分类的时候调用,每个类分类只调用一次.

2. 调用顺序:
    先调用类的load方法`所有类的load方法调用完`,再调用分类的load方法`所有的类调用完后再调用分类的load`,然后按照编译顺序调用, 因为不是消息发送机制,所以load方法是直接通过函数地址调用.

##### +initialize方法:
1. 会在类第一次接收到消息时候调用,每个类只初始化一次.

2. 调用顺序:
    如果父类没有初始化过,调用子类的时候会先调用父类的initialize方法,然后才调用子类的initialize方法,如果子类没实现方法,就调用父类的方法初始化自己.
> 由于是消息传递机制,如果分类实现了initialize,那么会调用分类的initialize实例化自己,另外一定是先完成父类的初始化,才会初始化子类


### 分类能否添加成员变量
1. 分类不能添加成员变量,因为没有ivars数组,但是可以添加属性,但是属性只自动生成get与set方法申明,
2. 可以用runtime方法, obj_setAssociatedObject方法设置关联对象,关联对象主要使用一个全局管理类,A sscoiationsManger.

<img src="https://github.com/luoganzhi/WorkBook/blob/master/iOS/image/releatedObject.png" width="600" alt="img" align=center>
