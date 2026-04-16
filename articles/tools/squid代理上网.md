[squid官网链接](https://www.squid-cache.org/)



这里squid工具使用背景，有个3588板子只能通过交换机和本地电脑连接，板子无法上网，这里通过安装squid代理，来使得板子能够正常上网。大致是，本地电脑安装squid代理将本地电脑作为一个网络代理服务器，修改板子的网络代理为本地电脑ip，这样板子可通过本地电脑代理直接访问网络。

# 使用步骤

本地pc安装squid

1.

安装squid

```
sudo apt install squid
```

也可以下载源码本地进行编译.

2.

修改配置文件

```
# 因为是只读的，需要先给写权限
sudo chmod +w squid.conf
sudo vim squid.conf
```

vim编辑器下`/http_access `，搜索。 enter后 使用n键查找下一个，找到

```
# http_access deny all  # 注释掉改行
http_access allow all   # 添加这一行
```

然后`wq`保存文件。

3.

启动squid服务

```
sudo systemctl start squid
```

查看服务端口号

```
sudo netstat -antpl # 加sudo 否则程序名可能检测不到
```

可以看到是3128端口号。



板端配置及设置

4.

到板端添加环境变量。

```bash
#先试着ping一下开了squid服务的机器的ip
#这里我板子和安装了squid的pc通过同一个交换机连接，pc的ip为192.168.1.86
ping 192.168.1.86 # 需要能成功ping通
#配置网络代理
export http_proxy=http://192.168.1.86:3128
```

5.

测试是否能够联网

```
wget www.baidu.com
```

一般可以成功连接并下载保存一个index.html文件

出现了

> wget: server returned error: HTTP/1.1 403 Forbidden

将pc机器squid服务重启一下就可以成功ping通了。
