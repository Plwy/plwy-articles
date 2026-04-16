# valgrind的安装及调试使用

## 安装

```bash
sudo apt install valgrind
```

报错

```
Error in `/usr/share/doc-base/valgrind', line 9: all `Format' sections are invalid.
Note: `install-docs --verbose --check file_name' may give more details about the above error.
```

根据报错提示输入

```bash
install-docs --verbose --check /usr/share/doc-base/valgrind
```

输出

```
Warning in `/usr/share/doc-base/valgrind', line 9: file `/usr/share/doc/valgrind/html/manual.html' does not exist.
Error in `/usr/share/doc-base/valgrind', line 9: all `Format' sections are invalid.
/usr/share/doc-base/valgrind: Fatal error found, the file won't be registered.
==========
“/usr/share/doc-base/valgrind”第 9 行警告：文件“/usr/share/doc/valgrind/html/manual.html”不存在。 “/usr/share/doc-base/valgrind”第 9 行出错：所有“Format”部分均无效。 /usr/share/doc-base/valgrind：发现致命错误，该文件将不会被注册。
```

不注册就不注册吧，问题不大。

## a simple demo

test.cpp

```c++
#include <stdlib.h>
#include <stdio.h>
void func()
{
 //只申请内存而不释放
    void *p=malloc(sizeof(int));
}
int main()
{
    func();
    printf("hello!\n");
    return 0;
}
```

```bash
// 编译生成可执行文件
gcc -o ./a.out ./test.cpp
```

valgrind工具检测可执行文件

```bash
valgrind --log-file=valReport --leak-check=full --show-reachable=yes --leak-resolution=low ./a.out
```

运行完后，当前目录下生成valReport日志文件

```
vim valReport 
```

查看日志文件，日志如下：

```
==2207536== HEAP SUMMARY:
==2207536==     in use at exit: 4 bytes in 1 blocks
==2207536==   total heap usage: 2 allocs, 1 frees, 1,028 bytes allocated
==2207536==
==2207536== 4 bytes in 1 blocks are definitely lost in loss record 1 of 1
==2207536==    at 0x483B7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2207536==    by 0x10917E: func() (in /home/sun/zsl_workspace/cpp_proj/test_cpp/a.out)
==2207536==    by 0x109192: main (in /home/sun/zsl_workspace/cpp_proj/test_cpp/a.out)
==2207536==
==2207536== LEAK SUMMARY:
==2207536==    definitely lost: 4 bytes in 1 blocks
==2207536==    indirectly lost: 0 bytes in 0 blocks
==2207536==      possibly lost: 0 bytes in 0 blocks
==2207536==    still reachable: 0 bytes in 0 blocks
==2207536==         suppressed: 0 bytes in 0 blocks
==2207536==
==2207536== For lists of detected and suppressed errors, rerun with: -s
==2207536== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)

```

可以看到，main , 中的func()， 中的malloc函数导致了泄露。 明确泄露的内存有4个字节。

## 日志分析

ref:https://www.cnblogs.com/gmpy/p/14778243.html

**valgrind** 将内存泄漏分为 4 类。

- 明确泄漏（definitely lost）：内存还没释放，但已经没有指针指向内存，内存已经不可访问
- 间接泄漏（indirectly lost）：泄漏的内存指针保存在明确泄漏的内存中，随着明确泄漏的内存不可访问，导致间接泄漏的内存也不可访问
- 可能泄漏（possibly lost）：指针并不指向内存头地址，而是指向内存内部的位置
- 仍可访达（still reachable）：指针一直存在且指向内存头部，直至程序退出时内存还没释放。

### 明确泄露

上面的简单例子就是明确的泄露，使用了malloc申请了内存却没有free。

**明确泄漏的内存是强烈建议修复的**.

### 间接泄露

间接泄漏就是指针并不直接丢失，但保存指针的内存地址丢失了

间接泄露举例：

```cpp
struct list {
	struct list *next;
};

int main(int argc, char **argv)
{
	struct list *root;
	
	root = (struct list *)malloc(sizeof(struct list));
	root->next = (struct list *)malloc(sizeof(struct list));
	printf("root %p roop->next %p\n", root, root->next);
	root = NULL;
	return 0;
}
```

丢失的是 *root* 指针，导致 *root* 存储的 *next* 指针成为了间接泄漏。

默认情况下，只会打印 明确泄漏 和 可能泄漏，如果需要同时打印 间接泄漏，需要加上选项 **--show-reachable=yes**.

**间接泄漏的内存肯定也要修复的，不过一般会随着 明确泄漏 的修复而修复**

### 可能泄露

**valgrind** 之所以会怀疑可能泄漏，是因为指针已经偏移，并没有指向内存头，而是有内存偏移，指向内存内部的位置。

有些时候，这并不是泄漏，因为这些程序就是这么设计的，例如为了实现内存对齐，额外申请内存，返回对齐后的内存地址。但更多时候，是我们不小心 `p++` 了。

**可能泄漏的情况需要我们根据代码情况自己分析确认**

### 仍可访达

仍可访达 表示在程序退出时，不管是正常退出还是异常退出，内存申请了没释放，都属于仍可访达的泄漏类型。

如果测试的程序是正常退出的，那么这些 仍可访达 的内存就是泄漏，最好修复了。

如果测试是长期运行的程序，通过信号提前终止，那么这些内存就大概率并不是泄漏。
