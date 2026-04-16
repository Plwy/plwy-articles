# Tensorrt 性能优化

 TensorRT是nvidia的推理加速库，只能在nvdia的gpu上用！Intel cpu请使用openvino，amd gpu请使用opencl和ROCm。



## 如何进行性能测试

ref:https://zhuanlan.zhihu.com/p/553367059

### 性能衡量标准

- 单个推理的网络**延迟**：从输入呈现给网络到输出可用所经过的时间

- 网络的**吞吐量**：在固定的时间单位内可以完成多少推理。

仅考虑网络推理的延迟和吞吐量。不考虑前后处理。



### 性能测试工具和方法

#### 时钟计时

**测试网络的推理时间**

`std::chrono::system_clock`表示系统范围的经过时间，而`std::chrono::high_resolution_clock`以可用的最高精度测量时间。

```c++
#include <chrono>

auto startTime = std::chrono::high_resolution_clock::now();
context->enqueueV2(&buffers[0], stream, nullptr);
cudaStreamSynchronize(stream);
auto endTime = std::chrono::high_resolution_clock::now();
float totalTime = std::chrono::duration<float, std::milli>
(endTime - startTime).count();
```

#### CUDA Event

仅在主机上计时的一个问题是它需要主机/设备同步。 优化的应用程序可能会在设备上并行运行许多推理，并具有重叠的数据移动。 此外，同步本身给定时测量增加了一些噪声。

为了帮助解决这些问题，CUDA 提供了一个事件 API。 此 API 允许您将事件放入 CUDA 流中，这些事件将在遇到事件时由 GPU 打上时间戳。 然后时间戳的差异可以告诉您不同操作花费了多长时间。

#### Profiler

TensorRT 有一个**Profiler** ( [C++](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deeplearning/tensorrt/api/c_api/classnvinfer1_1_1_i_profiler.html) , [Python](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deeplearning/tensorrt/api/python_api/infer/Core/Profiler.html) ) 接口.完成推理后，将调用您的类的分析器对象以报告**网络中每一层的时间**。这些时序可用于定位瓶颈、比较序列化引擎的不同版本以及调试性能问题。

还可以使用`trtexec`在给定输入网络或计划文件的情况下使用 TensorRT 分析网络。



#### NVIDIA Nsight™ Systems

CUDA 分析器NVIDIA Nsight™ Systems 。用于报告在执行期间启动的内核、主机和设备之间的数据移动以及使用的 CUDA API 调用的时序信息。

在 Nsight Systems 中使用 `NVTX` 跟踪，NVTX 是一个基于 C 的 API，用于标记应用程序中的事件和范围。启用NVTX跟踪允许 Nsight Compute 和 Nsight Systems 收集由 TensorRT 应用程序生成的数据。 

TensorRT 使用 NVTX 为每一层标记一个范围，然后允许 CUDA 分析器将每一层与调用来实现它的内核相关联。在 TensorRT 中，NVTX 有助于将运行时引擎层的执行与 CUDA内核调用相关联。 Nsight Systems 支持在时间轴上收集和可视化这些事件和范围。 Nsight Compute 还支持在应用程序挂起时收集和显示给定线程中所有活动 NVTX 域和范围的状态

**构建引擎时设置NVTX的跟踪。**

默认情况下，TensorRT 仅在 NVTX 标记中显示层名称，而用户可以在构建引擎时通过设置`IBuilderConfig`中的 `ProfilingVerbosity` 来控制细节级别。

- 禁用 NVTX 跟踪，请将 `ProfilingVerbosity` 设置为`kNONE`

C++

```

builderConfig->setProfilingVerbosity(ProfilingVerbosity::kNONE);

```

Python

```
builder_config.profiling_verbosity = trt.ProfilingVerbosity.NONE
```

- 允许 TensorRT 在 NVTX 标记中打印更详细的层信息，包括输入和输出尺寸、操作、参数、顺序编号等。通过将`ProfilingVerbosity`设置为`kDETAILED`

C++

```
builderConfig->setProfilingVerbosity(ProfilingVerbosity::kDETAILED);
```

