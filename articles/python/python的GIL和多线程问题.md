**GIL是什么？**

GIL的作用：

- **防止多线程竞争：** GIL确保同一时刻只有一个线程执行Python字节码。
- **限制CPU密集型任务的并行性，简化内存管理：** 对于CPU密集型任务，由于GIL的存在，多线程无法充分利用多核CPU，因为在任何给定时刻，只有一个线程能够执行Python字节码。

GIL的本质：

GIL实际上是一个互斥锁，在Python解释器层面上实现。由于GIL的存在，同一时刻只有一个线程能够获得解释器的控制权，其他线程被阻塞，无法执行Python字节码。这意味着在多核CPU上，Python的多线程程序可能无法充分利用多核性能。



**python的多线程是否无用？**

python下的多线程对CPU密集型代码并不友好，对IO密集型代码比较友好。

1、CPU密集型代码(各种循环处理、计数等等)，在这种情况下，ticks计数很快就会达到阈值，然后触发GIL的释放与再竞争（多个线程来回切换当然是需要消耗资源的），所以**python下的多线程对CPU密集型代码并不友好。**

2、IO密集型代码(文件处理、[网络爬虫](https://zhida.zhihu.com/search?content_id=564243&content_type=Article&match_order=1&q=网络爬虫&zhida_source=entity)等)，多线程能够有效提升效率(单线程下有IO操作会进行IO等待，造成不必要的时间浪费，而开启多线程能在线程A等待时，自动切换到线程B，可以不浪费CPU的资源，从而能提升程序执行效率)。**所以python的多线程对IO密集型代码比较友好。**



**如何避免GIL的影响提高Python程序的并发性能**

1. c代码扩展。使用cython，cytpe等将cpu密集型计算进行重写。
2. 多进程。通过使用`multiprocessing`模块，可以创建多个进程来充分利用多核CPU。每个进程有各自独立的python解释器和GIL，实现并行。
3. 异步编程。采用异步编程模型，如`asyncio`库，可以在IO密集型任务中充分利用事件循环和协程来避免GIL的影响。异步编程避免了线程的阻塞等待，使得单个线程能够处理多个任务。



ref:

https://blog.csdn.net/qq_41586251/article/details/135117057

https://zhuanlan.zhihu.com/p/20953544
