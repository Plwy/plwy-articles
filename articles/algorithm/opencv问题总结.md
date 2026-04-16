## opencv 的ubuntu下的安装问题

### 针对需求编译安装opencv，当前需要一个怎样的opencv包

1.只是使用简单的函数，测一下opencv的使用。

2.不需要图形图像界面显示，使用基本的图像处理。

### apt install ,pip install , 和源码编译安装的差异。

pip install 安装的opencv的python包。通常`pip install opencv-python` 命令。

apt install 和源码安装的差异主要在于，安装位置，以及自定义安装选项。

源码安装可以自定义编译选项，比如以及是否编译特定的算法功能等。

apt 安装的方法可以自动处理依赖关系

### opencv如何干净的卸载重装

1.卸载软件apt包管理仓库中的opencv

```
sudo apt-get purge libopencv*
```

2.源码编译的卸载。到源码编译的目录下，找到编译好的build目录，在build目录下执行卸载命令, 然后删除build目录。

```
cd build
sudo make uninstall
cd ..
sudo rm -r build #  
```

删除可能的相关文件夹，通常安装在这些目录

```
sudo rm -r 
/usr/local/include/opencv4
/usr/local/lib/libopencv*
/usr/local/share/opencv4
/usr/local/bin/opencv* 

/usr/include/opencv 
/usr/share/opencv 
```

3.删除pip安装的opencv包 

```
pip uninstall opencv-python
```

### 使用cmake对源码进行编译

1.cmake图像界面编译；

2.cmake命令编译。

如何根据需求设置编译选项？后面安装例子提到。

### 什么时候编译成opencv_world

opencv_world将所有模块打包成了一个库。这样只使用一个链接就可以使用多个opencv模块，当不确定使用哪些模块，可以一起打包为opencv_world。需要设置 `BUILD_opencv_world=ON`。

### **opencv和opencv_contirb包的模块说明**

- core: OpenCV 核心功能模块，提供了基本的数据结构、图像处理函数和数学运算等常见功能。

- imgcodecs: 图像编解码模块，用于读取、写入和编解码各种图像格式，如JPEG、PNG等。

- imgproc: 图像处理模块，提供了图像处理和操作的函数，包括滤波、边缘检测、几何变换等。

- calib3d: 相机标定和三维重建模块，用于相机标定、立体视觉、姿态估计和三维物体重建等任务。

- highgui: 高级图形用户界面模块，提供了创建窗口、显示图像、处理鼠标和键盘事件等功能，用于快速构建基于图形界面的应用程序。

- dnn: 深度学习模块，用于加载和运行深度学习模型，以进行图像分类、目标检测、语义分割等任务。

- features2d: 特征检测和描述子模块，提供了常用的特征点检测和描述子生成算法，用于图像匹配、目标跟踪等。

- flann: 快速近似最近邻搜索模块，提供了一种高效的近似最近邻搜索算法，用于快速检索和匹配大规模特征数据库。

- gapi: 图形加速模块，用于图像和视频数据的高性能处理和计算，提供了简化编程模型和优化的图像处理操作。

- ml: 机器学习模块，提供了各种机器学习算法和工具，包括分类、回归、聚类和降维等任务。

- objc: Objective-C 接口模块，用于在 iOS 和 macOS 平台上使用 OpenCV 库进行图像处理和计算视觉任务。

- objdetect: 目标检测模块，提供了常见的目标检测算法和预训练的目标检测模型，用于检测和识别图像中的对象。

- photo: 图像编辑模块，提供了对图像进行颜色校正、噪声去除、图像增强等操作的函数。

- stitching: 图像拼接模块，用于将多张图像拼接成全景图像或景深图像，适用于创建全景照片和虚拟现实等应用。

- ts: 测试模块，包含了 OpenCV 的单元测试和功能测试框架，用于验证库的正确性和稳定性。

- video: 视频处理模块，提供了视频捕获、读写和处理的函数，包括光流估计、视频稳定等功能。

- videoio: 视频输入/输出模块，用于读取和写入各种视频格式的文件，并提供了与摄像头设备进行交互的功能。


opencv-contrib 则是一些外围组件，提供的模块包括:

