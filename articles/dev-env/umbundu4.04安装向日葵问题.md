**下载安装**

[图形版](https://sunlogin.oray.com/download/linux?type=personal)

```
sudo dpkg -i SunloginClient_15.2.0.63064_amd64.deb 
```

报错：

> 正在选中未选择的软件包 sunloginclient。
> (正在读取数据库 ... 系统当前共安装有 223558 个文件和目录。)
> 准备解压 SunloginClient_15.2.0.63064_amd64.deb  ...
> 正在解压 sunloginclient (15.2.0.63064) ...
> dpkg: 依赖关系问题使得 sunloginclient 的配置工作不能继续：
>  sunloginclient 依赖于 libgconf-2-4；然而：
>   未安装软件包 libgconf-2-4。
>
> dpkg: 处理软件包 sunloginclient (--install)时出错：
>  依赖关系问题 - 仍未被配置
> 正在处理用于 gnome-menus (3.36.0-1.1ubuntu3) 的触发器 ...
> 正在处理用于 desktop-file-utils (0.27-2build1) 的触发器 ...
> 在处理时有错误发生：
>  sunloginclient



**未解决方案**

https://blog.csdn.net/xiangfengl/article/details/141390296

```
sudo apt update
sudo apt upgrade
sudo apt --fix-broken install
```

**解决方案：**

1. 下载两个包

```bash
# libgconf-2-4
sudo wget http://th.archive.ubuntu.com/ubuntu/pool/universe/g/gconf/libgconf-2-4_3.2.6-7ubuntu2_amd64.deb

# gconf2-common
sudo wget http://th.archive.ubuntu.com/ubuntu/pool/universe/g/gconf/gconf2-common_3.2.6-7ubuntu2_all.deb
```

2. 安装

```bash
# 安装分先后
sudo dpkg -i gconf2-common_3.2.6-7ubuntu2_all.deb
sudo dpkg -i libgconf-2-4_3.2.6-7ubuntu2_amd64.deb 
```

最后安装成功。

```
sudo dpkg -i SunloginClient_15.2.0.63064_amd64.deb
```

