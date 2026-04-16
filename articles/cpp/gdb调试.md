

## 启动gdb

进入GDB调试模式

  ```
  gdb my_program
  ```

  启动GDB并将程序加载到内存中，my_program是你需要调试的程序，需要编译为debug版本

向程序传递参数

  在启动GDB时：

```
gdb -args my_program -v
```

  在启动GDB时将参数传递给程序。

eg:

```
// ./test ./modelpath ./imgpath 3
//gdb调试
gdb --args ./test ./modelpath ./imgpath 3
```



## 常用GDB命令

run（r）：开始运行程序，直到遇到断点或程序退出

```
(gdb) run
(gdb) r
```

break（b）：在指定的源文件的特定行或函数处设置断点

```
(gdb) break file.c:42
(gdb) b file.c:42
```

next（n）：单步执行，但不进入函数调用

```
(gdb) next
(gdb) n
```

step（s）：单步执行，进入函数调用

```
(gdb) step
(gdb) s
```

continue（c）：从当前位置继续执行，直到遇到下一个断点或程序退出

```
(gdb) continue
(gdb) c
```

print（p）：查看变量或表达式的值

```
(gdb) print variable_name
(gdb) print array[0]
```

backtrace（bt）：显示当前函数调用的堆栈

```
(gdb) backtrace
(gdb) bt
```

quit（q）：退出GDB

```
(gdb) quit
```

watch（w）：监视指定变量的值的变化

```
(gdb) watch variable_name
```

info breakpoints（info b）：显示所有已设置的断点的列表

```
(gdb) info breakpoints
```

delete（d）：删除指定的断点

```
(gdb) delete breaknum
```

set variable（set）：设置变量的值

```
(gdb) set variable variable_name=value
```

call（c）：调用指定的函数

```
(gdb) call function_name()
```

frame（f）：切换到调用堆栈中的不同帧

```
(gdb) frame 2
```

until（u）：继续执行，直到达到特定的代码行

```
(gdb) until 42
```



info threads（info t）：显示所有线程的列表

```
(gdb) info threads
```



thread（t）：切换到不同的线程

```
(gdb) thread threadnum
```

