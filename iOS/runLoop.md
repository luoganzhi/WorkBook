




```
_thread = [[MyThread alloc] initWithBlock:^{
    [[NSRunLoop currentRunLoop] addPort:[[NSPort alloc] init] forMode:NSDefaultRunLoopMode];
    [[NSRunLoop currentRunLoop] run];
}];
// 如果不启动runloop,那么线程不会死亡,但是已经退出了,不会再响应教给线程的事件.
```