Python

```
builder_config.profiling_verbosity = trt.ProfilingVerbosity.DETAILED
```

**trtexec运行 Nsight 系统**

以下是使用trtexec工具收集 Nsight Systems 配置文件的命令示例：

```bash
# 构建引擎
trtexec --onnx=foo.onnx --profilingVerbosity=detailed --saveEngine=foo.plan
#  Nsight Systems 运行推理生成分析文件
nsys profile -o foo_profile trtexec --loadEngine=foo.plan --warmUp=0 --duration=0 --iterations=50
```

第一个命令构建引擎并将其序列化为`foo.plan` ，第二个命令使用`foo.plan`运行推理并生成一个`foo_profile.qdrep`文件，然后可以在 Nsight Systems GUI 界面中打开该文件以进行可视化。

`--profilingVerbosity=detailed`标志允许 TensorRT 在 NVTX 标记中显示更详细的层信息，而`--warmUp =0` `--duration=0` `--iterations=50`标志允许您控制要运行的推理迭代次数。默认情况下， trtexec运行推理三秒钟，这可能会导致输出 `qdrep` 文件非常大。

#### 跟踪设备内存

跟踪内存使用情况与执行性能一样重要。 通常，设备上的内存比主机上的内存更受限制。 为了跟踪设备内存，推荐的机制是创建一个简单的自定义 GPU 分配器，该分配器在内部保留一些统计信息，然后使用常规 CUDA 内存分配函数 `cudaMalloc` 和 `cudaFree`。

可以为构建器`IBuilder` 设置自定义 GPU 分配器以进行网络优化，并在使用`IGpuAllocato`r API 反序列化引擎时为`IRuntime` 设置。 自定义分配器的一个想法是跟踪当前分配的内存量，并将带有时间戳和其他信息的分配事件推送到分配事件的全局列表中。 查看分配事件列表可以分析一段时间内的内存使用情况。

在移动平台上，GPU 内存和 CPU 内存共享系统内存。 在内存大小非常有限的设备上，如 Nano，系统内存可能会因大型网络而耗尽； 甚至所需的 GPU 内存也小于系统内存。 在这种情况下，增加系统交换大小可以解决一些问题。 一个示例脚本是：

```shell
 echo "######alloc swap######"
 if [ ! -e /swapfile ];then
     sudo fallocate -l 4G /swapfile
     sudo chmod 600 /swapfile
     sudo mkswap /swapfile
     sudo /bin/sh -c 'echo  "/swapfile \t none \t swap \t defaults \t 0 \t 0" >> /etc/fstab'
     sudo swapon -a
 fi
```



## 部署时的Tensorrt优化策略

1.针对不同网络的优化策略，比如设计特定网络启用层融合，针对transformer的显式量化加速，针对图的CUDA调度优化。

2.engine转换时的优化策略， 通过设置批处理提高并行计算效率提高网络吞吐量，通过设置选择最优的engine转换策略， 

3.engine推理时的优化策略，streaming和多线程调度的配合，处理多并发并充分利用计算资源。



### 批处理

​	使用批处理并行计算，在 TensorRT 中，批次是可以统一处理的输入的集合。批次中的每个实例都具有相同的形状，并以完全相同的方式流经网络。因此，每个实例都可以简单地并行计算。通常，增加批量大小会提高总吞吐量。此外，当网络包含 `MatrixMultiply` 层或完全连接层时，如果硬件支持，由于使用了 Tensor Cores，32 的倍数的批大小往往对 FP16 和 INT8 推理具有最佳性能。

​	根据请求进行推理的服务器，可以实现机会批处理。对于每个传入的请求，等待时间T 。如果在此期间有其他请求进来，请将它们一起批处理。否则，继续进行单实例推理。这种类型的策略为每个请求增加了固定的延迟，但可以将系统的最大吞吐量提高几个数量级。

显示批处理和隐式批处理。

- 显式批处理：只需要通过在构建引擎时设置动态维度，指定批处理大小和批处理大小的范围。

