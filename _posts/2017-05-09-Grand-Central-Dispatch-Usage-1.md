---
layout: post
title:  "Grand Central Dispatch (1/2)"
date:   2017-05-09 20:54:20
categories: iOS
tags: iOS
---

## Introduction

在 iOS 和 macOS 开发过程中，频繁地使用到多线程编程来解决一些实际问题，如网络数据异步请求、图片异步加载、定时器实现等等。苹果提供了三种方法去完成多线程开发：

1. NSThread
2. NSOperationQueue
3. Grand Central Dispatch

其中 **Grand Central Dispatch** 是三者抽象程度最高，也是苹果推荐的开发方式。

> Grand Central Dispatch，简称 GCD，是 [libdispatch](https://libdispatch.macosforge.org) 的通俗叫法，它是由纯 C 语言实现，基于 XNU 内核（iOS 和 macOS 的操作系统内核）编写的高性能并发库。

在接下来的文章中，我会把 **Grand Central Dispatch (GCD)** 的用法分成几个模块进行介绍。

## Queue

队列 (Queue) 是编程中一种常见的数据结构，分为**串行队列 (Serial)** 和**并发队列 (Concurrent)**。

串行队列和并发队列都满足 **FIFO (First Input First Output)** 原则，即任务的执行顺序与任务添加到队列时的顺序保持一致，唯一不同的是，串行队列同一时间只允许一个任务处于执行状态，其他任务必须要等到之前的任务执行完毕后才可以开始执行，而并发队列则不需要等待上个任务执行完毕就可以开始执行。如下图

![serial_and_concurrent](/images/grand-central-dispatch-usage-1/serial_and_concurrent.jpg)

> 串行队列是单线程执行任务，并发队列是多线程执行任务。

GCD 中有两个获取系统队列的方法，分别用于获取主线程当前执行的串行队列和不同优先级的全局并发队列。

```objc
// 获取主线程当前执行的串行队列
dispatch_queue_t dispatch_get_main_queue()

// 获取对应优先级的全局并发队列
dispatch_queue_t dispatch_get_global_queue(long identifier, unsigned long flags)
```

获取全局队列方法参数中，`identifier` 决定了需要什么优先级的队列，`flags` 为预留参数，传入非 0 值可能会使得方法返回 nil。

队列的优先级有四种，分别是

```objc
DISPATCH_QUEUE_PRIORITY_HIGH        // 高优先级
DISPATCH_QUEUE_PRIORITY_DEFAULT     // 默认优先级
DISPATCH_QUEUE_PRIORITY_LOW         // 低优先级
DISPATCH_QUEUE_PRIORITY_BACKGROUND  // 后台优先级
```

注意，这里的优先级并不能保证加入队列中的任务执行的先后顺序，而是保证 CPU 分配给这几个队列并发执行的时间长短。这里需要理解两个词汇，**并发 (Concurrent)** 和**并行 (Parallelism)**。

多核设备可以同时并行地运行多个线程，而单核设备只能同时运行一个线程，为了达到多任务执行的效果，需要在多个线程之间进行切换，来看作是一种多线程处理，这个切换过程叫做**上下文转换 (Context Switch)**，如下图所示：

![parallelism_and_concurrent](/images/grand-central-dispatch-usage-1/parallelism_and_concurrent.jpg)

所以上述的优先级是对应并发情况下，高优先级分配的时间片更多更长。

如果上面两种队列都不能满足需求，我们可以选择自己创建符合条件的队列。

```objc
// 创建一个新的队列
dispatch_queue_t dispatch_queue_create(const char *_Nullable label, dispatch_queue_attr_t attr)
```

第一个参数 `label` 是新队列的标识或名称，会在调试过程中显示在对应的线程上，命名方式最好采用反向域名的方式，如 `com.mesird.UIRefresher`    
第二个参数`attr` 是队列的属性，决定新队列是**串行 (DISPATCH_QUEUE_SERIAL)** 还是**并发 (DISPATCH_QUEUE_CONCURRENT)**

当我需要一个自定义的并发队列进行大量计算时，我就可以这样写

```objc
// example : 创建一个串行队列
dispatch_queue_t serialQueue = dispatch_queue_create("com.mesird.queue.calculation", DISPATCH_QUEUE_CONCURRENT);
```

队列已经有了，接下来的事情就是把不同的任务添加到相应的队列中去执行。

队列的执行方式也有两种，**同步** 和 **异步**。相信了解过多线程编程的人对这两个名词并不陌生，同步就是在当前线程上执行任务，而异步则是在非当前线程上执行任务。

![sync_and_async](/images/grand-central-dispatch-usage-1/sync_and_async.jpg)

在每个 iOS 应用中，主线程都是绘制 UI 和手势交互的队列，当我们处理耗时任务时，需要在其他线程上完成，原因就是防止大量的耗时任务阻塞主线程绘制 UI 和手势交互，在用户视角的表现就是页面卡住了。

举个例子，如果你的应用需要进行网络请求，并且在服务端返回数据后进行页面渲染，那么你就需要使用异步请求接口再返回到主线程绘制 UI。

```objc
[NetworkService querySomeDataWithParameters:parameters andHandlerResult:^(BOOL success, NSDictionary *result, NSError *error) {
    if (success) {
        dispatch_async(dispatch_get_main_queue(), ^{
            // do some UI render work on main queue
        });
    } else {
        NSLog(@"Response error : %@", error.localizedDescription);
    }
}];
```

在上述代码中，网络请求方法内部实现异步请求，于是主线程不会被这次请求阻塞，其次在接口数据返回后，需要在主线程上渲染界面。

接下来看下面这段代码

```objc
- (void)viewDidLoad {
    [super viewDidLoad]; 
    
    dispatch_sync(dispatch_get_main_queue(), ^{
        // do some UI render work
    });
}
```

如果你已经尝试了，你会发现应用程序崩溃了，因为产生了**死锁 (Deadlock)**。

> 死锁：在并发系统中，发生了多个线程需要同时使用同一块公共资源，但同时在等待对方释放该资源的情况，如果没有外部干涉，这几个线程将会一直等待下去。这种互相等待释放资源的状态叫做死锁。

这是我们项目开发中禁止的写法，也是一项基本常识。在主线程上同步执行界面渲染工作，首先程序把这部分渲染任务添加到 **main queue** 上，然后等待 **main queue** 执行结束（同步）。因为这块渲染任务也是 **main queue** 的一部分，所以就相当于自己在等自己执行完成后再执行自己，因此形成了死循环。

主线程上同步渲染 UI 只是一种情况，只要在 A 线程上同步执行一个任务就会发生死锁。

## Barrier

考虑这样一种场景：线程 A 在更改一个 `nonatomic` 变量，同时线程 B 正在读取这个变量，这个时候我们无法保证线程 B 读取出来的变量值是线程 A 修改之前、修改之后亦或是修改过程中的值，我们把这种现象叫做 **非线程安全 (Thread-Unsafe)**，示例代码如下。

```objc
...
@property (nonatomic, strong) NSMutableArray *objects;

...
- (void)addObjectToArray:(id)object {
    if (object) {
        [self.objects addObject:object];
    }
}

- (NSArray *)readArray {
    return [NSArray arrayWithArray:self.objects];
}

```

在同一个线程中调用 `addObjectToArray:` 方法和 `readArray` 方法并不会产生任何问题，但是在多线程中会出现[**读写问题 (Readers–writers problem)**](https://en.wikipedia.org/wiki/Readers–writers_problem)。

非线程安全的变量可以在多线程中使用，但是不能同时进行读写操作，原因如上述。既然如此，我们可以把读写操作按照同步任务去执行，读操作和写操作只能同时执行一个，就可以避免这种情况。GCD 中提供了这样的两个方法：

```objc
// 添加栅栏任务并异步执行
void dispatch_barrier_async(dispatch_queue_t queue, dispatch_block_t block);
// 添加栅栏任务并同步执行
void dispatch_barrier_sync(dispatch_queue_t queue, dispatch_block_t block);
```

这两个方法的第一个参数都是需要添加到的队列，第二个参数是需要执行的任务。两者的图示如下：

![barrie](/images/grand-central-dispatch-usage-1/barrier.jpg)

使用 barrier 重构上述的代码，将 `addObjectToArray:` 方法以栅栏任务添加至自定义队列异步执行，并在同一队列上同步读取可变数组的值，这样就能保证读写一个非线程安全变量不出现问题。

```objc
...
@property (nonatomic, strong) NSMutableArray *objects;
@property (nonatomic, strong) dispatch_queue_t objectsAccessQueue;

...
- (instancetype)init {
    if (self = [super init]) {
        // some initial code here
        self.objectsAccessQueue = dispatch_queue_create("com.mesird.queue.barrier", DISPATCH_QUEUE_CONCURRENT);
    }
    return self;
}

- (void)addObjectToArray:(id)object {
    if (object) {
        dispatch_barrier_async(self.objectsAccessQueue, ^{
            [self.objects addObject:object];
        });
    }
}

- (NSArray *)readArray {
    __block NSArray *retObjects;
    dispatch_sync(self.objectsAccessQueue, ^{
        retObjects = [NSArray arrayWithArray:self.objects];
    });
    return retObjects;
}
```

## Singleton

在不使用 GCD 的情况下，我们编写单例的代码如下：

```objc
+ (instancetype)sharedManager {
    static SomeManager *sharedManager = nil;
    if (!sharedManager) {
        sharedManager = [[SomeManager alloc] init];
        // do some instance initialization here
    }
    return sharedManager;
}
```

这种写法看似没什么问题，但是在多线程情况下，若初始化代码较多，可能会出现线程 A 和线程 B 都进入到 `if` 的逻辑判断中，初始化代码被执行了两次，并且两次返回的 sharedManager 对象是不相同的。我们可以使用 `@synchronized()` 关键字加锁来解决该问题，其保证其大括号内的代码只会在一个线程上执行。

```objc
+ (instancetype)sharedManager {
    static SomeManager *sharedManager = nil;
    @synchronized(self) {
        if (!sharedManager) {
            sharedManager = [[SomeManager alloc] init];
            // do some instance initialization here
        }
    }
    return sharedManager;
}
```

我们还可以使用 `dispatch_once` 来实现单例方法，代码如下。

```objc
+ (instancetype)sharedManager {
    static SomeManager *sharedManager = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedManager = [[SomeManager alloc] init];
        // do some instance initialization here
    });
    return sharedManager;
}
```

> 注：使用 `dispatch_once` 创建的单例，初始化代码只会执行一次，若在 App 运行期间将该单例置为 nil，则该单例永远只能为 nil。

## Timer

很多情况下，我们需要延时展示/隐藏一张图片或其他控件，我们会想到使用 **定时器 (NSTimer)**，或是直接使用 **runtime** 的方法 `performSelector:withObject:afterDelay:` 来实现某个时间之后执行对应的选择子。

GCD 中提供了一个方法来达到同样的效果，即在固定时间后执行某一个任务。

```objc
void dispatch_after(dispatch_time_t when, dispatch_queue_t queue, dispatch_block_t block);
```

该方法把对应的任务 `block` 在具体的时间点 `when` 加入到指定的队列 `queue` 中，随后执行。需要注意的是，这里的具体时间到达时，只是将该任务添加到队列中，而不是真正的执行时间，所以虽然 dispatch_time_t 类型能够精确到微秒，但是具体的执行时间会有细微的偏差，在一般的业务开发中基本可以忽略不计。

Xcode 提供了该方法的代码块，如下述代码，在 3 秒后执行一个动画，将 `transparentAlertView` 渐隐并最终移除该控件。

```objc
dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(3 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
    // 执行动画，渐隐 alertView
    [UIView animateWithDuration:0.3 animations:^{
        self.transparentAlertView.alpha = 0;
    } completion:^(BOOL finished) {
        if (finished) {
            [self.transparentAlertView removeFromSuperView];
        }
    }];
});
```

上述代码通过 `dispatch_time()` 创建一个 dispatch_time_t 对象来表示一个具体的时间点，`NSEC_PER_SEC` 是一个秒单位，`DISPATCH_TIME_NOW` 表示当前时间。

## Apply

在多线程编程中，我们一般会在其他线程上执行一个任务，如果希望执行固定次数任务的话，GCD 提供了 `dispatch_apply` 方法。

```objc
void dispatch_apply(size_t iterations, dispatch_queue_t queue, void (^block)(size_t));
```

参数 `iterations` 表示重复次数，`queue` 为指定添加到的队列，带参数的 `block` 为任务，参数指第几次执行，一个数组遍历的代码示例如下：

```objc
NSArray *objects = @[@"1", @"a", @"text"];
dispatch_queue_t queue = dispatch_queue_create("com.mesird.queue.interation", DISPATCH_QUEUE_SERIAL);
dispatch_apply(objects.count, queue, ^(size_t index){
    NSLog(@"%@", objects[index]);
});
NSLog(@"Done");
```

上述代码创建了一个同步队列用于执行任务，之后往该队列上添加了 10 个任务，最终的输出结果是数组 `objects` 的遍历以及最后输出了 "Done"。

> 可以将 `dispatch_apply` 理解为往对应的队列中添加了 N 个同步任务，因此谨慎在主线程中使用该方法，如果任务过大会阻塞 UI 绘制。

## Group
 
在日常开发中往往会出现这种情况，你需要知道一个队列中的任务什么时候执行结束，以便做一些收尾工作，就好比动画结束后会执行 `complete:^(BOOL finished){}` 这个 block。

如果这个队列是串行队列，那么好办，只需要在往串行队列中添加一个收尾任务即可：

```objc
dispatch_queue_t serialQueue = dispatch_queue_create("com.mesird.queue.serial", DISPATCH_QUEUE_SERIAL);
dispatch_async(serialQueue, ^{
    // handle some tasks here
});
```

但是如果这个队列是一个并发队列，或是几个队列的情况，则不好把控具体哪一个队列的任务会最后执行完成，这个时候我们需要使用到 **dispatch_group**。

**dispatch_group** 是一个队列的组，group 可以获知当前组内的队列是否都已经执行完毕，也可以设置一个完成通知，当所有队列的任务都执行完成后，通知 group 去执行一些任务。

```objc
// 队列任务全部结束后通知执行任务
void dispatch_group_notify(dispatch_group_t group, dispatch_queue_t queue, dispatch_block_t block);
```

`group` 是需要监测的队列组，当队列的任务都执行完成后，队列 `queue` 被通知去执行任务 `block`。

在实际开发中会有这样一种情况，当一个页面涉及到两个接口去加载数据，并且只有两个接口都返回数据后才会刷新页面，这个时候我们可以把这两个接口请求队列添加到一个组中，当且仅当两个请求队列任务执行完成后通知组去执行刷新任务。

```objc
dispatch_queue_t queryQueueA = dispatch_queue_create("com.mesird.queue.queryA", DISPATCH_QUEUE_CONCURRENT);
dispatch_queue_t queryQueueB = dispatch_queue_create("com.mesird.queue.queryB", DISPATCH_QUEUE_CONCURRENT);
dispatch_group_t queryGroup = dispatch_group_create();
dispatch_group_async(queryQueueA, ^{
    // request some data from server
});
dispatch_group_async(queryQueueB, ^{
    // request some data from server
});
__weak __typeof(self) weakSelf = self;
dispatch_group_notify(queryGroup, dispatch_get_main_queue(), ^{
    // refresh UI on main queue
    __strong __typeof(weakSelf) strongSelf = weakSelf;
    [strongSelf.tableView reloadData];
});
```

同时，如果你要在某个时间点去获取某个 group 中的队列是否执行完成，可以使用该方法：

```objc
long dispatch_group_wait(dispatch_group_t group, dispatch_time_t timeout);
```

参数 `group` 对应的是需要检测的队列组，`timeout` 参数表示等待多久之后返回结果，可以传 `DISPATCH_TIME_NOW` 表示立即返回检测结果和 `DISPATCH_TIME_FOREVER` 表示一直等到队列任务执行结束后再返回，同样也可以传入自定义的时间表示等待多久时间后返回结果。

> `dispatch_group_wait` 同步执行，等待 `timeout` 时间到或组中队列任务执行结束，在这段时间内，执行该方法的现成是被阻塞的。也可以直白地理解为，`dispatch_group_async` 方法可以异步获取队列执行结束的时间，而 `dispatch_group_wait` 方法则是同步等待到队列结束。

## Semaphore

提到多线程编程，少不了的就是同步互斥问题。信号量作为基础的数据结构，能够避免 **资源竞争(Race Condition)** 现象。

GCD 提供了信号量类 **dispatch_semaphore_t** 以及如下两个方法来解决同步互斥问题。

```objc
// 创建信号量
dispatch_semaphore_t dispatch_semaphore_create(long value);
// 资源等待并占用
long dispatch_semaphore_wait(dispatch_semaphore_t dsema, dispatch_time_t timeout);
// 资源释放
long dispatch_semaphore_signal(dispatch_semaphore_t dsema);
```

创建信号量的参数 `value` 指定了信号量的值（可以直白地理解为该资源可以同时被几个线程同时使用）。

`dispatch_semaphore_wait` 方法与 `dispatch_group_wait` 方法相似，需要传递一个时间参数表示等待多久，在该方法中如果传入 `DISPATCH_TIME_FOREVER` 则会一直阻塞当前线程直到该资源被其他线程释放，当该信号量的值大于等于 1 时，方法会返回 0，并且同时将信号量的值减去 1，表明当前线程要使用该资源。

`dispatch_semaphore_signal` 方法的工作就是将对应的信号量加 1。

一个使用信号量的代码示例：

```objc
NSMutableArray *objects = [NSMutableArray array];
dispatch_queue_t queue = dispatch_queue_create("com.mesird.queue.concurrent", DISPATCH_QUEUE_CONCURRENT);
// 创建信号量，初始值为 1
dispatch_semaphore_t semaphore = dispatch_semaphore_create(1);
for (int i = 0; i < 100; i ++) {
   dispatch_async(queue, ^{
       // 等待并持有信号量 (-1)
       dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
       // 使用资源
       [objects addObject:@(i)];
       // 释放信号量 (+1)
       dispatch_semaphore_signal(semaphore);
   });
}
```

## ARC

GCD 中涉及到的类如 `dispatch_group_t`、`dispatch_queue_t`、`dispatch_time_t` 等等，均继承自 **NSObject**，在 ARC 环境下，不需要再做人为的内存管理操作。