- cuda: CUDA加速模块，用于利用NVIDIA的CUDA平台进行图像处理和计算的加速。
- alphamat: 基于图像和视频的前景/背景分割模块，用于提取图像中的前景对象或分离图像的前景和背景。
- aruco: ArUco标记检测模块，用于在图像中检测和识别ArUco标记，常用于相机姿态估计和增强现实等应用。
- bgsegm: 背景分割模块，提供了一些用于背景建模和背景分割的算法，用于从图像或视频中提取前景对象。
- bioinspired: 生物启发模块，提供了一些基于生物视觉系统的图像处理算法，用于模仿人类和动物视觉系统的特性。
- ccalib: 相机标定模块，提供了相机标定和立体视觉校准的函数，用于获取相机内外参数和立体视觉的对齐。
- cnn_3dobj: 3D目标检测和姿态估计模块，用于检测和识别图像中的三维对象，并估计其姿态。
- cvv: OpenCV可视化模块，提供了一组用于图像和数据可视化的工具和界面。
- datasets: 数据集模块，提供了一些常用的计算机视觉和机器学习数据集，用于算法开发和性能评估。
- dnn_objdetect: 基于深度学习的目标检测模块，提供了使用预训练的深度学习模型进行目标检测的函数。
- dnn_superres: 基于深度学习的图像超分辨率模块，用于将低分辨率图像放大为高分辨率图像。
- dnns_easily_fooled: 深度神经网络易受攻击模块，用于生成对深度神经网络易于误导的输入数据。
- dpm: 部件级别模型模块，用于利用部件级别模型进行目标检测和姿态估计。
- face: 人脸识别和人脸特征点检测模块，用于人脸识别、表情识别和人脸特征点定位等任务。
- freetype: FreeType字体渲染模块，用于在图像中渲染文本和字体。
- fuzzy: 模糊逻辑模块，提供了一些模糊逻辑和模糊集合的函数，用于处理模糊和不确定性的问题。
- hdf: HDF5数据存储模块，提供了一些用于读写HDF5格式数据的函数和接口。
- julia: Julia语言接口模块，用于在OpenCV中使用Julia语言进行图像处理和计算视觉任务。
- line_descriptor: 线段描述子模块，用于检测和描述图像中的线段特征。
- matlab: MATLAB接口模块，用于在MATLAB环境中调用OpenCV函数进行图像处理和计算视觉任务。
- mcc: 多相机系统校准模块，用于多相机系统的标定和几何校准。
- optflow: 光流估计模块，提供了一些光流估计算法，用于分析运动的图像序列。
- ovis: OGRE可视化模块，用于将3D对象和场景可视化，并在其中添加计算机视觉效果。
- plot: 图表绘制模块，提供了绘制各种图表和图形的函数，用于数据可视化和分析。
- reg: 图像配准模块，用于对齐和配准图像，以进行图像拼接、图像融合和图像比较等任务。
- rgbd: RGBD数据处理模块，用于处理RGBD数据（RGB图像+深度图像），如点云生成、物体识别等。
- saliency: 显著性检测模块，用于检测图像中显著目标或区域。
- sfm: 稀疏结构光束法平差模块，用于从多张图像中恢复相机姿态和三维结构。
- stereo: 立体视觉模块，提供了一些立体匹配算法和立体视觉的函数，用于处理立体图像和进行深度估计。
- structured_light: 结构光模块，用于使用结构光进行三维重建和表面重建。
- text: 文本检测和识别模块，用于检测和识别图像中的文本内容。
- tracking: 目标跟踪模块，提供了一些目标跟踪算法，用于连续跟踪视频序列中的目标。
- xfeatures2d: 扩展特征检测和描述子模块，提供了一些额外的特征检测和描述子算法，如SIFT、SURF等。
- ximgproc: 扩展图像处理模块，提供了一些额外的图像处理算法和滤波器，如边缘保持滤波、颜色空间转换等。
- xobjdetect: 扩展目标检测模块，提供了一些额外的目标检测算法和预训练的目标检测模型。
- xphoto: 扩展图像修复和颜色校正模块，提供了一些图像修复和颜色校正的算法和函数。

