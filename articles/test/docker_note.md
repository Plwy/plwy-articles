# Docker

## docker 命令

包含命令及对应参数解释，以及使用过的实际命令例子。

**docker run：**创建一个新的容器并运行一个命令

参数解释：https://docs.docker.com/engine/reference/run/

- **-a stdin:** 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；

- **-d:** 后台运行容器，并返回容器ID；

- **-i:** 以交互模式运行容器，通常与 -t 同时使用；

- **-P:** 随机端口映射，容器内部端口**随机**映射到主机的端口

- **-p:** 指定端口映射，格式为：**主机(宿主)端口:容器端口**

- **-t:** 为容器重新分配一个伪输入终端，通常与 -i 同时使用；

- **--name="nginx-lb":** 为容器指定一个名称；

- **--dns 8.8.8.8:** 指定容器使用的DNS服务器，默认和宿主一致；

- **--dns-search example.com:** 指定容器DNS搜索域名，默认和宿主一致；

- **-h "mars":** 指定容器的hostname；

- **-e username="ritchie":** 设置环境变量；

- **--env-file=[]:** 从指定文件读入环境变量；

- **--cpuset="0-2" or --cpuset="0,1,2":** 绑定容器到指定CPU运行；

- **-m :**设置容器使用内存最大值；

- **--net="bridge":** 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；

- **--link=[]:** 添加链接到另一个容器；

- **--expose=[]:** 开放一个端口或一组端口；

- **--volume , -v:** 绑定一个卷

- --ipc="MODE"  : 设置容器的 IPC 模式

- **--rm**

  在Docker容器退出时，默认容器内部的文件系统仍然被保留，以方便调试并保留用户数据。但是，对于foreground容器，由于其只是在开发调试过程中短期运行，其用户数据并无保留的必要，因而可以在容器启动时设置--rm选项，这样在容器退出时就能够自动清理容器内部的文件系统。


eg:

```bash
#使用镜像 nginx:latest，以后台模式启动一个容器,将容器的 80 端口映射到主机的 80 端口,主机的目录 /data 映射到容器的 /data。
docker run -p 80:80 -v /data:/data -d nginx:latest
#使用镜像nginx:latest以交互模式启动一个容器,在容器内执行/bin/bash命令
docker run -it nginx:latest /bin/bash

# get image
docker pull nvcr.io/nvidia/pytorch:21.08-py3

# gpu run
# 通过选项 --gpus all 使用所有的GPU资源。
#通过 --gpus '"device=0,2"' 使用指定的GPU设备
docker run --name mil_od_infer --gpus all -it -v /home/data/1_proj:/workspace --shm-size=64g nvcr.io/nvidia/pytorch:21.08-py3
# rm设置容器退出即被清理
docker run --rm -p 6511:6511 xx/xxx:v1
```



**docker build** 命令用于使用 Dockerfile 创建镜像。

- **--build-arg=[] :**设置镜像创建时的变量；
- **--cpu-shares :**设置 cpu 使用权重；
- **--cpu-period :**限制 CPU CFS周期；
- **--cpu-quota :**限制 CPU CFS配额；
- **--cpuset-cpus :**指定使用的CPU id；
- **--cpuset-mems :**指定使用的内存 id；
- **--disable-content-trust :**忽略校验，默认开启；
- **-f :**指定要使用的Dockerfile路径；
- **--force-rm :**设置镜像过程中删除中间容器；
- **--isolation :**使用容器隔离技术；
- **--label=[] :**设置镜像使用的元数据；
- **-m :**设置内存最大值；
- **--memory-swap :**设置Swap的最大值为内存+swap，"-1"表示不限swap；
- **--no-cache :**创建镜像的过程不使用缓存；
- **--pull :**尝试去更新镜像的新版本；
- **--quiet, -q :**安静模式，成功后只输出镜像 ID；
- **--rm :**设置镜像成功后删除中间容器；
- **--shm-size :**设置/dev/shm的大小，默认值是64M；
- **--ulimit :**Ulimit配置。
- **--squash :**将 Dockerfile 中所有的操作压缩为一层。
- **--tag, -t:** 镜像的名字及标签，通常 name:tag 或者 name 格式；可以在一次构建中为一个镜像设置多个标签。
- **--network:** 默认 default。在构建期间设置RUN指令的网络模式

