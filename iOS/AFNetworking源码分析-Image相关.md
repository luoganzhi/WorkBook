# Image源码分析

- 解决了单个imageView多次请求一个url问题
- 解决了多个imageView请求一个url问题
- 处理了图片下载的线程安全问题, 创建下载图片任务是一个串行同步队列,每次只能等一个创建完再创建.
- 自己维护了一个任务池,一个待处理任务池,当前最多任务为4,多余的会放入待处理任务池.
- 处理了图片内存管理的问题
- 没有处理沙盒中图片管理,交给了系统来处理.

### 类分析
1. AFImageDownloader: 处理所有的下载逻辑,内部有:
	```
	@interface AFImageDownloader () 
	@property (nonatomic, strong, nullable) id <AFImageRequestCache> imageCache; // 所有缓存的管理对象 遵守AFImageRequestCache协议,默认对象为AFAutoPurgingImageCache
	@property (nonatomic, strong) AFHTTPSessionManager *sessionManager; // 如果不设置manager,默认为单例对象


	@property (nonatomic, strong) dispatch_queue_t synchronizationQueue; // 同步串行队列,处理所有图片的下载
	@property (nonatomic, strong) dispatch_queue_t responseQueue; // 响应并发队列,处理所有的响应

	@property (nonatomic, assign) NSInteger maximumActiveDownloads; // 最大下载数
	@property (nonatomic, assign) NSInteger activeRequestCount; 

	@property (nonatomic, strong) NSMutableArray *queuedMergedTasks; // 存放所有需要下载任务,如果当前最大下载数小于最大下载数,就不存放任务,直接resume
	@property (nonatomic, strong) NSMutableDictionary *mergedTasks; // 存放每一个下载任务,key为rul,值为AFImageDownloaderMergedTask

	@end
	```
2. AFImageDownloaderMergerTask 下载任务对象
	```
	@interface AFImageDownloaderMergedTask : NSObject
	@property (nonatomic, strong) NSString *URLIdentifier; // 根据url生成的唯一标识符
	@property (nonatomic, strong) NSUUID *identifier;
	@property (nonatomic, strong) NSURLSessionDataTask *task; // 下载任务
	@property (nonatomic, strong) NSMutableArray <AFImageDownloaderResponseHandler*> *responseHandlers;// 所有请求过这个url的不同对象的handle都放入这里

	@end

	```
3. AFImageDownloaderResponseHandler 下载任务回调handler
	```
	@interface AFImageDownloaderResponseHandler : NSObject
	@property (nonatomic, strong) NSUUID *uuid; // 标志id,仅仅标志
	@property (nonatomic, copy) void (^successBlock)(NSURLRequest *, NSHTTPURLResponse *, UIImage *);
	@property (nonatomic, copy) void (^failureBlock)(NSURLRequest *, NSHTTPURLResponse *, NSError *);
	@end
	```
4. AFAutoPurgingImageCache 缓存管理对象
	```
	@interface AFAutoPurgingImageCache () // 管理内存
	@property (nonatomic, strong) NSMutableDictionary <NSString* , AFCachedImage*> *cachedImages; // 缓存的所有图片, identify作为key取图片
	@property (nonatomic, assign) UInt64 currentMemoryUsage; // 当前使用的内存
	@property (nonatomic, strong) dispatch_queue_t synchronizationQueue; // 同步队列
	@end

	```
5. AFCachedImage 缓存image包装对象 
	```
	@interface AFCachedImage : NSObject

	@property (nonatomic, strong) UIImage *image; // 存储的图片
	@property (nonatomic, copy) NSString *identifier; // 每个图片的标识符,根据url生成
	@property (nonatomic, assign) UInt64 totalBytes; // 图标大小
	@property (nonatomic, strong) NSDate *lastAccessDate; // 上次访问,使用时间
	@property (nonatomic, assign) UInt64 currentMemoryUsage; // 当前内存使用量

	@end

	```

### 流程总结

1. 下载的时候先判断url是否有效,如果无效直接设置placeholderImage为当前image
2. 判断当前对象当前url是否在下载,通过Association关联对象判断,如果在下载直接返回,防止单个对象重复下载.
3. 清空当前对象其他操作,将当前任务放入.
4. 根据缓存判断是否图片,有就直接返回,没有开启下载
5. 将任务包装成AFImageDownloaderMergerTask,如果是不同对象的相同请求,放入AFimageDownloaderMergerTask的responsHandlers中
6. 下载完成,遍历handlers,将值传递出去
7. 将管理对象的值清空


> 最大下载数是能放进线程的数,但是线程还是串行,只能一个一个执行,最大下载数为4

> 缓存图片默认最大容量是100M,超过100M将清理缓存,如果不配置用户偏好缓存设置,就清理到60M以下,按LRU算法清理,即最不常用的删除掉
