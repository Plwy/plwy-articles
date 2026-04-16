list:

- clashy配置

- chrome下载，账号同步

- 百度网盘下载，账号同步

- wechat下载 [微信 Linux 版](https://linux.weixin.qq.com/)

- vscode下载，插件

  python,remote-ssh,gitlen,github copilot,c++,cmake

- fcitx5输入法 (sogou不好用卸载了)

- frameshot [download](https://flameshot.org/#download)

- xterminal [download](https://www.terminal.icu/)

- miniconda

- ffmpeg

- git

- file-roller

- build-essential编译相关

- cuda

## 常用软件

官网下载deb包安装

```bash
# chrome
sudo dpkg -i google-chrome-stable_current_amd64.deb
# vscode
sudo dpkg -i code_1.96.4-1736991114_amd64.deb 
# baidudisk
sudo dpkg -i baidunetdisk_4.17.7_amd64.deb 
# typora
sudo dpkg -i typora_1.10.8_amd64.deb
# wechat
sudo dpkg -i WeChatLinux_x86_64.deb
# wps
sudo dpkg -i wps-office_12.1.0.17900_amd64.deb 
# xterminal
sudo dpkg -i XTerminal-3.15.0-linux-amd64.deb
```

## apt下载一些必要的工具

```bash
# 使用ifconfig命令
sudo apt install net-tools 
sudo apt install curl
sudo apt install vim 
sudo apt install git
sudo apt install ffmpeg
# 编译相关 包括gcc g++ make等
sudo apt install build-essential
sudo apt install cmake
# 归档工具file-roller
sudo apt install file-roller
# vlc 视频播放软件直接在软件商店下载
```

## clash下载配置

下载位置：[clash-verge](https://github.com/zzzgydi/clash-verge/releases)

[clash-verge-rev](https://github.com/clash-verge-rev/clash-verge-rev/releases)也可以。

```
sudo chmod +x clash-verge_1.3.8_amd64.AppImage 
```

clash界面上，添加机场的配置,可以在代理下看到节点信息， 端口号默认设置为7890.

pc上， 设置->网络->代理， 设置为手动，然后

http代理，https代理：url设置为http://127.0.0.1, 端口号设置为7890.

Socks主机：url设置为socks5://127.0.0.1, 端口号设置为7891.

## 输入法下载配置

sogoupinyin狗屎。安装后各种问题。无法切换输入法，中英无法切换，有的软件无法打出中文，有的软件莫名输入时显示多余的字符等。

卸载了fcitx4, 安装了fcitx5

```bash
# 卸载
sudo apt-get remove --purge fcitx
sudo apt autoremove  fcitx
# 安装
sudo apt update
sudo apt install fcitx5 
sudo apt install fcitx5-pinyin
sudo apt install fcitx5-configtool fcitx5-chinese-addons
```

配置输入法框架 fcitx5 的环境变量，确保在使用不同的桌面应用程序（尤其是基于 GTK 和 Qt 的程序）时能够正确调用 fcitx5 输入法。

```bash
echo 'export GTK_IM_MODULE=fcitx5' >> ~/.profile
echo 'export QT_IM_MODULE=fcitx5' >> ~/.profile
echo 'export XMODIFIERS="@im=fcitx5"' >> ~/.profile
```

在fcitx设置中将 拼音和 键盘-英语 拖入输入法栏目。

使用ctrl+space 切换中英输入即可。



## MIniconda

[下载方式](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions)

照着文档执行即可

```bash
 wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
 bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
 source ~/miniconda3/bin/activate
 conda init --all
```



### 设置conda源

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --show channels
conda config --set show_channel_urls yes
```

### pip 源

设置清华源

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```



## cuda安装

cuda toolkit安装

1.提前装好 编译工具,否则提示这个

>  Failed to verify gcc version. See log at /var/log/cuda-installer.log for details.

2.nvidia官网下载

[](https://developer.nvidia.com/cuda-12-3-2-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu)

根据系统架构和os版本

Linux->x86_64->ubuntu->22.04

下载runfile

3.安装

```
sudo bash cuda_12.3.2_545.23.08_linux.run
```

continue->accept ->选中toolkit 其他driver doc都取消。

4.环境变量

`vim ~/.bashrc`添加

```bash
export PATH=/usr/local/cuda-12.3/bin:${PATH}
export LD_LIBRARY_PATH=/usr/local/cuda-12.3/lib64:${LD_LIBRARY_PATH}
```

5.检查

```
nvcc -V
```

### cudnn

不同版本的安装地址:https://developer.nvidia.com/cudnn-archive

tar包的安装。[tar包下载](https://developer.download.nvidia.com/compute/cudnn/redist/cudnn/linux-x86_64/)

```
tar -xvf cudnn-linux-x86_64-8.9.7.29_cuda12-archive.tar.xz
```

将include和lib下的文件全拷贝到cuda的include和lib目录下。

```bash
# 加 -P 保留软连接
cd cudnn-linux-x86_64-8.9.7.29_cuda12-archive/include
sudo cp -P * /usr/local/cuda/include
cd cudnn-linux-x86_64-8.9.7.29_cuda12-archive/lib
sudo cp -P * /usr/local/cuda/lib64
```



deb包安装

```bash
wget https://developer.download.nvidia.com/compute/cudnn/9.11.1/local_installers/cudnn-local-repo-ubuntu2404-9.11.1_1.0-1_amd64.deb
sudo dpkg -i cudnn-local-repo-ubuntu2404-9.11.1_1.0-1_amd64.deb
sudo cp /var/cudnn-local-repo-ubuntu2404-9.11.1/cudnn-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cudnn
```



12+的cuda ,onnxruntime-gpu需要9.0以上。

### Tensorrt

[Tensorrt官方安装指南](https://docs.nvidia.com/deeplearning/tensorrt/latest/installing-tensorrt/installing.html)

下载安装：

直接到https://developer.nvidia.com/tensorrt/download/10x，选择[TensorRT 10.13 GA for Linux x86_64 and CUDA 12.0 to 12.9 TAR Package](https://developer.nvidia.com/downloads/compute/machine-learning/tensorrt/10.13.0/tars/TensorRT-10.13.0.35.Linux.x86_64-gnu.cuda-12.9.tar.gz)  下载tar包 。6.5G

然后 参考`Tar File Installation`部分文档，

解压， 将解压后的lib库路径添加到环境变量

```
tar -xvf TensorRT-10.13.0.35.Linux.x86_64-gnu.cuda-12.9.tar.gz 
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:~/TensorRT-10.13.0.35/lib
```

tensorrt的tar包下还有python的wheel安装包，还有运行样例。





**结：**

或者根据自己的需求，参照官方文档，`apt install`特定的库

>  也可以直接用apt install 安装cuda和cudnn。

**目前使用组合：**

**cuda驱动最新版本**

**cuda12.3**

**cudnn 8.9.7**

**tensorrt 10.13.0**



## Opencv安装

https://github.com/opencv/opencv/tags 下载

使用cmake_gui进行编译选择

```
sudo apt install cmake-qt-gui
cmake-gui
```

对不需要的模块取消勾选。没特殊必要直接默认就好。

配置`OPENCV_EXTRA_MODULES_PATH` 为`~/opencv_contrib-4.12.0/modules`。然后generate

```bash
cd opencv-4.12.0/build
make -j12  
sudo make install
```



## JAVA JDK安装

需要开发jni接口，安装jdk库

```bash
sudo apt update
sudo apt install openjdk-11-jdk
```

装完检查

```bash
$ java -version
openjdk version "11.0.28" 2025-07-15
OpenJDK Runtime Environment (build 11.0.28+6-post-Ubuntu-1ubuntu124.04.1)
OpenJDK 64-Bit Server VM (build 11.0.28+6-post-Ubuntu-1ubuntu124.04.1, mixed mode, sharing)
$ javac -version
javac 11.0.28

```



## Docker安装

### [ubuntu docker engine 安装](https://docs.docker.com/desktop/setup/install/linux/)

1.添加GPG key

2.添加apt源

3.`apt install` docker相关

可直接创建`run.sh`脚本，添加内容：

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

```

### [docker去掉sudo权限的方法](https://zhuanlan.zhihu.com/p/484171630)

默认情况下，只有 root 用户和 docker 组的成员可以访问 Docker 引擎。需要将当前用户添加到docker组。

```bash
# 查看docker组下成员
sudo cat /etc/group | grep docker
# 创建docker组，(默认是有docker组) 
sudo groupadd docker 
# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER
# 重新加载用户组权限
newgrp docker
# 验证生效
docker info
```



### nvidia-container-toolkit安装

[下载方法](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

照做

1.

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

2.

```bash
sudo apt-get update
export NVIDIA_CONTAINER_TOOLKIT_VERSION=1.17.4-1
  sudo apt-get install -y \
      nvidia-container-toolkit=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
      nvidia-container-toolkit-base=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
      libnvidia-container-tools=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
      libnvidia-container1=${NVIDIA_CONTAINER_TOOLKIT_VERSION}
```



安装完了配置docker，然后重启docker

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```



## .AppImage添加到应用菜单

如何在应用中打开，如何配置图标。

1.

下载.AppImage，添加可执行权限

```
chmod +x Cherry-Studio-1.4.0-x86_64.AppImage
```

下载一个应用图标图片，最好是.png

2.

配置`.desktop`文件

主要Icon 和Exec部分

以下是一个Clashy.desktop文件：

```
#!/usr/bin/env xdg-open
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Name=clash-verge
GenericName=clash-verge
Comment=clash
Exec=绝对路径/Clashy/clash-verge_1.3.8_amd64.AppImage
Icon=绝对路径/Clashy/clashverge-300.png
Terminal=false
Type=Application
Categories=Network;
```

3.

将配置好的`.desktop`文件，拷贝到`/usr/share/applications/`目录下。再打开应用，可以看到图标生效了。

```bash
sudo cp ~/softwares/Clashy/Clashy.desktop /usr/share/applications/

```

