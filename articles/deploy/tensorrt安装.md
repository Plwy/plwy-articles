tensorrt 安装

**TAR包安装 8.5.3**

选择红框中的TAR 包进行下载。

![image-20250108151524674](tensorrt安装及使用.assets/image-20250108151524674.png)

得到文件`TensorRT-8.5.3.1`。并使用bin目录下的trtexec进行模型转换。

python中使用tensorrt推理,在python中使用`pip install tensorrt==8.5.3.1 `装包。

开始调用模型时候出现了：

```
trt version: 8.5.3.1
[01/08/2025-15:55:20] [TRT] [I] Loaded engine size: 50 MiB
[01/08/2025-15:55:20] [TRT] [E] 1: [stdArchiveReader.cpp::StdArchiveReader::42] Error Code 1: Serialization (Serialization assertion stdVersionRead == serializationVersion failed.Version tag does not match. Note: Current Version: 232, Serialized Engine Version: 213)
[01/08/2025-15:55:20] [TRT] [E] 4: [runtime.cpp::deserializeCudaEngine::66] Error Code 4: Internal Error (Engine deserialization failed.)
```

解决办法：

1.只下载后使用其中的txtexec命令不行。 首先修改本地环境变量，改为当前8.5.3.1的版本。使环境变量生效，然后重新打开terminal。这时重新生成后运行还是有问题。

```bash
# ~/.bashrc
export PATH=$PATH:/home/sun/softwares/TensorRT-8.5.3.1/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/sun/softwares/TensorRT-8.5.3.1/lib
```

2.python库安装使用TensorRT-8.5.3.1/python目录下的whl文件安装。` pip install ~/TensorRT-8.5.3.1/python/tensorrt-8.5.3.1-cp39-none-linux_x86_64.whl`

3.我将原始的tensorrt的目录移动到其他地方，重新生成了一遍，仔细看生成日志确定使用的8.5.3.1版本，运行不报序列版本问题了。 也就是刚才新设置的环境变量没有生效，还是使用了原始库中的文件。





