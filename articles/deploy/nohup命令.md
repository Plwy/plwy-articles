ref:https://blog.csdn.net/weixin_49114503/article/details/134266408

## nohup

nohup 是 no hang up的缩写，意思是不挂断 。

[nohup 命令](https://so.csdn.net/so/search?q=nohup 命令&spm=1001.2101.3001.7020)，在**默认情况下（非重定向时），会输出一个名叫 nohup.out 的文件到当前目录下**，如果当前目录的 nohup.out 文件不可写，输出重定向到 $HOME/nohup.out 文件中。

**应对场景**：远程执行 Linux 脚本时，有时候会由于网络问题，导致客户端失去连接，终端断开，脚本运行一半就意外结束了。这种时候，就可以用nohup 指令来运行指令，即使客户端与服务端断开，服务端的脚本仍可继续运行。

- 关闭客户端后，命令仍然会运行，不会挂断。
- nohup命令允许被运行的程序的输出信息将不会显示到终端。

```bash
# 不挂断运行默认输出到当前目录nohup.out
nohup sh test.sh
# 使用重定向 >，不挂断运行默认输出到当前指定文件output.log下
nohup sh test.sh >output.log
```



## &

通常nohup和&配合运行 ，nohup保证不挂断，&实现后台运行。

```bash
# 挂起并后台运行， 日志输出到output.log
nohup ./test.sh >output.log &
```

**挂起并后台运行， 不输出日志**

```
nohup ./test.sh >/dev/null &
```

**其他一些文件描述符的使用：**

- `0 `表示stdin标准输入，用户键盘输入的内容
- `1` 表示stdout标准输出，输出到显示屏的内容
- `2 `表示stderr标准错误，报错内容
- `2>&1 `是一个整体，`>`左右不能有空格，即将错误内容重定向输入到标准输出中去
- `>`符号用于将命令的标准输出重定向到指定的文件中
- `2>`表示将命令的标准错误输出重定向到指定的文件中
- `2>&1`表示将命令的标准错误输出重定向到标准输出中

**只输出错误信息到日志文件，其它日志不输出**

```
nohup ./test.sh > /dev/null   2>error.log  &
```

**输出标准日志和错误日志一起输出到log中**

```bash
# 后台执行test.sh文件，将标准日志输出到output.log文件中，将错误日志也输出到output.log文件中
nohup ./test.sh > output.log 2>&1 &
等同于
nohup ./test.sh > output.log 2>output.log &
```