![opencv代码框架分析](https://pica.zhimg.com/70/v2-2e293367ca6129318fbda5b776559623_1440w.image?source=172ae18b&biz_tag=Post)



### **何时选择是否编译opencv-contrib**

当需要使用比如contrib包中的cuda库目标检测等库时，添加opencv-contib的module路径至opencv编译时的opencv  extra path 路径。cmake GUI可搜extra。

### pip提供的opencv安装包

pip提供的opencv的包的类型有四种，都可以直接通过pip install安装。

- **opencv-python**

  只包含opencv库的主要模块. 一般不推荐安装.

- **opencv-contrib-python**

  包含主要模块和contrib模块, 功能基本完整, 推荐安装.

- **opencv-python-headless**

  和opencv-python一样, 但是没有GUI功能, 无外设系统可用.

- **opencv-contrib-python-headless**

  和opencv-contrib-python一样但是没有GUI功能. 无外设系统可用.它是一个轻量级的OpenCV扩展库，它只包含了一些相对简单的功能，例如绘图、颜色转换等。

  **不要同时安装opencv-python和opencv-contrib-python**



### **移动端使用的opencv如何编译的**

[opencv-mobile](https://github.com/nihui/opencv-mobile) opencv 库的最小构建。可以直接从这里下载编译好的包。

**android和ios下编译opencv**

ref:

https://blog.csdn.net/u013740166/article/details/130261564

https://blog.csdn.net/u011520181/article/details/106931617

https://be7v.top/archives/119.html



### **opencv如何做到的跨平台**

使用C++编写，使用跨平台的CMake作为构建工具，可在不同的操作系统和编译环境下进行构建。提供了一些抽象接口可支持调用不同平台上的底层库。

## 本地opencv重装

- **卸载opencv** ，通常涉及以下几个目录

```bash
sudo rm -r 
/usr/local/include/opencv4
/usr/local/lib/libopencv*
/usr/local/share/opencv4
/usr/local/bin/opencv* 

/usr/include/opencv 
/usr/share/opencv 
```



- **编译配置**

1.搜cuda，相关的都on了，with_cuda ,... ，

2.根据显卡算力设置，cuda_arch_bin设为 7.5  ref[here](https://github.com/opencv/opencv/issues/21887)， 否则编译时可能出现以下错误

```
Built target opencv_cudaarithm make: *** [Makefile:166: all]
```

3.设置extra module path

然后generate， 出现anaconda库冲突问题

```
CMake Warning at cmake/OpenCVUtils.cmake:1547 (add_library):
  Cannot generate a safe runtime search path for target opencv_imgcodecs
  because files in some directories may conflict with libraries in implicit
  directories:

    runtime library [libpng16.so.16] in /usr/lib/x86_64-linux-gnu may be hidden by files in:
      /home/sun/anaconda3/lib
    runtime library [libz.so.1] in /usr/lib/x86_64-linux-gnu may be hidden by files in:
      /home/sun/anaconda3/lib
    runtime library [libtiff.so.5] in /usr/lib/x86_64-linux-gnu may be hidden by files in:
      /home/sun/anaconda3/lib

  Some of these libraries may not be found correctly.
Call Stack (most recent call first):
  cmake/OpenCVModule.cmake:966 (ocv_add_library)
  cmake/OpenCVModule.cmake:882 (_ocv_create_module)
  modules/imgcodecs/CMakeLists.txt:157 (ocv_create_module)

```

4.修改PATH环境变量

开始修改的~/.bashrc, source 后出现。

```
 " command not found: shopt "
```

这是因为装了zsh ，应该修改~/.zshrc

```bash
vim ~/.zshrc  #注释掉了anaconda的设置部分
source ~/.zshrc
# 这里echo $PATH 发现没有生效，也重开了teminal
#又改了
vim /etc/profile #同样注释掉了anaconda的设置部分
source /etc/profile 
# 这里echo $PATH 发现没有生效，也重开了teminal
```

试着重新编译还是显示库冲突。试着重启了电脑才修改生效， $PATH中终于没有了anaconda/bin。重新配置cmake后生成也不再显示库冲突。

5.将4.6.0换成了4.8.0。 4.6.0使用的opencv_contrib-4.x包， module下有文件在编译时出错。

6.安装上面一样重新配置，编译通过。能够正常使用cuda相关库。



# 板端安装ffmpeg和opencv记录

交叉编译3568 opencv

下载[ffmpeg](https://ffmpeg.org/download.html)

下载[opencv4.6.0.zip](https://github.com/opencv/opencv/tags)

## **本地交叉编译ffmpeg**

```bash
cd ffmpeg-6.1.1
mkdir build
./configure --enable-cross-compile --cc=aarch64-linux-gnu-gcc --cxx=aarch64-linux-gnu-g++ --target-os=linux --arch=arm64 --prefix=./install_ffmpeg --enable-shared --disable-static --strip=aarch64-linux-gnu-strip

```



```bash

./configure \
--enable-cross-compile \
--prefix=/home/topeet/workspace/opencv3_build/opencv3_install \
--cross-prefix=/usr/local/arm64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu- \
--arch=arm64 \
--target-os=linux \
--enable-gpl \
--extra-cflags=-fPIC \
--disable-filters \
--disable-encoders \
--enable-decoder=h264 --enable-parser=h264 --enable-demuxer=h264 \
--disable-asm  --enable-parsers --disable-debug --enable-ffmpeg --enable-shared --disable-static --disable-stripping --disable-doc --disable-yasm --disable-libx264
```



然后

```bash
make -j8
sudo make install
```

install完后会在指定目录下生成bin, include, lib, share四个目录，其中bin目录下会包含2个可执行文件ffmpeg和ffprobe, 执行此两个文件需要LD_LIBRARY_PATH指向动态库；include目录下包含8个ffmpeg模块的头文件；lib目录下包含生成的动态库和静态库；share目录包含了一些examples等文件；

```bash
cd ffmpeg/bin
file ffmpeg
```

会显示以下内容

```
ffmpeg: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, for GNU/Linux 3.7.0, BuildID[sha1]=bf4349873d8a351977e97dce9a2d6cf8dfb5aca4, stripped
```

基本编译成功

2. **接下来将这些交叉编译得到的文件拷贝至板端。**

注意不要直接scp或者远程工具拖过去，会导致lib中的动态库将的软连接丢失，导致的后面执行 `sudo ldconfig`命令出现如以下的报错。

> /sbin/ldconfig.real: /usr/local/ffmpeg/lib/libavfilter.so.9 is not a symbolic link

按照以下方法，

```bash
# 先zip压缩 . 添加-y参数 ,防止丢失软连接属性
zip -ry ffmpeg.zip /usr/local/ffmpeg/
# 然后拷贝过去
scp .. 或者远程工具直接拖过去，然后
# 然后解压缩，不用加额外参数
unzip ffmpeg
cd ffmpeg/lib
ls -all # 会看到软连接都在
# 这个时候的文件 直接cp -r 进行拷贝软连接都还在
```

3. **配置库文件路径**

```bash
# 将解压后的文件改放在/usr/local
cd /etc/ld.so.conf.d/
vim ffmpeg.conf # 添加ffmpeg 动态库配置文件
# 添加以下内容
/usr/local/ffmpeg/lib  
#保存，然后执行生效
sudo ldconfig
```

4. **配置环境变量**

```bash
sudo vim ~/.bashrc
# 添加以下
export PATH=$PATH:/usr/local/ffmpeg/bin
#
source ~/.bashrc
echo $PATH  # 可以看到ffmpeg 的bin目录已经被加入
```

5.检查是否安装成功

 1.此时在终端直接输入`ffmpeg`,可以看到ffmpeg的版本等信息。

此时ffmpeg就算安装成功了。

2.

```
cd /usr/local/ffmpeg/bin
ldd ffmpeg  # 可以看到ffmpeg的相关依赖库
```

ref:

ffmpeg 安装依赖的多个第三方库: https://blog.csdn.net/T__zxt/article/details/123424359

其他的一些ffmpeg的编译选项：

```bash
sudo cmake  -D CMAKE_BUILD_TYPE=RELEASE  -D CMAKE_C_COMPILER=aarch64-linux-gnu-gcc -D CMAKE_CXX_COMPILER=aarch64-linux-gnu-g++ -D BUILD_SHARED_LIBS=ON -D CMAKE_CXX_FLAGS=-fPIC -D CMAKE_C_FLAGS=-fPIC -D CMAKE_EXE_LINKER_FLAGS=-lpthread -ldl -D ENABLE_PIC=ON -D WITH_1394=OFF -D WITH_ARAVIS=OFF -D WITH_ARITH_DEC=ON -D WITH_ARITH_ENC=ON -D WITH_CLP=OFF -D WITH_CUBLAS=OFF -D WITH_CUDA=OFF -D WITH_CUFFT=OFF -D WITH_FFMPEG=ON -D WITH_GSTREAMER=ON -D WITH_GSTREAMER_0_10=OFF -D WITH_HALIDE=OFF -D WITH_HPX=OFF -D WITH_IMGCODEC_HDR=ON -D WITH_IMGCODEC_PXM=ON -D WITH_IMGCODEC_SUNRASTER=ON -D WITH_INF_ENGINE=OFF -D WITH_IPP=OFF -D WITH_ITT=OFF -D WITH_JASPER=ON -D WITH_JPEG=ON -D WITH_LAPACK=ON -D WITH_LIBREALSENSE=OFF -D WITH_NVCUVID=OFF -D WITH_OPENCL=OFF -D WITH_OPENCLAMDBLAS=OFF -D WITH_OPENCLAMDFFT=OFF -D WITH_OPENCL_SVM=OFF -D WITH_OPENEXR=OFF -D WITH_OPENGL=OFF -D WITH_OPENMP=OFF -D WITH_OPENNNI=OFF -D WITH_OPENNNI2=OFF -D WITH_OPENVX=OFF -D WITH_PNG=OFF -D WITH_PROTOBUF=OFF -D WITH_PTHREADS_PF=ON -D WITH_PVAPI=OFF -D WITH_QT=OFF -D WITH_QUIRC=OFF  -D WITH_TBB=OFF -D WITH_TIFF=ON -D WITH_VULKAN=OFF -D WITH_WEBP=ON -D WITH_XIMEA=OFF -D CMAKE_INSTALL_PREFIX=./install_ffmpeg  -D WITH_GTK=OFF -D WITH_GTK_2_X=OFF  ..

```



```bash
./configure --prefix=/usr/local/my/ffmpeg --enable-version3 --enable-libdrm --enable-rkmpp --enable-libx264 --enable-nonfree --enable-gpl
```



opencv编译选项

```bash
sudo cmake  -D CMAKE_BUILD_TYPE=RELEASE  -D CMAKE_C_COMPILER=aarch64-linux-gnu-gcc -D CMAKE_CXX_COMPILER=aarch64-linux-gnu-g++ -D BUILD_SHARED_LIBS=ON -D CMAKE_CXX_FLAGS=-fPIC -D CMAKE_C_FLAGS=-fPIC -D CMAKE_EXE_LINKER_FLAGS=-lpthread -ldl -D ENABLE_PIC=ON -D WITH_1394=OFF -D WITH_ARAVIS=OFF -D WITH_ARITH_DEC=ON -D WITH_ARITH_ENC=ON -D WITH_CLP=OFF -D WITH_CUBLAS=OFF -D WITH_CUDA=OFF -D WITH_CUFFT=OFF -D WITH_FFMPEG=ON -D WITH_GSTREAMER=ON -D WITH_GSTREAMER_0_10=OFF -D WITH_HALIDE=OFF -D WITH_HPX=OFF -D WITH_IMGCODEC_HDR=ON -D WITH_IMGCODEC_PXM=ON -D WITH_IMGCODEC_SUNRASTER=ON -D WITH_INF_ENGINE=OFF -D WITH_IPP=OFF -D WITH_ITT=OFF -D WITH_JASPER=ON -D WITH_JPEG=ON -D WITH_LAPACK=ON -D WITH_LIBREALSENSE=OFF -D WITH_NVCUVID=OFF -D WITH_OPENCL=OFF -D WITH_OPENCLAMDBLAS=OFF -D WITH_OPENCLAMDFFT=OFF -D WITH_OPENCL_SVM=OFF -D WITH_OPENEXR=OFF -D WITH_OPENGL=OFF -D WITH_OPENMP=OFF -D WITH_OPENNNI=OFF -D WITH_OPENNNI2=OFF -D WITH_OPENVX=OFF -D WITH_PNG=OFF -D WITH_PROTOBUF=OFF -D WITH_PTHREADS_PF=ON -D WITH_PVAPI=OFF -D WITH_QT=OFF -D WITH_QUIRC=OFF  -D WITH_TBB=OFF -D WITH_TIFF=ON -D WITH_VULKAN=OFF -D WITH_WEBP=ON -D WITH_XIMEA=OFF -D CMAKE_INSTALL_PREFIX=./install_ffmpeg  -D WITH_GTK=OFF -D WITH_GTK_2_X=OFF  ..
```

该编译选项，如果在板端执行，make到一半内存不足。

如果在本地进行交叉编译，还是有问题，Unknown argument -ldl 以及 去除 -ldl 后，出现 

>  Cannot generate a safe runtime search path for target opencv_perf_videoio
>   because there is a cycle in the constraint graph:



```bash
cmake  -D CMAKE_BUILD_TYPE=RELEASE  -D CMAKE_C_COMPILER=aarch64-linux-gnu-gcc -D CMAKE_CXX_COMPILER=aarch64-linux-gnu-g++ -D BUILD_SHARED_LIBS=ON -D CMAKE_CXX_FLAGS=-fPIC -D CMAKE_C_FLAGS=-fPIC -D CMAKE_EXE_LINKER_FLAGS=-lpthread -D ENABLE_PIC=ON -D WITH_1394=OFF -D WITH_ARAVIS=OFF -D WITH_ARITH_DEC=ON -D WITH_ARITH_ENC=ON -D WITH_CLP=OFF -D WITH_CUBLAS=OFF -D WITH_CUDA=OFF -D WITH_CUFFT=OFF -D WITH_FFMPEG=ON -D WITH_GSTREAMER=OFF -D WITH_GSTREAMER_0_10=OFF -D WITH_HALIDE=OFF -D WITH_HPX=OFF -D WITH_IMGCODEC_HDR=ON -D WITH_IMGCODEC_PXM=ON -D WITH_IMGCODEC_SUNRASTER=ON -D WITH_INF_ENGINE=OFF -D WITH_IPP=OFF -D WITH_ITT=OFF -D WITH_JASPER=ON -D WITH_JPEG=ON -D WITH_LAPACK=ON -D WITH_LIBREALSENSE=OFF -D WITH_NVCUVID=OFF -D WITH_OPENCL=OFF -D WITH_OPENCLAMDBLAS=OFF -D WITH_OPENCLAMDFFT=OFF -D WITH_OPENCL_SVM=OFF -D WITH_OPENEXR=OFF -D WITH_OPENGL=OFF -D WITH_OPENMP=OFF -D WITH_OPENNNI=OFF -D WITH_OPENNNI2=OFF -D WITH_OPENVX=OFFs -D WITH_PNG=OFF -D WITH_PROTOBUF=OFF -D WITH_PTHREADS_PF=ON -D WITH_PVAPI=OFF -D WITH_QT=OFF -D WITH_QUIRC=OFF  -D WITH_TBB=OFF -D WITH_TIFF=ON -D WITH_VULKAN=OFF -D WITH_WEBP=ON -D WITH_XIMEA=OFF -D CMAKE_INSTALL_PREFIX=./install_ffmpeg  -D WITH_GTK=ON -D WITH_GTK_2_X=OFF  -D BUILD_ZLIB=ON -D BUILD_JPEG=ON -D BUILD_WEBP=ON -D BUILD_TIFF=ON -D BUILD_JAVA=OFF -D BUILD_OPENCV_JAVA_BINDING_GENERATOR=OFF  -D WITH_PYTHON=OFF -D BUILD_OPENCV_PYTHON_TESTS=OFF -D OPENCV_PYTHON3_VERSION=OFF -D PYTHON2_EXECUTABLE=OFF  -D PYTHON3_EXECUTABLE=OFF -D PYTHON3_INCLUDE_DIR=OFF -D PYTHON3_NUMPY_INCLUDE_DIRS=OFF -D BUID_OPENCV_PYTHON_BINDINGS_GENERATOR=OFF -D OPENVJPEG_DIR=OFF -D OPENCV_EXTRA_MODULES_PATH=/home/sun/下载/opencv_contrib-4.8.0/modules ..
```



```
 -D BUILD_opencv_xfeatures2d=OFF -D BUILD_opencv_hdf=OFF -D BUID_OPENCV_FACE=OFF -D BUILD_OPENCV_STEREO=OFF -D BUILD_OPENCV_WECHAT_QRCODE=OFF -D BUILD_OPENCV_XOBJDETECT=OFF 
```



## opencv cmake 交叉编译命令

```bash
cd opencv-4.8.0
mkdir build && cd build
cmake \
-D CMAKE_BUILD_TYPE=RELEASE  \
-D CMAKE_C_COMPILER=aarch64-linux-gnu-gcc \
-D CMAKE_CXX_COMPILER=aarch64-linux-gnu-g++ \
-D BUILD_SHARED_LIBS=ON \
-D CMAKE_CXX_FLAGS=-fPIC \
-D CMAKE_C_FLAGS=-fPIC \
-D CMAKE_EXE_LINKER_FLAGS="-lpthread -ldl" \
-D ENABLE_PIC=ON \
-D WITH_1394=OFF \
-D WITH_ARAVIS=OFF \
-D WITH_ARITH_DEC=ON \
-D WITH_ARITH_ENC=ON \
-D WITH_CLP=OFF \
-D WITH_CUBLAS=OFF \
-D WITH_CUDA=OFF \
-D WITH_CUFFT=OFF \
-D WITH_FFMPEG=ON \
-D WITH_GSTREAMER=OFF \
-D WITH_GSTREAMER_0_10=OFF \
-D WITH_HALIDE=OFF \
-D WITH_HPX=OFF \
-D WITH_IMGCODEC_HDR=ON \
-D WITH_IMGCODEC_PXM=ON \
-D WITH_IMGCODEC_SUNRASTER=ON \
-D WITH_INF_ENGINE=OFF \
-D WITH_IPP=OFF \
-D WITH_ITT=OFF \
-D WITH_JASPER=ON \
-D WITH_LAPACK=ON \
-D WITH_LIBREALSENSE=OFF \
-D WITH_NVCUVID=OFF \
-D WITH_OPENCL=OFF \
-D WITH_OPENCLAMDBLAS=OFF \
-D WITH_OPENCLAMDFFT=OFF \
-D WITH_OPENCL_SVM=OFF \
-D WITH_OPENEXR=OFF \
-D WITH_OPENGL=OFF \
-D WITH_OPENMP=OFF \
-D WITH_OPENNNI=OFF \
-D WITH_OPENNNI2=OFF \
-D WITH_OPENVX=OFF \
-D WITH_PROTOBUF=OFF \
-D WITH_PTHREADS_PF=ON \
-D WITH_PVAPI=OFF \
-D WITH_QT=OFF \
-D WITH_QUIRC=OFF  \
-D WITH_TBB=OFF \
-D WITH_VULKAN=OFF \
-D WITH_XIMEA=OFF \
-D WITH_EIGEN=ON \
-D WITH_TIFF=OFF \
-D WITH_PNG=OFF \
-D WITH_JPEG=OFF \
-D WITH_WEBP=OFF \
-D CMAKE_INSTALL_PREFIX=../install_ffmpeg/  \
-D WITH_GTK=ON \
-D OPENCV_EXTRA_MODULES_PATH="../../opencv_contrib-4.8.0/modules" \
-D BUILD_ZLIB=ON \
-D ZLIB_INCLUDE_DIR="../3rdparty/zlib" \
-D OPENCV_GENERATE_PKGCONFIG=ON \
-D WITH_GTK_2_X=OFF  -D BUILD_ZLIB=ON -D BUILD_JPEG=ON -D BUILD_WEBP=ON -D BUILD_TIFF=ON -D BUILD_JAVA=OFF -D BUILD_OPENCV_JAVA_BINDING_GENERATOR=OFF  -D WITH_PYTHON=OFF -D BUILD_OPENCV_PYTHON_TESTS=OFF -D OPENCV_PYTHON3_VERSION=OFF -D PYTHON2_EXECUTABLE=OFF  -D PYTHON3_EXECUTABLE=OFF -D PYTHON3_INCLUDE_DIR=OFF -D PYTHON3_NUMPY_INCLUDE_DIRS=OFF -D BUID_OPENCV_PYTHON_BINDINGS_GENERATOR=OFF -D OPENVJPEG_DIR=OFF -D BUILD_opencv_features2d=OFF -D BUILD_opencv_xfeatures2d=OFF -D BUILD_opencv_freetype=OFF -D BUILD_opencv_gapi=OFF ..
```

OPENCV_GENERATE_PKGCONFIG，勾选上。这是生成.pc文件的选项

然后

```bash
make -j8  # 编译遇到很多很多问题
make install  # 指定安装路径会生成一些文件，拷贝到板端
```

修改一下lib/pkgconfig/opencv4.pc文件

修改prefix为 拷贝到的路径。

```
sudo vim /etc/ld.so.conf.d/opencv.conf 
#修改为 当前安装的lib路径
sudo ldconfig
```

整个安装过程没有报错，但是结果得到的opencv库无法读图读视频。

由于依赖gtk等三方库，而x86上不好交叉编译，所以决定直接板端编译。



## opencv交叉编译遇到的问题和暂时解决办法

- 关闭java相关

BUILD_JAVA=OFF -D BUILD_OPENCV_JAVA_BINDING_GENERATOR=OFF

- 关闭python相关

-D WITH_PYTHON=OFF -D BUILD_OPENCV_PYTHON_TESTS=OFF -D OPENCV_PYTHON3_VERSION=OFF -D PYTHON2_EXECUTABLE=OFF  -D PYTHON3_EXECUTABLE=OFF -D PYTHON3_INCLUDE_DIR=OFF -D PYTHON3_NUMPY_INCLUDE_DIRS=OFF -D BUID_OPENCV_PYTHON_BINDINGS_GENERATOR=OFF

- libopencv_imgcodecs.so 

```
[ 31%] Linking CXX shared library ../../lib/libopencv_imgcodecs.so
../../3rdparty/lib/liblibpng.a(pngrtran.c.o): In function `png_do_read_transformations':
pngrtran.c:(.text.png_do_read_transformations+0x16bc): undefined reference to `png_do_expand_palette_rgba8_neon'
pngrtran.c:(.text.png_do_read_transformations+0x1868): undefined reference to `png_riffle_palette_neon'
pngrtran.c:(.text.png_do_read_transformations+0x2e3c): undefined reference to `png_do_expand_palette_rgb8_neon'
../../3rdparty/lib/liblibpng.a(pngrutil.c.o): In function `png_read_filter_row':
pngrutil.c:(.text.png_read_filter_row+0xb0): undefined reference to `png_init_filter_functions_neon'
collect2: 错误： ld 返回 1
make[2]: *** [modules/imgcodecs/CMakeFiles/opencv_imgcodecs.dir/build.make:425：lib/libopencv_imgcodecs.so.4.6.0] 错误 1
make[1]: *** [CMakeFiles/Makefile2:4690：modules/imgcodecs/CMakeFiles/opencv_imgcodecs.dir/all] 错误 2
make: *** [Makefile:166：all] 错误 2
```

ref:https://www.yii666.com/blog/561477.html

将源码中的**/3rdparty/libpng/pngpriv.h**文件进行修改，将

```bash
# 注释掉131行
/* if (defined(__ARM_NEON__) || defined(__ARM_NEON)) && \ */
# 改为：
if defined(PNG_ARM_NEON) && (defined(__ARM_NEON__) || defined(__ARM_NEON)) && \
```



- 特征提取库

```
Consolidate compiler generated dependencies of target opencv_features2d
/usr/lib/x86_64-linux-gnu/libfreetype.so: error adding symbols: 文件格式错误
collect2: 错误： ld 返回 1
make[2]: *** [modules/freetype/CMakeFiles/opencv_freetype.dir/build.make:101：lib/libopencv_freetype.so.4.6.0] 错误 1
make[1]: *** [CMakeFiles/Makefile2:4474：modules/freetype/CMakeFiles/opencv_freetype.dir/all] 错误 2
make[1]: *** 正在等待未完成的任务....
```

-D BUILD_opencv_features2d=OFF -D BUILD_opencv_xfeatures2d=OFF -D 

- libopencv_freetype.so 一个中文库

```
[ 28%] Linking CXX shared library ../../lib/libopencv_freetype.so
/usr/lib/x86_64-linux-gnu/libfreetype.so: error adding symbols: 文件格式错误
collect2: 错误： ld 返回 1
make[2]: *** [modules/freetype/CMakeFiles/opencv_freetype.dir/build.make:101：lib/libopencv_freetype.so.4.6.0] 错误 1
make[1]: *** [CMakeFiles/Makefile2:4474：modules/freetype/CMakeFiles/opencv_freetype.dir/all] 错误 2
make[1]: *** 正在等待未完成的任务....
```

BUILD_opencv_freetype=OFF

- liblibpng.a

```
[ 28%] Linking C static library ../lib/liblibpng.a
[ 28%] Built target libpng
make: *** [Makefile:166：all] 错误 2

```

-D WITH_TIFF=OFF 
-D WITH_PNG=OFF 
-D WITH_JPEG=OFF 
-D WITH_WEBP=OFF

 -D BUILD_ZLIB=ON -D BUILD_JPEG=ON -D BUILD_WEBP=ON -D BUILD_TIFF=ON

-D OPENVJPEG_DIR=OFF

- libopencv_gapi.so

```
[ 60%] Linking CXX shared library ../../lib/libopencv_gapi.so
/usr/lib/x86_64-linux-gnu/libgstbase-1.0.so: error adding symbols: 文件格式错误
collect2: 错误： ld 返回 1
make[2]: *** [modules/gapi/CMakeFiles/opencv_gapi.dir/build.make:2007：lib/libopencv_gapi.so.4.6.0] 错误 1
make[1]: *** [CMakeFiles/Makefile2:4089：modules/gapi/CMakeFiles/opencv_gapi.dir/all] 错误 2
make: *** [Makefile:166：all] 错误 2
```

-D BUILD_opencv_gapi=OFF



- libgstbase-1.0.so 库格式错误，只能找到x86的

```
[ 51%] Linking CXX shared library ../../lib/libopencv_videoio.so
/usr/lib/x86_64-linux-gnu/libgstbase-1.0.so: error adding symbols: 文件格式错误
collect2: 错误： ld 返回 1
make[2]: *** [modules/videoio/CMakeFiles/opencv_videoio.dir/build.make:278：lib/libopencv_videoio.so.4.6.0] 错误 1
make[1]: *** [CMakeFiles/Makefile2:4095：modules/videoio/CMakeFiles/opencv_videoio.dir/all] 错误 2
make[1]: *** 正在等待未完成的任务....
[ 51%] Linking CXX shared library ../../lib/libopencv_datasets.so
[ 51%] Built target opencv_datasets
make: *** [Makefile:166：all] 错误 2
```

-D WITH_GSTREAMER=OFF

- 绘图的库找到gtk库的格式错误，需要arm 只有本地x86的

```
WITH_GTK=OFF[ 51%] Linking CXX shared library ../../lib/libopencv_highgui.so
/usr/lib/x86_64-linux-gnu/libgtk-3.so: error adding symbols: 文件格式错误
collect2: 错误： ld 返回 1
make[2]: *** [modules/highgui/CMakeFiles/opencv_highgui.dir/build.make:162：lib/libopencv_highgui.so.4.6.0] 错误 1
make[1]: *** [CMakeFiles/Makefile2:4220：modules/highgui/CMakeFiles/opencv_highgui.dir/all] 错误 2
make: *** [Makefile:166：all] 错误 2
```

-D WITH_GTK=OFF  然后顺利跳过

顺利编译成功

遇到的整个过程与[这个博客](https://blog.csdn.net/xidaoliang/article/details/124730226)最相似。



- 板端运行，报错：

```
terminate called after throwing an instance of 'cv::Exception'
  what():  OpenCV(4.6.0) /home/sun/softwares/opencv-4.6.0/modules/highgui/src/window.cpp:1250: error: (-2:Unspecified error) The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script in function 'cvNamedWindow'
```

说明highgui绘图库用不了，编译时还是需要gtk库。

​    cv::VideoCapture capture;    capture.open(camera_path);  不报错，但是无法打开视频文件。

此外cv::imread也无法读图，不知道为何。 读图读视频都没出现报错，只是读到的为空。



## 3568上编译opencv

ref:https://blog.csdn.net/dashuo0501/article/details/133985172

opencv4.8.0

```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE  \
             -D CMAKE_INSTALL_PREFIX=../install_opencv/ \
             -D CMAKE_C_COMPILER=aarch64-linux-gnu-gcc \
             -D CMAKE_CXX_COMPILER=aarch64-linux-gnu-g++ \
             -D BUILD_SHARED_LIBS=ON \
             -D CMAKE_CXX_FLAGS=-fPIC \
             -D CMAKE_C_FLAGS=-fPIC \
             -D CMAKE_EXE_LINKER_FLAGS=-lpthread -ldl \
             -D ENABLE_PIC=ON \
             -D WITH_1394=OFF \
             -D WITH_ARAVIS=OFF \
             -D WITH_ARITH_DEC=ON \
             -D WITH_ARITH_ENC=ON \
             -D WITH_CLP=OFF \
             -D WITH_CUBLAS=OFF \
             -D WITH_CUDA=OFF \
             -D WITH_CUFFT=OFF \
             -D WITH_FFMPEG=ON \
             -D WITH_GSTREAMER=ON \
             -D WITH_GSTREAMER_0_10=OFF \
             -D WITH_HALIDE=OFF \
             -D WITH_HPX=OFF \
             -D WITH_IMGCODEC_HDR=ON \
             -D WITH_IMGCODEC_PXM=ON \
             -D WITH_IMGCODEC_SUNRASTER=ON \
             -D WITH_INF_ENGINE=OFF \
             -D WITH_IPP=OFF \
             -D WITH_ITT=OFF \
             -D WITH_JASPER=ON \
             -D WITH_JPEG=ON \
             -D WITH_LAPACK=ON \
             -D WITH_LIBREALSENSE=OFF \
             -D WITH_NVCUVID=OFF \
             -D WITH_OPENCL=OFF \
             -D WITH_OPENCLAMDBLAS=OFF \
             -D WITH_OPENCLAMDFFT=OFF \
             -D WITH_OPENCL_SVM=OFF \
             -D WITH_OPENEXR=OFF \
             -D WITH_OPENGL=OFF \
             -D WITH_OPENMP=OFF \
             -D WITH_OPENNNI=OFF \
             -D WITH_OPENNNI2=OFF \
             -D WITH_OPENVX=OFF \
             -D WITH_PNG=OFF \
             -D WITH_PROTOBUF=OFF \
             -D WITH_PTHREADS_PF=ON \
             -D WITH_PVAPI=OFF \
             -D WITH_QT=OFF \
             -D WITH_QUIRC=OFF \
             -D WITH_TBB=OFF \
             -D WITH_TIFF=ON \
             -D WITH_VULKAN=OFF \
             -D WITH_WEBP=ON \
             -D WITH_XIMEA=OFF \
             -D WITH_GTK=ON -D WITH_GTK_2_X=OFF  ..
```

make期间出现报错：

```
error: ‘decoded_info’ was not declared in this scope
```

参考这个[patch](https://github.com/opencv/opencv/commit/e9414169a3824d075ad4939c11a97402ffc5cef1.patch)进行修改，重新make，编译通过

```
sudo make install
```

这时安装文件在install_opencv下，我将该文件移动到/usr/local下并改名为opencv。那么我的opencv 的安装位置为/usr/local/opencv 其下有bin, lib, include,share四个文件。

在配置cmakeLists时，设置路径

```cmake
set(OpenCV_DIR /usr/local/opencv/lib/cmake/opencv4/)
find_package(OpenCV REQUIRED)
```

此时编译运行opencv 会出现.so包无法找到的问题，需要将opencv相关的库文件配置到动态库路径中

```bash
sudo vim /etc/ld.so.conf.d/opencv.conf 
# 添加
/usr/local/opencv/lib
# 保存
# 然后
sudo ldconfig 
```

然后重新编译opencv项目文件，可成功读图读视频。

但是使用imshow报错：

```
OpenCV Error: Unspecified error (The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Carbon support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script) in cvNamedWindow, file /home/nick/.Apps/opencv/modules/highgui/src/window.cpp, line 516
terminate called after throwing an instance of 'cv::Exception'
  what():  /home/nick/.Apps/opencv/modules/highgui/src/window.cpp:516: error: (-2) The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Carbon support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script in function cvNamedWindow
```

ref:[here](https://stackoverflow.com/questions/28776053/opencv-gtk2-x-error-unspecified-error-the-function-is-not-implemented) 就是opencv编译时没有gtk库编译进去。发现其实早在cmake完时就提示了

```
-- Checking for module 'gtk+-3.0'
--   No package 'gtk+-3.0' found
-- Checking for module 'gtk+-2.0'
--   No package 'gtk+-2.0' found
...
--   GUI:                           NONE
--     GTK+:                        NO
--     VTK support:                 NO
```

这就无法出现show的界面窗口。

```
apt-get update
apt-get install libgtk3.0-dev pkg-config
# 如果WITH_GTK_2_X=ON,应该还要下gtk2.0推断的话
apt-get install libgtk2.0-dev
```

使用上面命令下载后再执行之前cmake命令

```
--   GUI:                           GTK3
--     GTK+:                        YES (ver 3.24.20)
--       GThread :                  YES (ver 2.64.6)
--       GtkGlExt:                  NO
--     VTK support:                 NO
```

可以看到其找到了gtk的库。



## 再次在3568上编译opencv  编译成静态库

```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE  \
             -D CMAKE_INSTALL_PREFIX=../install_static/ \
             -D CMAKE_C_COMPILER=aarch64-linux-gnu-gcc \
             -D CMAKE_CXX_COMPILER=aarch64-linux-gnu-g++ \
             -D BUILD_SHARED_LIBS=OFF \
             -D CMAKE_CXX_FLAGS=-fPIC \
             -D CMAKE_C_FLAGS=-fPIC \
             -D CMAKE_EXE_LINKER_FLAGS=-lpthread -ldl \
             -D ENABLE_PIC=ON \
             -D WITH_1394=OFF \
             -D WITH_ARAVIS=OFF \
             -D WITH_ARITH_DEC=ON \
             -D WITH_ARITH_ENC=ON \
             -D WITH_CLP=OFF \
             -D WITH_CUBLAS=OFF \
             -D WITH_CUDA=OFF \
             -D WITH_CUFFT=OFF \
             -D WITH_FFMPEG=ON \
             -D WITH_GSTREAMER=ON \
             -D WITH_GSTREAMER_0_10=OFF \
             -D WITH_HALIDE=OFF \
             -D WITH_HPX=OFF \
             -D WITH_IMGCODEC_HDR=ON \
             -D WITH_IMGCODEC_PXM=ON \
             -D WITH_IMGCODEC_SUNRASTER=ON \
             -D WITH_INF_ENGINE=OFF \
             -D WITH_IPP=OFF \
             -D WITH_ITT=OFF \
             -D WITH_JASPER=ON \
             -D WITH_JPEG=ON \
             -D WITH_LAPACK=ON \
             -D WITH_LIBREALSENSE=OFF \
             -D WITH_NVCUVID=OFF \
             -D WITH_OPENCL=OFF \
             -D WITH_OPENCLAMDBLAS=OFF \
             -D WITH_OPENCLAMDFFT=OFF \
             -D WITH_OPENCL_SVM=OFF \
             -D WITH_OPENEXR=OFF \
             -D WITH_OPENGL=OFF \
             -D WITH_OPENMP=OFF \
             -D WITH_OPENNNI=OFF \
             -D WITH_OPENNNI2=OFF \
             -D WITH_OPENVX=OFF \
             -D WITH_PNG=OFF \
             -D WITH_PROTOBUF=OFF \
             -D WITH_PTHREADS_PF=ON \
             -D WITH_PVAPI=OFF \
             -D WITH_QT=OFF \
             -D WITH_QUIRC=OFF \
             -D WITH_TBB=OFF \
             -D WITH_TIFF=ON \
             -D WITH_VULKAN=OFF \
             -D WITH_WEBP=ON \
             -D WITH_XIMEA=OFF \
             -D WITH_GTK=ON -D WITH_GTK_2_X=OFF  ..
```

## opencv交叉编译难点总结

- 编译选型设置问题

编译选项设置错误，会导致编译不成功或者成功却无法实现需要的功能。

- 编译时间长，且编译中途出现各种错误。

- 第三方依赖库需要交叉编译

在X86的Linux服务器上交叉编译很难解决模块依赖的问题，如果需要imshow 需要依赖GTK，需要处理视频又需要依赖ffmpeg gstream等库，都需要arm平台的库，本地可能只有x86平台库，这意味着需要在X86上对ffmpeg 或者GTK的库在本地交叉编译，再在编译时将交叉编译好第三方库配置进去。





# Q&A

Q:我现在用我的电脑交叉编译一个项目要在3588盒子上跑， 该项目依赖opencv库， 而我编译的opencv库又依赖ffmpeg和gtk的库。

我在cmakelist里面把 opencvlib包含进去了，编译的时候找不到libgtk.so 还有ffmpeg 里面的libavcodec.so那些包，我该怎么把它们包含进来