- 隐式批处理：如果在创建网络时使用隐式批处理模式。在使用`IBuilder::setMaxBatchSize` 构建优化网络时，应该为构建器设置最大批量大小。当调用`IExecutionContext::execute`或`enqueue`时，作为绑定参数传递的绑定是按张量组织的，而不是按实例组织的。

​	构建优化的网络会针对给定的最大批量大小进行优化。最终结果将针对最大批量大小进行调整，但对于任何较小的批量大小仍然可以正常工作。可**以运行多个构建操作来为不同的批量大小创建多个优化引擎，然后在运行时根据实际批量大小选择要使用的引擎。**

### Stream

可以将多个主机线程与流一起使用。 一种常见的模式是将传入的请求分派到等待工作线程池中。 在这种情况下，工作线程池中的每一个都将具有一个执行上下文和 CUDA 流。 当工作变得可用时，每个线程将在自己的流中请求工作。 每个线程将与其流同步以等待结果，而不会阻塞其他工作线程。

CUDA图

[CUDA 图](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/cuda/cuda-c-programming-guide/index.html%23cuda-graphs)是一种表示内核序列（或更一般地是图）的方式，其调度方式允许由 CUDA 优化。 当您的应用程序性能对将内核排入队列所花费的 CPU 时间敏感时，这可能特别有用。

TensorRT 的`enqueuev2()` 方法支持对不需要 CPU 交互的模型进行 CUDA 图捕获







### 转engine时的策略

- 限制计算资源

在生成engine时限制计算资源，能使得engine针对有限的计算资源进行优化，并在推理期间使用类似条件时提供更好的吞吐量。

- 确定性战术选择

通过一些手段，如锁定 GPU 时钟频率等，使得TensorRT 在遍历所有可能的策略并选择最快的策略时，能选择到最佳的策略。



#### 限制计算资源



当减少的数量更好地代表运行时的预期条件时，限制在引擎创建期间可用于 TensorRT 的计算资源的数量是有益的。 例如，当期望 GPU 与 TensorRT 引擎并行执行额外工作时，或者当期望引擎在资源较少的不同 GPU 上运行时（请注意，推荐的方法是在 GPU 上构建引擎，即 将用于推理，但这可能并不总是可行的）。

您可以通过以下步骤限制可用计算资源的数量：

1. 启动 CUDA MPS 控制守护进程.
   nvidia-cuda-mps-control -d
2. 设置要与 `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE` 环境变量一起使用的计算资源的数量。 例如，`export CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=50`。
3. 构建网络引擎。
4. 停止 CUDA MPS 控制守护程序。
   echo quit | nvidia-cuda-mps-control

生成的引擎针对减少的计算核心数量（本例中为 50%）进行了优化，并在推理期间使用类似条件时提供更好的吞吐量。 鼓励您尝试不同数量的流和不同的 MPS 值，以确定网络的最佳性能。

有关 `nvidia-cuda-mps-control` 的更多详细信息，请参阅 [nvidia-cuda-mps-control](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deploy/mps/index.html%23topic_5_1_1) 文档和[此处](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deploy/mps/index.html%23topic_3_3_1_1)的相关 GPU 要求。

#### 确定性战术选择

在引擎构建阶段，TensorRT 会遍历所有可能的策略并选择最快的策略。 由于选择基于策略的延迟测量，因此如果某些策略具有非常相似的延迟，TensorRT 最终可能会在不同的运行中选择不同的策略。 因此，从相同 `INetworkDefinition` 构建的不同引擎在输出值和性能方面可能会略有不同。 您可以通过使用[引擎检查器](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deeplearning/tensorrt/developer-guide/index.html%23engine-inspector)或在构建引擎时打开详细日志记录来检查引擎的选定策略。

如果需要确定性的策略选择，下面列出了一些可能有助于改进策略选择的确定性的建议。

**锁定 GPU 时钟频率**

默认情况下，GPU 的时钟频率未锁定，这意味着 GPU 通常处于空闲时钟频率，只有在有活动的 GPU 工作负载时才会提升到最大时钟频率。 但是，从空闲频率提升时钟存在延迟，这可能会导致性能变化，同时 TensorRT 正在运行策略并选择最佳策略，从而导致不确定的策略选择。

