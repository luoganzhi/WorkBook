# Block探究

### block的本质问题
1. block其实是一个oc对象,因为其结构体第一个成员为class类型的isa指针.
```
struct main_block_impl_0 {
    struct block_impl {
        Void *isa; 
        Void *FuncPtr; // 指向block内部保存的函数调用地址
    }
    
    ivars// block内部包含的属性
         // int 为直接捕获值, 对象为指针引用
}

```

### block的类型
1. Global_block 全局block, 内部没有auto 变量,
2. stack_block 栈block, 内部含有auto变量
3. malloc_block 堆block, 内部有auto变量,并且被copy到堆上的block

### block 对变量的捕获方式:
1. 如果是auto局部变量, 那么就会捕获, 如果是基本数据,就值传递,如果是对象,就指针;
2. 如果是static局部变量, 也会捕获,捕获方式是指针传递
3. 其他全局变量都是不捕获,为直接访问

### block引用内存管理问题
- 在arc下, 用强指针指向block, 系统会自动对block进行一次copy操作,然后block内部属性,会因为修饰符号而被block强引用或者弱引用,调用block的copy方法,释放时候调用dispose函数
- 在mrc下,强指针不会对block对象进行copy操作,所以如果block是stack类型block,那么block对内部对象都不会产生强引用.

### 关于__block修饰属性问题
- __block会将修饰属性包装成一个对象,内部有__forwarding指针,指向自己,在copy的时候,栈上的_forwarding指向堆上,并且内部有保存修饰的属性,所以当你在函数内部访问局部变量的时候,会通过forwarding指针找到堆上的变量,访问block修改过后的值,而不是原本栈上的值.
> 为什么不能修改局部非静态变量? 因为2个空间不同,堆上的对象不能修改栈上的指针,因为栈上的对象生命周期不可控,同时block的作用域与局部变量的作用域不同,所以不能直接修改.
<img src="https://github.com/luoganzhi/WorkBook/blob/master/iOS/image/forwarding.png" width=600 alt="forwarding" align=center />
    


- 当block在栈上时, __block并不会对所修饰的属性产生强引用,但是当被copy到堆上时,会调用block_object_assgin,根据修饰的属性是strong还是weak产生对应的引用,移除的时候调用block_object_dispos函数释放对象,
- 在mrc下__block能消除循环引用,因为__block修饰的属性并不会retain使引用计数加1,所以`self -> block -> __block` 所以不会产生循环引用;
- __block在arc下产生的循环引用最少为3个对象,因为__block会变为对象

### 关于__weak, __unsafe_unretained区别
- 都是为了解决循环引用问题,但是weak是安全的,因为引用对象被销毁后,会将指针变为nil,而__unsafe_unretained不会,所以会产生野指针