```bash
# 指定镜像名称为detect5000/yolov5-flask
# 最后的.代表着将所有内容打包成镜像
docker build --tag zsl/yolov5-flask .
# 镜像更名
docker tag 原始名 zsl/yolov5-flask
```

**docker start** :启动一个或多个已经被停止的容器

**docker stop** :停止一个运行中的容器

**docker restart** :重启容器

```bash
-s :向容器发送一个信号
docker kill -s KILL mynginx
```

**docker rm** :删除容器

- **-f :**通过 SIGKILL 信号强制删除一个运行中的容器。
- **-l :**移除容器间的网络连接，而非容器本身。
- **-v :**删除与容器关联的卷。

```bash
# 强制删除容器 db01、db02：
docker rm -f db01 db02
# 删除所有已经停止的容器：
docker rm $(docker ps -a -q)
```

**docker pause** :暂停容器中所有的进程。

**docker unpause** :恢复容器中所有的进程。

**docker create ：**创建一个新的容器但不启动它

**docker exec ：**在运行的容器中执行命令.允许我们与容器内的应用程序进行交互，并在容器中运行命令行工具、脚本或其他操作.

```bash
# 通过 exec 命令对指定的容器执行 bash
docker exec -it 9df70f9a0714 /bin/bash
```

**docker inspect :** 获取容器/镜像的元数据。

- **-f :**指定返回值的模板文件。
- **-s :**显示总的文件大小。
- **--type :**为指定类型返回JSON。

```bash
# 获取镜像mysql:5.6的元信息
docker inspect mysql:5.6
```

**docker top :**查看容器中运行的进程信息，支持 ps 命令参数。

**docker attach :**连接到正在运行中的容器。

**docker logs :** 获取容器的日志

- **-f :** 跟踪日志输出
- **--since :**显示某个开始时间的所有日志
- **-t :** 显示时间戳
- **--tail :**仅列出最新N条容器日志



**docker stats :** 显示容器资源的使用情况，包括：CPU、内存、网络 I/O 等。

**docker commit :**从容器创建一个新的镜像。

- **-a :**提交的镜像作者
- **-c :**使用Dockerfile指令来创建镜像；
- **-m :**提交时的说明文字；
- **-p :**在commit时，将容器暂停。

```bash
# demo
docker commit -a "runoob.com" -m "my apache" a404c6c174a2  mymysql:v1 
# commit
docker commit -a "zsl" -m "yolov7 train" 033297dd73c2 mil_od_train:v1.0
```

**docker cp :**用于容器与主机之间的数据拷贝。

```
docker cp /www/runoob 96f7f14e99ab:/www/
```

**docker pull :** 从镜像仓库中拉取或者更新指定镜像

**docker push :** 将本地的镜像上传到镜像仓库,要先登陆到镜像仓库

**docker images :** 列出本地镜像。

**docker rmi :** 删除本地一个或多个镜像。

- **-f :**强制删除；

```
# 强制删除本地镜像 runoob/ubuntu:v4。
docker rmi -f runoob/ubuntu:v4
```

**docker tag :** 标记本地镜像，将其归入某一仓库。

```bash
 # 将镜像ubuntu:15.10标记为 runoob/ubuntu:v3 镜像。
 docker tag ubuntu:15.10 runoob/ubuntu:v3
```

**docker history :** 查看指定镜像的创建历史。

**docker save :** 将指定镜像保存成 tar 归档文件。

- **-o :**输出到的文件。

```bash
# 将镜像 runoob/ubuntu:v3 生成 my_ubuntu_v3.tar 文档
docker save -o my_ubuntu_v3.tar runoob/ubuntu:v3

# 打包一个或者多个image
docker save -o images.tar postgres:9.6 mongo:3.4
```