因此，在开始构建 TensorRT 引擎之前锁定 GPU 时钟频率可能会提高策略选择的确定性。 您可以通过调用 `sudo nvidia-smi -lgc <freq>` 命令来锁定 GPU 时钟频率，其中 `<freq>` 是要锁定的所需频率。 您可以调用 `nvidia-smi -q -d SUPPORTED_CLOCKS` 来查找 GPU 支持的时钟频率。

因此，在开始构建 TensorRT 引擎之前锁定 GPU 时钟频率可能会提高策略选择的确定性。 有关如何锁定和监控 GPU 时钟以及可能影响 GPU 时钟频率的因素的更多信息，请参阅[性能测量的硬件/软件环境](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deeplearning/tensorrt/developer-guide/index.html%23hw-sw-environ-perf-measure)部分。

**增加平均时序迭代**

默认情况下，TensorRT 将每个策略运行至少四次迭代并取平均延迟。 您可以通过调用 `setAvgTimingIterations()` API 来增加迭代次数：

**C++**

```cpp
 builderConfig->setAvgTimingIterations(8);
```

**Python**

```python
 Builder_config.avg_timing_iterations = 8
```

增加平均计时迭代次数可能会提高战术选择的确定性，但所需的引擎构建时间会变得更长。

**使用TimingCache**

[The Timing Cache](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deeplearning/tensorrt/developer-guide/index.html%23builder-layer-timing) 记录特定层配置的每个策略的延迟。 如果 TensorRT 遇到具有相同配置的另一层，则会重用策略延迟。 因此，通过在使用相同 `INetworkDefinition` 和构建器配置运行的多个引擎构建中重用相同的时序缓存，您可以使 TensorRT 在生成的引擎中选择一组相同的策略。

有关详细信息，请参阅[The Timing Cache](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deeplearning/tensorrt/developer-guide/index.html%23builder-layer-timing) 部分。



## 如何提高GPU利用率

