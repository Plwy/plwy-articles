## pytorch如何实现利用多GPU训练

多GPU可以使用 `nn.DataParallel` 打包模型，再使用`model.to(device)` 把模型传送到多块GPU中进行运算。

```python
model = Model(input_size, output_size)  # 实例化模型对象
if torch.cuda.device_count() > 1:  # 检查电脑是否有多块GPU
    print(f"Let's use {torch.cuda.device_count()} GPUs!")
    model = nn.DataParallel(model)  # 将模型对象转变为多GPU并行运算的模型

model.to(device)  # 把并行的模型移动到GPU上
```

pytorch会根据batch_size大小将每个batch的数据平均分到多个gpu上。



## **nn.DataParallel详细解析**

`torch.nn.DataParallel(module, device_ids=None, output_device=None, dim=0)`:

这个函数主要有三个参数：

1. `module`：即模型，此处注意，虽然输入数据被均分到不同gpu上，但每个gpu上都要拷贝一份模型。
2. `device_ids`：即参与训练的gpu列表，例如三块卡， device_ids = [0，1，2]。
3. `output_device`：指定输出gpu，一般省略。在省略的情况下，默认为第一块卡，即索引为0的卡。此处有一个问题，输入计算是被几块卡均分的，但输出loss的计算是由这一张卡独自承担的，这就造成这张卡所承受的计算量要大于其他参与训练的卡。

**下面来具体讲讲`nn.DataParallel`中是怎么做的：**

首先在前向过程中，你的输入数据会被划分成多个子部分（以下称为副本）送到不同的`device`中进行计算，而你的模型`module`是在每个`device`上进行复制一份，也就是说，输入的`batch`是会被平均分到每个`device`中去，但是你的模型`module`是要拷贝到每个`devide`中去的，每个模型`module`只需要处理每个副本即可，当然你要保证你的`batch size`大于你的`gpu`个数。然后在反向传播过程中，每个副本的梯度被累加到原始模块中。概括来说就是：**`DataParallel`会自动帮我们将数据切分 `load` 到相应 `GPU`，将模型复制到相应 `GPU`，进行正向传播计算梯度并汇总。**





 **如何保存和加载多GPU网络？**

如何来保存和加载多GPU网络，它与普通网络有一点细微的不同：

```python3
net = torch.nn.Linear(10,1)  # 先构造一个网络
net = torch.nn.DataParallel(net, device_ids=[0,3])  #包裹起来
torch.save(net.module.state_dict(), './networks/multiGPU.h5') #保存网络

# 加载网络
new_net = torch.nn.Linear(10,1)
new_net.load_state_dict(torch.load("./networks/multiGPU.h5"))
```

因为`DataParallel`实际上是一个`nn.Module`，所以我们在保存时需要多调用了一个`net.module`，模型和优化器都需要使用`net.module`来得到实际的模型和优化器。

ref:https://zhuanlan.zhihu.com/p/393857045

