**调用jni接口的release后，java程序仍占用了显存的问题。**

1.显存是否释放干净

有残留

2.是否与转出的模型设置有关。

设置nocache重转后仍有残留

3.tensorrt 执行释放后，逻辑上gpu是否应该完全释放干净

不会完全释放干净

ref:https://github.com/HeKun-NVIDIA/TensorRT-Developer_Guide_in_Chinese/blob/main/5.TensorRT%E5%A6%82%E4%BD%95%E5%B7%A5%E4%BD%9C/5.TensorRT%E5%A6%82%E4%BD%95%E5%B7%A5%E4%BD%9C.md

**tensorrt运行时的主要设备内存占用：**

context使用的持久内存和暂存内存量,

engine在反序列化时分配设备内存来存储模型权重

TensorRT 默认直接从 CUDA 分配设备内存。并不会控制所有 GPU 内存。

TensorRT 的依赖项（ [cuDNN](https://developer.nvidia.com/cudnn)和[cuBLAS](https://developer.nvidia.com/cublas) ）会占用大量设备内存。CUDA 基础设施和 TensorRT 的设备代码也会消耗设备内存。内存量因平台、设备和 TensorRT 版本而异。



4.release后未能释放干净，重新初始化engine ，infer，再release， 残留的显存是否会叠加。

不会叠加，不管加载并释放多少个模型， release后残留的显存占用不变。说明占用的是必要的一些比如cuda基础或者依赖项。在进程结束后会释放，所以这种显存占用可以不用全部释放。
