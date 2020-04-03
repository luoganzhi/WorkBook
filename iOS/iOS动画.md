# CALayer探究

### CAShapeLayer :形状Layer
1. 使用了硬件加速,渲染速度快.
2. 不用像CALayer一样创建寄宿图层,节约内存.
3. 不会被图层边界裁切,想画多远,多大都行,形状由Path决定,而且是矢量绘制,所以不用考虑分辨率.
4. 做3D变换时,不会出现像素化.

- 主要用到mask相关,分别修改显示的圆角:
	```
		CAShapeLayer *layer = [CAShapeLayer layer];
    		layer.frame = _redView.bounds; // 图层大小等于需要添加遮罩的大小
    		UIRectCorner cor = UIRectCornerTopLeft | UIRectCornerTopRight; // 圆角位置
    		CGRect rect = _redView.bounds; // path作用路径
    		CGSize radii = CGSizeMake(50, 50); // 圆角半径
    		UIBezierPath *path = [UIBezierPath bezierPathWithRoundedRect:rect byRoundingCorners:cor cornerRadii:radii];
    		layer.path = path.CGPath;
    		_redView.layer.mask = layer;

	```

### CATextLayer :文本图层
1. 比UILabel渲染速度快很多.
2. 拥有几乎所有的UILabel属性.

- 属性:
	1. foregroundColor 文字颜色
	2. alignmentMode:对齐方式 `kCAAlignmentJustified`属于CoreAnimation固定值.
	3. font:
	```
	CFStringRef fontName = (__bridge CFStringRef)font.fontName; 
	CGFontRef fontRef = CGFontCreateWithFontName(fontName); 
	textLayer.font = fontRef;
	textLayer.fontSize = font.pointSize; 
	CGFontRelease(fontRef);
	```
	4. textLayer.contentsScale = [UIScreen mainScreen].scale; 防止出现像素化
	5. textLayer.wrapped = YES; 是否根据layer面积自动换行,默认不换行.

### CATransformLayer: 3D图层
1. 专门用于3D的图层.
2. CATransformLayer 并不扁平面化它的子图层.
3. 它不能显示它自己的内容,只有子图层变化才有用.
- 使用:
	```
	CATransform3D pt = CATransform3DIdentity;
	pt.m34 = -1.0 / 500.0; 
	self.containerView.layer.sublayerTransform = pt; // 让宿主图层从正投影变为透视投影
	

	CATransform3D c1t = CATransform3DIdentity;
	c1t = CATransform3DTranslate(c1t, -100, 0, 0); // CATransformLayer向左移动100的矩阵.
	CALayer *cube1 = [self cubeWithTransform:c1t];  // 放射变换
	[self.containerView.layer addSublayer:cube1]; // 将CATransformLayer添加到宿主图层.

	```

### CAGradientLayer: 渐变图层
1. 用来生成两种或者更多颜色的平滑渐变.
2. 使用了硬件加速.
- 属性:
	1. colors 存放变换颜色, 需要c类型,但是是oc的array,所以需要桥接`(__bridge id)`
	2. startPoint:开始渐变点, endPoint:结束渐变点. 取值范围为0->1.
	3. locations, 渐变位置, 从0->1, location数组个数需要和colors对应,如果少于,就按location渐变个数来,如果多余,就按colors个数来.

### CAReplicatorLayer: 复用图层
1. 对添加到复用图层上的图层,根据`instanceCount`来重复使用多少次.
2. 给所有实例图层添加仿射变换`instanceTransform`,每个图层变换相对于上一个图层位置变化.
3. CATransform3DScale(x,y,z) 如果是传入负数,例如需要变换的原来的点是(100,200),如果3DScale(1,-1,0),那么变换结果是(100,-200),相当于沿着X轴翻转.

### CAScrollLayer: 滚动图层
1. 它自动适应bounds的原点以便图层内容出现在滑动的地方.
2. UIScrollView就是简单的通过直接操作图层边界来实现滑动.

### CATiledLayer: 平铺图层
1. 解决大的图片载入问题,如果使用`imageName:`会阻塞线程,涉及到图片解压缩.
2. 将大图分解成小图,单独按需载入.
3. 核心代码: 根据scrollView滚动到不同位置加载不同位置的image,然后将屏幕之外的图片销毁,达到节约内存.
	```
	 	UIGraphicsPushContext(ctx);
    		[tileImage drawInRect:bounds];
    		UIGraphicsPopContext();
	```

### CAEmitterLayer: 粒子效果图层
1. 可以实现如微信红包雨.
2. 里面有许多CAEmitterCell容器.每个cell是一个图片.
3. 主要属性:
	1. birthRate: 粒子生成速度
	2. lifetime: 粒子的生命周期系数,多少秒销毁
	3. emitterPosition: 粒子发射的中心点.
	4. emitterSize: 发射源的尺寸大小
	5. emitterShape: 发射源的形状,枚举类型.
	6. emitterMode: 发射模式,枚举类型.
	7. renderMode: 渲染模式,枚举类型.
	8. velocity: 粒子速度, 默认1.0.
	9. scale: 粒子的缩放比例系数, 默认1.0
	10. spin: 粒子的自旋转速度系数, 默认1.0
4. CAEmitterCell.contents 注意接收CGImageRef类型,不要赋值UIImage.

### CAEAGLLayer: OpenGL图层,CoreAnimationEmbedAppleGLLayer.
1. 使用GLKit,简化OpenGL开发.
2. 使用OpenGL相关问题,后续继续学习探究.

### AVPlayerLayer: 视频图层
1. 属于AVFoundation.
2. MPMoivePlayer的底层实现是AVPlayerLayer.
