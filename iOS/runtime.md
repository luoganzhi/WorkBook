# runtime

1. 什么是runtime? 
	- runtime就是系统提供给我们的一组C语言的函数,可以等到系统运行的时候动态的修改一些方法实现,添加属性.
	- oc的动态性就是又runtime函数来支持的.
2. runtime的主要用途? 
	- 给系统添加分类,获取系统没有暴露的方法,成员变量,然后通过kvc的方法直接修改成员变量的值.
	- hook系统的方法,自定义自己的某些方法,然后再调回系统方法,`method_exchangeImplementations`实现.
	- 字典转模型,批量获取模型的key,然后通过字典赋值.
3. runtime的主要api:
	1. 动态创建一个类(参数:父类，类名，额外的内存空间) `Class objc_allocateClassPair(Class superclass, const char *name, size_t extraBytes)`
	2. 注册一个类(要在类注册之前添加成员变量) `void objc_registerClassPair(Class cls)`
	3. 拷⻉实例变量列表(最后需要调用free释放) `Ivar *class_copyIvarList(Class cls, unsigned int *outCount)`
	4. 获得一个实例方法、类方法`Methodclass_getInstanceMethod(Classcls,SELname)  Method class_getClassMethod(Class cls, SEL name)`
	5. 交换方法实现 `void method_exchangeImplementations(Method m1, Method m2)`
