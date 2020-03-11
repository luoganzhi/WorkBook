

# iOS锁问题
> https://juejin.im/post/5bf21d935188251d9e0c2937#heading-12


# 事件传递与响应

### 传递先给UIApplication -> UIWindow -> UIview->subViews倒序遍历

UIView的做法调用hitTest方法, hitTest会调用pointInside方法判断是否点击事件是否在内部, 然后如果返回是, 就继续倒序遍历
子控件, 继续调用hitTest方法,最后返回合适的view如果返回nil,就让当前view作为最适合响应的控件.

### 响应, 子控件-> 父控件-> 控制器->UIWindow -> UIApplication

子控件如果重写UITouchBegin并且不调用super 方法, 那么时间就不会往上响应, 即是父控件不会响应点击事件, 如果想让父控件响应,子控件也响应,只需要子控件处理完时间后,调用super方法即可.
处理事件写在super调用前后只影响具体执行时机,写在super后会等父控件事件处理完返回后,自己才会处理事件.
> ps:如果需要修改button的点击返回,只需要修改hitTest判断范围即可.


# 离屏幕渲染问题

1. cpu渲染不是真正的离屏渲染,应该叫`软件渲染`,而真正发生离屏渲染是在gpu部分.
    >> tip: 如果你的view实现了drawRect，此时打开Xcode调试的“Color offscreen rendered yellow”开关，你会发现这片区域不会被标记为黄色，说明Xcode并不认为这属于离屏渲染
    
2. cornerRadius加clickToBounds意思是设置圆角,加上裁切,所以需要离屏渲染,如果单纯设置coradius不会触发离屏渲染.
`self.layer.cornerRadius, self.layer.masksToBounds` 主要裁剪圆角的是Core Animation负责.

3. 触发离屏渲染的本质是: 如果不能一次性使用frame buffer画出最终的结果,那么就只能开辟内存存储中间结果,这其中就涉及到了上下文切换,所以开销大,产生卡
4.  可能触发离屏渲染的操作
    1. 设置圆角并裁剪
    2. 设置shadow属性
    3. group opacity设置
    4. Mask,遮罩设置
5.  优化方法
    1.  shouldRasterize设置yes, 会复用静态不变的layer, 但shouldResterize主旨是"降低性能损失，但总是至少会触发一次离屏渲染",所以如果你的layer不需要离屏渲染,但是你设置为true, 就会触发一次离屏渲染,影响性能.
    2. 用Core Graphics 进行绘图, 生成UIImage , 然后加到当前view上