**docker load :** 导入使用 [docker save](https://www.runoob.com/docker/docker-save-command.html) 命令导出的镜像。

- **--input , -i :** 指定导入的文件，代替 STDIN。
- **--quiet , -q :** 精简输出信息。

**docker export :**将文件系统作为一个tar归档文件导出到STDOUT。

- **-o :**将输入内容写到文件。

```bash
# 将id为a404c6c174a2的容器按日期保存为tar文件。
docker export -o mysql-`date +%Y%m%d`.tar a404c6c174a2
```

**docker import :** 从归档文件中创建镜像。

- **-c :**应用docker 指令创建镜像；
- **-m :**提交时的说明文字；

**docker info**：容器系统信息显示

```bash
[root@docker-slave3 ~]# docker info

Client:
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.10.4
    #使用 BuildKit 构建镜像。该命令支持--platform 参数可以同时构建支持多种系统架构的 Docker 镜像
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx    # 
  compose: Docker Compose (Docker Inc.)
    Version:  v2.17.2
    #使用 Dockerfile 定义应用程序的环境。
    #使用 docker-compose.yml 定义构成应用程序的服务，这样它们可以在隔离环境中一起运行。
	#最后，执行 docker-compose up 命令来启动并运行整个应用程序。
    Path:     /usr/libexec/docker/cli-plugins/docker-compose
  scan: Docker Scan (Docker Inc.)
    Version:  v0.23.0
    # 镜像漏洞扫描，扫描本地镜像是否存在漏洞软件。
    Path:     /usr/libexec/docker/cli-plugins/docker-scan

Containers: 45                  #容器的数量                                   
 Running: 44                    #正在运行的数量
 Paused: 0                      #暂停的数量
 Stopped: 1                     #已经停止的数量
Images: 264                     #镜像数量
Server Version: 1.12.5                   #docker server的版本
Storage Driver: devicemapper             #存储驱动程序
 Pool Name: docker-253:0-537427328-pool  #pool name的值根据Data file的模式改变      # direct-lvm 模式（Pool Name 为 docker-thinpool ）
 Pool Blocksize: 65.54 kB                #pool块大小
 Base Device Size: 10.74 GB              #基本存储大小
 Backing Filesystem: xfs                 #支持的文件系统
 Data file: /dev/loop0                   #使用的模式为loop-lvm        生产中不推荐使用（loop-lvm性能比较差）         使用 direct-lvm 模式（配置过程在最后面）
 Metadata file: /dev/loop1               #元数据文件位置
 Data Space Used: 86.78 GB               #数据使用的空间 direct-lvm 模式 direct-lvm 模式
 Data Space Total: 107.4 GB              #数据的总空间
 Data Space Available: 20.6 GB           #数据的可用空间
 Metadata Space Used: 159.8 MB           #元数据使用的空间
 Metadata Space Total: 2.147 GB          #元数据的总空间
 Metadata Space Available: 1.988 GB      #元数据的可用空间
 Thin Pool Minimum Free Space: 10.74 GB  # Thin pool(瘦供给池)的最小可用空间    *下面有瘦供给的解释    
 Udev Sync Supported: true                
 Deferred Removal Enabled: false
 Deferred Deletion Enabled: false
 Deferred Deleted Device Count: 0
 Data loop file: /var/lib/docker/devicemapper/devicemapper/data        #数据loop文件的位置
 WARNING: Usage of loopback devices is strongly discouraged for production use. Use `--storage-opt dm.thinpooldev` to specify a custom block storage device.            #警告信息
 Metadata loop file: /var/lib/docker/devicemapper/devicemapper/metadata    #元数据loop文件的位置
 Library Version: 1.02.135-RHEL7 (2016-09-28)
Logging Driver: json-file        
Cgroup Driver: cgroupfs
Plugins:                                    #插件            
 Volume: local
 Network: host null bridge overlay
Swarm: inactive
Runtimes: runc
Default Runtime: runc
Security Options: seccomp                    #内核安全组件
Kernel Version: 3.10.0-514.el7.x86_64        #内核版本
Operating System: CentOS Linux 7 (Core)      #操作系统
OSType: linux                                #操作系统类型
Architecture: x86_64                         #系统架构
CPUs: 4                                      #CPU数
Total Memory: 30.96 GiB                      #总空间
Name: docker-slave3.ctrm                     #主机名
ID: POZH:PSTG:ULR2:S75Y:OW57:ETGA:Z7RU:WEQA:VGNE:4JMJ:PJ3N:LXZW
Docker Root Dir: /var/lib/docker              #docker根目录
Debug Mode (client): false                    #调试模式（client）
Debug Mode (server): false                    #调试模式（server）
Registry: https://index.docker.io/v1/         #镜像仓库
Insecure Registries:                          #非安全镜像仓库
 15.116.20.134:5000
 15.116.20.104:80
 15.116.20.115:80
 127.0.0.0/8
```

## docker常用命令

```bash
# 列出所有镜像
docker images 
# 列出所有正在运行的容器
docker ps -a
# 拉取一个镜像
docker pull nvidia/cuda:12.6.0-cudnn-devel-ubuntu20.04
# 删除镜像 两个命令都可以
docker image rm image_id
docker rmi image_id
# 删除容器
docker rm -f container_id
# 查看镜像详细信息
docker inspect image_id
# 启动/停止容器
docker start contrainer_id
docker stop contrainer_id
# 运行一个容器
docker run --name container_name --gpus all -it nvidia/cuda:12.6.0-cudnn-devel-ubuntu20.04
# 从当前容器创建一个新镜像
docker commit -a "myname" -m "verbose"  contrainer_id image_name
# 镜像打包为tar文件
docker save -o test.tar test:v1
# load加载打包的镜像
docker load -i test.tar
```



## docker file 常用指令

```bash
FROM             # 基础镜像，一切从这里开始构建
MAINTAINER        # 镜像是谁写的， 姓名+邮箱
RUN             # 镜像构建的时候需要运行的命令
ADD             # 步骤，tomcat镜像，这个tomcat压缩包！添加内容 添加同目录
WORKDIR         # 镜像的工作目录
VOLUME             # 挂载的目录
EXPOSE             # 暴露端口配置  和我们的-p一样的
CMD         # 指定这个容器启动的时候要运行的命令，只有最后一个会生效，可被替代。
ENTRYPOINT         # 指定这个容器启动的时候要运行的命令，可以追加命令
ONBUILD # 当构建一个被继承DockerFile这个时候就会运行ONBUILD的指令，触发指令。
COPY             # 类似ADD，将我们文件拷贝到镜像中
ENV             # 构建的时候设置环境变量
```

CMD类似于 RUN 指令，用于运行程序，但二者运行的时间点不同:

- CMD 在docker run 时运行。
- RUN 是在 docker build。

demo1：

```dockerfile
FROM python:3.7-slim-buster #引入python环境

RUN apt-get update  
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 5000

CMD ["python", "webapp.py"]
```

这样生成的镜像，在创建容器挂载该镜像并运行时会直接运行CMD命令。

## docker镜像打包过程记录

### docker镜像打包内网训练

当前任务：需要到内网电脑的服务器上进行模型训练。本地外网电脑打包好docker镜像并上传到内网服务器用于训练。

```bash
# 拉取镜像用于训练
docker pull nvcr.io/nvidia/pytorch:21.08-py3

# run
# 设置容器名， 使用gpu, 映射路径， 映射端口， 设置共享内存大小
docker run --name mil_od2 --gpus all -it -v /home/sun/zsl_workspace/mil_detect_proj:/workspace -p 8080:6006 --shm-size=64g nvcr.io/nvidia/pytorch:21.08-py3

# 进入容器进行操作
docker exec -it mil_od2 /bin/bash

# 提交当前容器，将当前容器做成一个镜像
## docker commit -a 作者名 -m 镜像备注 容器ID 镜像名：tag名
docker commit -a "zsl" -m "yolov7 train" 033297dd73c2 mil_od_train:v1.0

# 将当前镜像导出，保存为一个.tar文件
docker save -o mil_od_train.tar mil_od_train:v1.0

# 将.tar文件拷贝到另一台电脑，然后使用load加载， 将保存的镜像移植过来
docker load -i mil_od_train.tar

# 将容器导出，保存为一个.tar文件
docker export -o mil_od_export.tar 19548a2b8e4
# 通过import导入，生成一个镜像
docker import mil_od_export.tar mil_od_export:v1.0 
```

基本流程：

1.编写dockerfile ， 包含基础镜像， 工作路径， 依赖包。

2.docker build .. 根据dockerfile 创建镜像。

3.docker run -it  .. 从该镜像启动容器。 

4.python xx.py 运行程序。

5.docker cp ..将运行结果拷贝出来。

6.docker export ..导出容器

7.docker import .. 导出的包拷贝到其他设备上，容器导入即可使用

8.docke start .. 启动 docker exec -it  ..进入



### docker save 和docker export

ref：https://blog.csdn.net/liukuan73/article/details/78089138

用户既可以使用 docker load 来导入镜像存储文件到本地镜像库，也可以使用 docker import 来导入一个容器快照到本地镜像库。这两者的区别在于容器快照文件将丢弃所有的历史记录和元数据信息（即仅保存容器当时的快照状态），而镜像存储文件将保存完整记录，体积也要大。此外，从容器快照文件导入时可以重新指定标签等元数据信息。

 docker save可以打包一个或者多个镜像，然后可使用docker load导入这些镜像。

 **docker save的应用场景是，如果你的应用是使用docker-compose.yml编排的多个镜像组合，但你要部署的客户服务器并不能连外网。这时，你可以使用docker save将用到的镜像打个包，然后拷贝到客户服务器上使用docker load载入。**

docker export是用来将container的文件系统进行打包的。

```bash
# 将一个container导出为文件。
docker export -o postgres-export.tar postgres

# 将export的文件 导入，导入后会成为一个镜像，可以为该镜像指定新名称
# 如果本地镜像库中已经存在同名的镜像，则原有镜像的名称将会被剥夺，赋给新的镜像。原有镜像将成为孤魂野鬼，只能通过IMAGE ID进行操作。
docker import postgres-export.tar postgres:latest
```

**docker export的应用场景主要用来制作基础镜像，比如你从一个ubuntu镜像启动一个容器，然后安装一些软件和进行一些设置后，使用docker export保存为一个基础镜像。然后，把这个镜像分发给其他人使用，比如作为基础的开发环境**



### docker镜像打包部署

#### dockerfile打包镜像

```dockerfile
FROM nvidia/cuda:11.2.2-cudnn8-devel-ubuntu18.04
WORKDIR /mil_server_restruct
ADD . /mil_server_restruct
# COPY ./resnet50-19c8e357.pth /root/.cache/torch/hub/checkpoints/resnet50-19c8e357.pth

# RUN chmod 777 /tmp
RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com A4B469963BF863CC
# 删除nvidia更新源以避免apt update失败，安装python3-pip会同时安装python3
RUN mv /etc/apt/sources.list.d /etc/apt/sources.list.d_bak
RUN rm -rf /etc/apt/sources.list.d && apt update
RUN  apt-get install -y python3.7 
# 建立python软连接到python3，以兼容使用python运行命令的情况
RUN ln -s /usr/bin/python3.7 /usr/bin/python
RUN apt-get install -y curl
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN apt-get install -y python3-distutils
RUN python get-pip.py -i https://pypi.tuna.tsinghua.edu.cn/simple

# RUN apt install -y libgl1-mesa-glx 
# RUN apt-get install -y libglib2.0-dev 
# RUN apt-get install libglib2.0-dev

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install packet/torch-1.10.0+cu111-cp37-cp37m-linux_x86_64.whl  # 所需依赖，有网环境会自动下载
RUN pip install packet/torchvision-0.11.0+cu111-cp37-cp37m-linux_x86_64.whl
# RUN pip install /packet/torchaudio-0.10.0+cu111-cp37-cp37m-linux_x86_64.whl

CMD ["python", "server.py"]
```

> 1.**关于WORKDIR和ADD:**
>
> 部署时候的容器工作路径和宿主机项目目录的关系。
>
> ```dockerfile
> WORKDIR /mil_server_restruct   # 在容器的根目录创建一个名为..的文件夹
> ADD . /mil_server_restruct # 将dockerfile 当前目录下的文件全部拷贝到 容器中 /mil_server_restruct 文件夹下。
> ```
> 2. **服务器上的opencv-python的安装**
> 需要使用`pip install opencv-python-headless`
> 否则运行是会报错，缺失一些显示需要的包。如：libgl1-mesa-glx  libglib2.0-dev  libglib2.0-dev等
> 

通过dockerfile构建，并打包镜像。
```bash
docker build -t mil_od_deploy:v1.0 .
docker save mil_od_deploy:v1.0 -o mil_od_deploy.tar
```



**修改镜像的名字和tag**

save打包时，最好带上镜像名和tag号，如果直接使用imageID打包，在load时会出现导入的镜像名和tag为`none`的情况，可使用docker tag进行改名

```bash
#docker tag 【镜像ID】【镜像名称】:【tag版本信息】 
docker tag 4157de9bccb1 mil_od_deploy:v1.0
```

### 关于一个项目一个镜像还是多个项目一个镜像的问题

**项目需要jdk, mysql, redis, nginx这四个依赖。那么，是应该把四个依赖各自放在一个docker镜像中，并把jar包放在jdk所在镜像中，还是应该用一个centOS镜像，在dockerfile中去yum这些依赖并配置？**

docker设计的就是一个容器跑一个进程服务

为了方便维护，要放在不通容器中，因为他们4个所依赖的环境也可能不同，要避免改动1个影响其他3个。

为了方便操作，可以写在同一个docker-compose脚本中，一同启动。



## docker run 和nvidia-docker run

与docker版本有关，好像是19.0之前的老版本docker 需要用 nvidia-docker命令。

### 基于镜像创建容器

创建容器注意几点：

-it  在容器中指定一个终端，并允许进行交互。

workspace映射，端口映射，容器名，共享内存设置

```bash
# 关于docker run
sudo docker run -it --name algorithm -v /data/algorithm:/data/algorithm --runtime=nvidia -e NVIDIA_VISIBLE_DEVICE=all 0a2a08268c14

# 启用gpu
docker run --name car_det --gpus all -it -v /media/data/zsl:/workspace -p 6006:6006 --shm-size=64g n7554ac65eba5

docker run --name detect_trt --gpus all -it -v /data/home/xtxk:/workspace 6a0422b292e7
# 加-it 创建后会直接进入容器内部的终端
```

创建好容器后

```bash
#查看当前容器
docker ps -a
#启动容器
docker start containerID
#进入容器
docker exec -it containerID /bin/bash
# 获取容器的日志
docker logs ef5a1d1af230
```



# Plus

版权声明：本文为CSDN博主「84岁带头冲锋」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/L2111533547/article/details/125830743

## dockerfile 常用指令

指令的一般格式为 INSTRUCTION arguments，指令包括 FROM、MAINTAINER、RUN 等。

### FROM

格式为 FROM 或FROM :。
第一条指令必须为 FROM 指令。并且，如果在同一个Dockerfile中创建多个镜像时，可以使用多个 FROM 指令（每个镜像一次）。

```
格式：
　　FROM <image>
　　FROM <image>:<tag>
　　FROM <image>@<digest>

示例：　　
	FROM mysql:5.6
注：
   tag或digest是可选的，如果不使用这两个值时，会使用latest版本的基础镜像
```


### MAINTAINER

格式为 MAINTAINER ，指定维护者信息。

```
格式：
    MAINTAINER <name>
示例：
    MAINTAINER bertwu
    MAINTAINER xxx@163.com
    MAINTAINER bertwu <xxx@163.com>
```


### RUN

格式为 RUN 或 RUN [“executable”, “param1”, “param2”]。
前者将在 shell 终端中运行命令，即 /bin/sh -c；后者则使用 exec 执行。指定使用其它终端可以通过第二种方式实现，例如 RUN [“/bin/bash”, “-c”, “echo hello”]。
每条 RUN 指令将在当前镜像基础上执行指定命令，并提交为新的镜像。当命令较长时可以使用 \ 来换行。

```
RUN用于在构建镜像时执行命令，其有以下两种命令执行方式：
shell执行
格式：
    RUN <command>
exec执行
格式：
    RUN ["executable", "param1", "param2"]
示例：
    RUN ["executable", "param1", "param2"]
    RUN apk update
    RUN ["/etc/execfile", "arg1", "arg1"]
注：RUN指令创建的中间镜像会被缓存，并会在下次构建中使用。如果不想使用这些缓存镜像，
可以在构建时指定--no-cache参数，如：docker build --no-cache
```


### CMD

支持三种格式
CMD [“executable”,“param1”,“param2”] 使用
exec 执行，推荐方式；
CMD command param1 param2 在
/bin/sh 中执行，提供给需要交互的应用；
CMD [“param1”,“param2”] 提供给
ENTRYPOINT 的默认参数；
指定启动容器时执行的命令，每个 Dockerfile 只能有一条 CMD 命令。如果指定了多条命令，只有最后一条会被执行。
如果用户启动容器时候指定了运行的命令，则会覆盖掉 CMD 指定的命令。

```
格式：
    CMD ["executable","param1","param2"] (执行可执行文件，优先)
    CMD ["param1","param2"] (设置了ENTRYPOINT，则直接调用ENTRYPOINT添加参数)
    CMD command param1 param2 (执行shell内部命令)
示例：
    CMD echo "This is a test." | wc -l
    CMD ["/usr/bin/wc","--help"]

注：CMD不同于RUN，CMD用于指定在容器启动时所要执行的命令，而RUN用于指定镜像构建时所要执行的命令。
```


### EXPOSE

格式为 EXPOSE […]。
告诉 Docker 服务端容器暴露的端口号，供互联系统使用。在启动容器时需要通过 -P，Docker 主机会自动分配一个端口转发到指定的端口。

```
格式：
    EXPOSE <port> [<port>...]
示例：
    EXPOSE 80 443
    EXPOSE 8080    
    EXPOSE 11211/tcp 11211/udp
注：　　EXPOSE并不会让容器的端口访问到主机。要使其可访问，需要在docker run运行容器时通过-p来发布这些端口，或通过-P参数来发布EXPOSE导出的所有端口

如果没有暴露端口，后期也可以通过-p 8080:80方式映射端口，但是不能通过-P形式映射
```

### ENV

格式为 ENV 。 指定一个环境变量，会被后续 RUN 指令使用，并在容器运行时保持。

```
格式：
    ENV <key> <value>  #<key>之后的所有内容均会被视为其<value>的组成部分，因此，一次只能设置一个变量
    ENV <key>=<value> ...  #可以设置多个变量，每个变量为一个"<key>=<value>"的键值对，如果<key>中包含空格，可以使用\来进行转义，也可以通过""来进行标示；另外，反斜线也可以用于续行
示例：
    ENV myName John Doe
    ENV myDog Rex The Dog	
    ENV myCat=fluffy
```


### ADD

格式为 ADD 。
该命令将复制指定的 到容器中的 。 其中 可以是Dockerfile所在目录的一个相对路径；也可以是一个 URL；还可以是一个 tar 文件（自动解压为目录）。

```
格式：
    ADD <src>... <dest>
    ADD ["<src>",... "<dest>"] 用于支持包含空格的路径
示例：
    ADD hom* /mydir/          # 添加所有以"hom"开头的文件
    ADD hom?.txt /mydir/      # ? 替代一个单字符,例如："home.txt"
    ADD test relativeDir/     # 添加 "test" 到 `WORKDIR`/relativeDir/
    ADD test /absoluteDir/    # 添加 "test" 到 /absoluteDir/
```

### COPY

格式为 COPY 。
复制本地主机的 （为 Dockerfile 所在目录的相对路径）到容器中的 。
当使用本地目录为源目录时，推荐使用 COPY。

### ENTRYPOINT
两种格式：
ENTRYPOINT [“executable”, “param1”, “param2”]
ENTRYPOINT command param1 param2（shell中执行）。
配置容器启动后执行的命令，并且不可被 docker run 提供的参数覆盖。
每个 Dockerfile 中只能有一个 ENTRYPOINT，当指定多个时，只有最后一个起效。

```
格式：
    ENTRYPOINT ["executable", "param1", "param2"] (可执行文件, 优先)
    ENTRYPOINT command param1 param2 (shell内部命令)
示例：
    FROM ubuntu
    ENTRYPOINT ["ls", "/usr/local"]
    CMD ["/usr/local/tomcat"]
  之后，docker run 传递的参数，都会先覆盖cmd,然后由cmd 传递给entrypoint ,做到灵活应用

注：ENTRYPOINT与CMD非常类似，不同的是通过docker run执行的命令不会覆盖ENTRYPOINT，
 而docker run命令中指定的任何参数，都会被当做参数再次传递给CMD。
 Dockerfile中只允许有一个ENTRYPOINT命令，多指定时会覆盖前面的设置，
 而只执行最后的ENTRYPOINT指令。
 通常情况下，	ENTRYPOINT 与CMD一起使用，ENTRYPOINT 写默认命令，当需要参数时候 使用CMD传参
```


### VOLUME

格式为 VOLUME [“/data”]。
创建一个可以从本地主机或其他容器挂载的挂载点，一般用来存放数据库和需要保持的数据等。

```
格式：
    VOLUME ["/path/to/dir"]
示例：
    VOLUME ["/data"]
    VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"
注：一个卷可以存在于一个或多个容器的指定目录，该目录可以绕过联合文件系统，并具有以下功能：
1 卷可以容器间共享和重用
2 容器并不一定要和其它容器共享卷
3 修改卷后会立即生效
4 对卷的修改不会对镜像产生影响
5 卷会一直存在，直到没有任何容器在使用它
```


### USER

格式为 USER daemon。
指定运行容器时的用户名或 UID，后续的 RUN 也会使用指定用户。
当服务不需要管理员权限时，可以通过该命令指定运行用户。并且可以在之前创建所需要的用户，例如：RUN groupadd -r postgres && useradd -r -g postgres postgres。要临时获取管理员权限可以使用 gosu，而不推荐 sudo。

```
格式:　　
USER user　　
USER user:group　　
USER uid　　
USER uid:gid　　
USER user:gid　　
USER uid:group

示例：    　　
     USER www
 注：
　　使用USER指定用户后，Dockerfile中其后的命令RUN、CMD、ENTRYPOINT都将使用该用户。
　　镜像构建完成后，通过docker run运行容器时，可以通过-u参数来覆盖所指定的用户。
```


WORKDIR
格式为 WORKDIR /path/to/workdir。
为后续的 RUN、CMD、ENTRYPOINT 指令配置工作目录。
可以使用多个 WORKDIR 指令，后续命令如果参数是相对路径，则会基于之前命令指定的路径

```
格式：
    WORKDIR /path/to/workdir
示例：
    WORKDIR /a  (这时工作目录为/a)
    WORKDIR b  (这时工作目录为/a/b)
    WORKDIR c  (这时工作目录为/a/b/c)
注：　
  通过WORKDIR设置工作目录后，Dockerfile中其后的命令RUN、CMD、ENTRYPOINT、ADD、COPY
  等命令都会在该目录下执行。在使用docker run运行容器时，可以通过-w参数覆盖构建时所设置的工作目录。
```


### ONBUILD

格式为 ONBUILD [INSTRUCTION]。
配置当所创建的镜像作为其它新创建镜像的基础镜像时，所执行的操作指令

```
格式：　
	ONBUILD [INSTRUCTION]
示例：
　　ONBUILD ADD . /app/src
　　ONBUILD RUN /usr/local/bin/python-build --dir /app/src
注：
　　NNBUID后面跟指令，当当前的镜像被用做其它镜像的基础镜像，该镜像中的触发器将会被钥触发
```

### LABEL

用于为镜像添加元数据

```
格式：
    LABEL <key>=<value> <key>=<value> <key>=<value> ...
示例：
　　LABEL version="1.0" description="这是一个Web服务器" by="IT笔录"
注：
　　使用LABEL指定元数据时，一条LABEL指定可以指定一或多条元数据，指定多条元数据时不同元数据
　　之间通过空格分隔。推荐将所有的元数据通过一条LABEL指令指定，以免生成过多的中间镜像。
```


### ARG

用于指定传递给构建运行时的变量(给dockerfile传参)，相当于构建镜像时可以在外部为里面传参

```dockerfile
格式：
    ARG <name>[=<default value>]
示例：
    ARG site
    ARG build_user=www

From centos:7
ARG parameter
VOLUME /usr/share/nginx
RUN yum -y install $parameter
EXPOSE 80 443
CMD nginx -g "daemon off;"
```

可以这如下这样灵活传参

```bash
docker build --build-arg=parameter=net-tools -t nginx:01 . 
```



网络配置

ref：

https://blog.csdn.net/sirobot/article/details/118196012

https://www.jianshu.com/p/5db52e909f59



**host是docker0的网关地址172.17.0.1，不能是127.0.0.1，在容器中127.0.0.1指向容器自己**



# Docker 文件清理

清理后电脑多了很多空间。

```bash
# 首先删除不要的镜像和容器
docker rmi image_id
docker rm -f container_id

# 查看Docker的磁盘使用情况
docker system df

```



```bash
# 清理磁盘，删除关闭的容器、无用的数据卷和网络，以及dangling镜像(即无tag的镜像)
docker system prune
```

慎用，**会一次性清理所有停止的容器**



```bash
docker system prune -a  # 慎用
```

 慎用， 命令清理得更加彻底，可以将没有容器使用Docker镜像都删掉。注意，这两个命令会把你暂时关闭的容器，以及暂时没有用到的Docker镜像都删掉





# Docker 国内镜像使用

1. 一次性：

```bash
# 格式
sudo docker pull [镜像源]/镜像名:版本号 
# 示例
docker pull docker.m.daocloud.io/nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04
```

2. 永久配置

```bash
sudo mkdir -p /etc/docker
# 添加国内镜像
sudo vim /etc/docker/daemon.json
```

添加以下内容：

```json
{
    "registry-mirrors": [
        "https://docker.m.daocloud.io",
        "https://docker.1ms.run",
        "https://docker-0.unsee.tech",
        "https://docker.xuanyuan.me/",
        "https://lispy.org/"
    ]
}
```

然后重启配置

```bash
sudo systemctl daemon-reload 
sudo systemctl restart docker 
```

直接`docker pull 镜像` 就可以 。