ref：[vivo 在推荐业务中如何用 MPS 提高 GPU 利用率？](https://zhuanlan.zhihu.com/p/579984363)

**目前主要有三条提高 GPU 利用率的策略**，一是通过**动态 Batch** 就把多个请求结合成一个，依次推理，这样还是在单个进程里面用一个 Context；二是起多个进程，同时提供服务，里面每个都是一个模型实例，这些多进程可以通过 MPS 技术，同时把任务提交给 GPU，GPU 会对这些资源进行隔离和限制，并发地运行里面的算子，从而达到动态 Batch 类似的效果；三是最新的 **GPU 支持**，类似硬件级别 GPU 虚拟化。

MPS 怎么用的 ？一个容器，也就是一个 Pod 分一张 GPU 卡，起一个Control 进程，这个 Control 进程负责管理这张卡，为这张卡起一个 MPS server，里面跑多个推理进程。这样 K8s 就可以正常的隔离，也不需要调整 K8s 的权限系统，Pod 的管理也比较方便。

ref:[[美团视觉GPU推理服务部署架构优化实践](https://tech.meituan.com/2023/02/09/inference-optimization-on-gpu-by-meituan-vision.html)](https://tech.meituan.com/2023/02/09/inference-optimization-on-gpu-by-meituan-vision.html)

https://tech.meituan.com/2022/03/03/ctr-gpu-inference.html



## Tensorrt 动态batch设置

ref:https://codeleading.com/article/20516360528/

转换具有动态batch的onnx模型，导出模型的时候，需要将模型输入的batch参数声明为动态参数

```python
# 定义输入名称，list结构，可能有多个输入
input_names = ['input']
# 定义输出名称，list结构，可能有多个输出
output_names = ['output']
# 声明动态维度，这里我们把input的第0维度赋名为batch_size
dynamic_axes = {
            'input': {0: 'batch_size'}
        }
 # 构造输入，用以onnx验证
input = torch.randn(2, 3, 384, 288, requires_grad=True)
torch.onnx.export(model, input, output_path,
                          export_params=True,
                          opset_version=10,
                          do_constant_folding=True,
                          input_names=input_names,
                          output_names=output_names,
                          dynamic_axes=dynamic_axes)
```

转出后，可以用netron来查看，转持的onnx模型，是否支持动态维度。

## Tensorrt的优化方式

ref:https://www.cnblogs.com/wujianming-110117/p/12983582.html

主要采用了以下方式来提升模型的运行速度。

- **层间融合或张量融合（Layer & Tensor Fusion）**

模型推理时是GPU通过启动不同的CUDA（核心来完成计算的，CUDA核心计算张量的速度是很快的，但是往往大量的时间是浪费在CUDA核心的启动和对每一层输入/输出张量的读写操作上面，这造成了内存带宽的瓶颈和GPU资源的浪费。

TensorRT通过对层间的横向或纵向合并，使得层的数量大大减少。横向合并可以把卷积、偏置和激活层合并成一个CBR结构，只占用一个CUDA核心。纵向合并可以把结构相同，但是权值不同的层合并成一个更宽的层，也只占用一个CUDA核心。合并之后的计算图的层次更少了，占用的CUDA核心数也少了，因此整个模型结构会更小，更快，更高效。

- **数据精度校准（Weight &Activation Precision Calibration）**

网络训练完成后，在部署推理的过程中由于不需要反向传播，可以适当降低数据精度，比如降为FP16或INT8的精度。更低的数据精度将会使得内存占用和延迟更低，模型体积更小。TensorRT会提供完全自动化的校准（Calibration ）过程，会以最好的匹配性能将FP32精度的数据降低为INT8精度，最小化性能损失。

- **Kernel Auto-Tuning**

网络模型在推理计算时，是调用GPU的CUDA核进行计算的。TensorRT可以针对不同的算法，不同的网络模型，不同的GPU平台，进行 CUDA核的调整（怎么调整的还不清楚），以保证当前模型在特定平台上以最优性能计算。

- **Dynamic Tensor Memory**

在每个tensor的使用期间，TensorRT会为其指定显存，避免显存重复申请，减少内存占用和提高重复使用效率。

- **Multi-Stream Execution**

Scalable design to process multiple input streams in parallel，这个应该就是GPU底层的优化了。

TensorRT具体加速效果决定于显卡和模型，例如在3080ti上resnet50从pytorch转TensorRT可以加速10倍，但是yolov5只能加速一倍多。

## TensorRT的运行过程

- 基本网络构建
  创建builder
  创建network
  创建config
  network添加输入
  network添加层，绑定输入
  network mark output，指定输出节点
  builder编译network
  序列化，并储存为文件
- 推理过程
  创建runtime
  反序列化engine
  创建执行上下文ExecuteContext
  获取binding的维度，并为输入输出节点分配内存
  为输入塞数据
  入队, context->enqueue(batch, void** bindings, stream, event);
  复制结果回主机
  流同步，等待推理结束
  打印结果

## trtexec进行模型转换

直接可以用以下命令进行模型转换

```bash
./trtexec --onnx=xxx.onnx --saveEngine=xxx.trt --workspace=1024 --minShapes=inputx:1x3x480x640 --optShapes=inputx:16x3x480x640 --maxShapes=inputx:32x3x480x640 --fp16

```

- onnx: 输入的onnx模型
- saveEngine：转换好后保存的tensorrt engine
- workspace：使用的gpu内存，有时候不够，需要手动增大点
- minShapes：动态尺寸时的最小尺寸，格式为NCHW，需要给定输入node的**名字**，
- optShapes：推理测试的尺寸，trtexec会执行推理测试，该shape就是测试时的输入shape
- maxShapes：动态尺寸时的最大尺寸，**这里只有batch是动态的，其他维度都是写死的**
- fp16：float16推理

optShape需要确定batch的具体大小，得到最优的engine

*maxBatchSize* 值的选择取决于应用程序以及任何给定时间的预期推断流量（例如，图像数）。通常的做法是构建多个针对不同批量大小优化的引擎（使用不同的 *maxBatchSize* 值），然后在运行时选择最优化的引擎。

