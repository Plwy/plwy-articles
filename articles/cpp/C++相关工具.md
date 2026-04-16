

[TOC]

本人当前使用的c++工具链

编辑器：vscode /vim

LSP ：clangd/intellicode

编译器： gcc/g++, llvm+clang

调试：vscode 配置断点调试 和 GDB/LLDB命令行调试

代码风格：google style

代码格式检查：clang-format

远程连接：remote-ssh



todo：

- clangd配置
- clang-format修改配置

## C++运行原理

[详解C/C++代码的预处理、编译、汇编、链接全过程](https://blog.csdn.net/hypc9709/article/details/129413523)



## C++标准

- C++11(2011年发布)：引入了许多新特性，如智能指针、多线程支持、并发控制、动态类型、自动类型推断等。
- C++14(2014年发布)：主要针对C++11的补充和改进，增加了一些新特性，如constexpr、if constexpr、inline变量等。
- C++17(2017年发布)：引入了更多新特性，如结构化绑定、并行算法、文件系统库等。



## C++开发工具

linux上开发常见使用的IDE：

- vscode

- qt creator

- clion

- **source insight**：

  相较于vscode，可以通过创建Source Insight工程来选择哪些文件加入，哪些文件不加入

- **code blocks**

- vim

- emasc

​	可使用evil mode用于光标移动，编辑，按键映射

- understand



##  C/C++ LSP

 *LSP*是*Language* *Server* *Protocol* 的缩写,它定义了一种标准化的协议,用于编辑器和语言工具之间的通信。

**intellisense**

代码补全辅助工具。自动代码补全；实时错误检查；代码改进建议。

**clanged**

和intellisense一样是一个语言服务器，可以通过插件与许多编辑器一起使用。功能包含：代码完成、编译错误、转到定义等。



## C++ 代码分析及分析工具

### 代码静态分析

程序静态分析（Program static analysis）是指**在不执行代码情况下， 通过词法分析、语法分析、语义分析、控制流、数据流分析等技术对源代码进行扫描，验证代码是否满足规范性、安全性、可靠性、可维护性等指标的一种代码分析技术**。 通过对代码进行审查分析，检查代码的功能、性能，提升代码质量。

**静态分析方式**

- 
  人工审查，依赖于人，适合于小型项目或者代码量不大的场景；效率低、易遗漏

- 软件工具分析，理想的方式， 准确率、可靠性、效率都远高于人工审查

对源代码的静态分析，通常会有以下几种错误类别：

- **内存相关的致命错误**
  - 访问没有申请内存的空指针（空指针）
  - 访问已释放内存的指针（野指针）
  - 内存越界访问
  - 内存泄露，申请了内存没有释放
  - 重复释放内存
  - 文件描述符泄漏（未释放）
  - 格式化字符串不安全（内存越界）
- **逻辑相关错误**
  - 逻辑错误，重复代码分支、缺少分支语句（如`switch`缺少`break`）、变量比较类型不一致、常true或false
  - 运算错误，除0运算、无符号数小于0、bool类型自加
  - 可疑检查，死循环、死锁、if语句“=”问题、返回局部变量、变量溢出
- **编码规范与其他**
  - 编程风格，命名、规范性、可读性、可移植和复用性
  - 执行问题，函数未使用、变量未使用、代码不可到达（提前`return`）
  - 隐患问题，语法问题、逻辑模糊问题、类型强制转换、编译警告、`volatile`问题
  - 效率问题，时间复杂度、空间复杂度、逻辑循环、
  - 标准行业规范，如[MISRA C](https://acuity.blog.csdn.net/article/details/81989570)

#### **静态分析工具推荐**

- 开源免费

**CoBot、TscanCode、Cppcheck、Flawfinder**等

- 专业付费

**pclint，coverity，Klocwork**等。

#### 代码度量工具

大多选择SourceMonitor，这款软件是免费的，功能包括基本的代码行、函数数量、类数量统计，还包括分支比例度量、圈复杂度度量、代码深度度量等，并且会根据度量结果生成报表。

## C++代码风格规范

ref：https://zhuanlan.zhihu.com/p/414323404

[Google C++编码风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/contents/)

代码风格规范主要有几个方面：命名规范、语言规范、格式规范。其中大部分命名规范和语言规范主要需要开发者编写代码的时候遵循。

代码格式化工具有clang-format。clang-format是一个开源的代码格式化工具，它可以帮助程序员自动调整源代码的格式，以符合指定的编码风格规范。通过配置简单易懂的格式化选项，clang-format可以在保持代码功能不变的情况下，自动处理缩进、空格、括号、逗号等细节，提高代码的可读性和一致性。



## 其他工具

**Copilot**

Github推出的Copilot，AI辅助编程的工具。 和[cursor](https://cursor.sh/)一样能自动生成代码。

**CodeGeeX**

借助大模型的智能，不仅能生成和补全代码，还能自动添加注释、进行代码审查、修复bug，甚至能跨语言翻译，提供针对技术问题的问答支持。它支持Python、Java等语言，适用于VS Code、JetBrains IDEs等工具。





