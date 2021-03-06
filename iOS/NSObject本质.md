# NSObject本质

### 一个NSObject实例变量实质占用内存大小
```
NSObject impl {
    Class isa // class指针占用8byte
}
```
但NSObject结构体生成的时候,由于结构体分配内存需要内存对齐,源码中也写了,如果小于16,那么就默认分配16个字节

> ios系统还有自己的对齐方式,如果是申请较小的内存,那么默认分配的内存会以[16,32,48....256]分配,不超过256byte
>>结构体默认对齐方式,为最大成员变量的倍数量

### 查询内存分配大小方法
1. malloc_size 查询系统会对象分配了多少内存
2. size_of 只是查询对象大小,并且size_of是`运算符号`,在编译的时候就会确定.
3. getinstance_size也是返回对象大小,不是返回系统分配了多少内存.


### 对象, 类对象, 元类对象
1. instance:只存放属性,isa指针
2. Class : 存放对象方法,isa指针,superclass指针,协议等等**不存放类方法**
3. meta Class: 主要存放的有类方法,isa指针,superclass指针


##### 小知识
> 大小端对齐. 大端：把数据低位放到地址高位；小端：把数据低位放到地址低位。
> 从而小端存储比较符合人的一般逻辑。 ios 默认小段对齐
>
> 字节表示: 0xff = 256 = 2^8 = 1byte 
