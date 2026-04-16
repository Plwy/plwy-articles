仅仅有简单c++基础的，想看懂稍复杂c++项目有几个点理解了很关键。

- 引用和指针的定义和区别
- 指针的声明和内存分配。
- 指针的传递，值传递，引用传递。
- 结构体的初始化。
- memset和malloc的含义和区别。



当前程序的内存管理有问题，如何进行排查，不会改，为什么不会改？具体的点在哪里？

第一步，静态代码检查 。需要知道内存是如何进行管理的。如何分配和释放的。

指针如何定义和初始化

结构体如何定义和初始化

指针传递，内存在哪里释放

第二步，动态调试。需要知道如何定位到内存问题处，并找出原因。

如何使用gdb进行调试，以及如何查看调试信息，并分析。

如何使用Valgrind进行调试，以及如何查看调试信息，并分析。





zerocopy和普通模式的区别

MPP做了什么以什么形式

RGA做了什么以什么形式?是否需要更新驱动，还是api的问题还是本身调用代码的问题。



### 局部变量作为返回值的问题

```c++
int* test()
{
        int a=10;
        return &a;
}
int main()
{
        int* p=test();
        printf("%d\n",*p);
        return 0;
}
```

报错！这里传递了局部变量的内存地址，但是局部变量数据存放在栈去，在函数结束后就释放了，这个地址就无效了。



```c++
int test()
{
        int a=10;
        return a;
}
int main()
{
        int p=test();
        printf("%d\n",p);
        return 0;
}
```

没问题。 这里传递的是局部变量的值，即使该局部变量内存空间释放也没有影响。

```c++
int* test()
{
        int a=10;
        int *q = nullptr;
        q = &a;
        return q;
}
int main()
{
        int* p=test();
        printf("%d\n",*p);
        return 0;
}
```

**为什么运行没问题?** 这里返回的不是局部变量的地址，而是局部变量的值，一个int指针类型的值。但是a的地址指向了q,但是a被释放后，该地址岂不是无效的？

指针指向的内存一定在堆区么？？

这里的p是在栈区么需要释放么？？







### sizeof类型和sizeof变量的区别

遇到的问题：

```c++
typedef struct {
    int left;
    int top;
    int right;
    int bottom;
} image_rect_t;

typedef struct {
    image_rect_t box;
    float prop;
    int cls_id;
} object_detect_result;

typedef struct {
    int id;
    int count;
    object_detect_result results[128];
} object_detect_result_list;

//这里定义了一个结构体，接收传出的检测结果。
object_detect_result_list *results;
memset(results, 0, sizeof(results));  // 使用结构体指针变量，结果正常
memset(results, 0, sizeof(object_detect_result_list));  // 使用结构体类型，结果异常,直接内存错误
```

打印发现sizeof(results)=8, sizeof(object_detect_result_list)=3080.

**分析：**

结构体变量中第一个成员的地址就是结构体变量的首地址。结构体大小等于最后一个成员的偏移量加上最后一个成员的大小。偏移量指的是结构体变量中成员的地址和结构体变量地址的差。通常，结构体的总大小为结构体最宽基本类型成员大小的整数倍，如有需要编译器会在最末一个成员之后加上填充字节。

sizeof(结构体变量)为求该结构体的大小。计算如下：

image_rect_t大小：4+4+4+4=16

object_detect_result大小：16+4+4=24

object_detect_result_list大小：4+4+24*128=3080

sizeof(结构体指针变量)， 16位机器，指针占2个字节。32位机器，指针占4个字节。64位机器，指针占8个字节。这里是8个字节。

**原因：**

这里对结构体指针变量做初始化，声明后result只会分配8个字节的内存空间.

这里memset指的将results指向的前n字节的内存置0.最后的字节空间的大小一定是小于等于results的内存大小。

**这里没有注意到是结构体指针变量，而不是结构体变量导致了错误。如果results是结构体变量，这里结果是一致的。sizeof( )结构体类型名和结构体变量的值是一样的。**

指针的初始化不用这样用memset的方式置0，可以直接用NULL或者nullptr赋值。



### 对象的动态建立和静态建立

C++中建立类的对象有两种方式：
（1）静态建立，例如 A a;
     静态建立一个类对象，就是由编译器为对象在栈空间中分配内存。使用这种方法，是直接调用类的构造函数。
（2）动态建立，例如 A* p = new A();
     动态建立一个类对象，就是使用new运算符为对象在堆空间中分配内存。这个过程分为两步：第一步执行operator new( )函数，在堆空间中搜索一块内存并进行分配；第二步调用类的构造函数构造对象。这种方法是间接调用类的构造函数。



在C++语法中，静态对象由于是在STACK上生成，因而比动态生成对象的效率要高，而且不会造成内存泄露。而我发现在实际工作中，一般都是动态生成对象(用NEW)，动态生成有什么好处吗？

原因 1：
“静态对象由于是在STACK上生成，因而比动态生成对象的效率要高，而且不会造成内存泄露”

  不会造成内存泄露 的原理你应该清楚吧，就是因为在你的对象生存的函数退出时，对象自动析构了。但~~~~~
  如果你的对象要在多个涵数中使用，或者要在一个函数中建立，而在另一个函数中使用（COM 就是用这种方法使用对象的），那你怎么办？当然只能是用 new 的方法了。

原因 2：
   函数的传址与传值的不同你应该懂吧。
   标明动态对象的是一个指针，标明静态对象的是一个值。当这个对象作为别的函数的参数时，你就知动态对象的作用了。

另：
   如果你的对象是全局的，那静态，动态也一样：都是在程序退出时析构。都不用关心内存问题。而且动态对象可以在程序未退出进删除，这点要比静态对象强。

原文链接：https://blog.csdn.net/Don_sandman/article/details/78047146

----------------

静态建立对象在程序运行的过程中，对象所占的空间是不能随时释放的。如果希望在需要时才建立对象，不需要时就释放它，这就是动态建立对象，使用new运算符

用new运算符动态的分配内存后，将返回一个指向新对象的指针值（即所分配内存空间的起始地址），可以通过这个地址来访问这个对象

```c++
Box * pt;			// 定义一个指向Box类对象的指针变量
pt = new Box;		// 在pt存放了新建对象的起始地址
Box * ps = new Box(1,2,3);	// 可以在指向new时，对新建的对象进行初始化
```

### 初始化一个指针变量。是否需要释放。 如何给它分配内存

比如这样写是否合理？是否需要释放该指针的内存？

```c++
int main(int argc, char **argv)
{
	char *video_name = argv[1];
}
```

我理解，这里是传入了一个char* 指针的指针，这个argv[1]是一个以及分配内存的char *的地址，需要定义一个char *的指针来接收这个地址，所以这里只是将一个char类型的指针变量指向了一段内存地址。 这个内存存在的生命周期和main()函数一致。**可以手动释放也可以不管。**



### 对于带指针数组的结构体变量，如何初始化。

image_buffer_t  in_data; 如何赋值，传入其他函数后，最外层的函数是否需要进行内存释放?

对于结构体中的指针成员变量，需要手动为其分配内存。



[ref](https://blog.csdn.net/XZ2585458279/article/details/124716701)**在为结构体分配内存时，运行时系统不会自动为结构体内部的指针分配内存。类似地，当结构体消失时，运行时系统也不会自动释放结构体内部的指针指向的内存。**

```c++
typedef struct_person {
	char* firstName;
	char* lastName;
	char* title;
	uint age;
} Person;

```

```c++
void initializePerson (Person *person, const char* fn,const char* ln,const char* title, uint age) 
{
	person->firstName = (char*) malloc(strlen(fn) + 1);
	strcpy(person->firstName, fn);
	person->lastName = (char*) malloc(strlen(ln) + 1);
	strcpy(person->lastName, ln);
	person->title = (char*) malloc(strlen(title)+ 1);
	strcpy(person->title, title);
	person->age = age;
}

void processPerson() {
	Person person;
	initializePerson(&person, "Peter", "Underwood", "Manager", 36);
	...
}
int main() {
	processPerson();
	...
}

```

因为这个声明是函数的一部分，函数返回后person的内存会消失。不过，动态分配的内存不会被释放，仍然保存在堆上。不幸的是，我们丢失了它们的地址，因此无法将其释放，从而导致了内存泄漏。

我们需要在processPerson函数结束前释放内存：

```c++
void deallocatePerson(Person *person) {
	free(person->firstName);
	free(person->lastName);
	free(person->title);
}

void processPerson( ) {
	Person person;
	initializePerson(&person, "Peter", "Underwood", "Manager"，36);
	...
	deallocatePerson(&person);
```



### 关于值传递，指针的传递，引用传递。

[ref](https://zhuanlan.zhihu.com/p/179297345)例子

```c++
#include <stdio.h>
int func(int* pRes)
{
    if(pRes == NULL)
    pRes = new int(12);//分配新的内存空间给指针pRes,并赋值 
    return 0;
}
int main ()
{
    int *pInt = NULL;
    int val = func(pInt);
    printf("%d\n",*pInt);                                            
    return 0;
}
```

`g++ -o test test.cpp`编译可通过，`./test` 执行会报错`segmentation fault (core dumped)`。

**原因**：在`func`函数调用过程中，形参和实参的传递使用了`值传递`方式，这种情况下，形参变量在`函数体内`发生了变化，在函数结束之后，`形参变量随之释放`，不能把变化的结果返回给实参。

可以使用`指针传递`或者`引用传递`。想要在函数体内改变`pRes`的值，并把这个变化返回到`main`函数中，必须传递`pRes`的指针。因为`pRes`本身就是指针，所以应该`传递指针的指针`，或者`指针的引用`。

> 这里指针作为函数参数时，传入函数的指针实际上是原指针的拷贝
>
> - 当对指针指向的值进行修改时，原指针指向的值也发生对应修改
> - **但当对指针指向（即指针的值）进行修改时，原指针指向不会发生改变**
>
> 为了能够对原指针指向进行修改，应该将原指针的引用作为参数传入，此时函数中对指针的任意操作都是直接对原指针进行操作
>
> - 当对指针指向的值进行修改时，原指针指向的值也发生对应修改
> - 但当对指针指向（即指针的值）进行修改时，原指针指向发对应生改变

以下两种方式都可成功打印12.

**引用传递**

```c++
#include <stdio.h>
int func(int* &pRes) // 传入指针的引用
{
    if(pRes == NULL) //指针变量不为空
    pRes = new int(12);//分配新的内存空间给指针pRes,并赋值 
    return 0;
}
int main ()
{
    int *pInt = NULL; // 指针指向空地址
    int val = func(pInt); // 传入指针变量
    printf("%d\n",*pInt); // 打印时解引用，得到指针指向的值
    return 0;
}
```

**指针传递**

```c++
#include <stdio.h>
int func(int** pRes) // 传入指针的指针
{
    if(*pRes == NULL) //指针变量不为空
    *pRes = new int(12);//分配新的内存空间给指针pRes,并赋值 
    return 0;
}
int main ()
{
    int *pInt = NULL; // 指针指向空地址
    int val = func(&pInt); // 传入指针变量
    printf("%d\n",*pInt); // 打印时解引用，得到指针指向的值
    return 0;
}
```

传值：实参拷贝传递给形参。就是把实参赋值给形参，赋值完毕后实参就和形参没有任何联系，对形参的修改就不会影响到实参。

传地址：把实参地址的拷贝传递给形参。就是把实参的地址复制给形参。复制完毕后实参的地址和形参的地址没有任何联系，对实参形参地址的修改不会影响到实参, 但是对形参地址所指向对象的修改却直接反应在实参中。

传引用：本质没有任何实参的拷贝，两个变量指向同一个对象。这是对形参的修改，必然反映到实参上。

- 无论传值还是传指针，函数都会生成一个临时变量，但**传引用时，不会生成临时变量**
- 传值时，只可以引用值而不可以改变值，但**传值引用时，可以改变值**。
- 传指针时，只可以改变指针所指的内容，不可以改变指针本身，但**传指针引用时，既可以改变指针所指的内容，又可以改变指针本身**。
- 引用传递函数的参数，在内存中并没有产生实参的副本，它是直接对实参操作;而使用一般变量传递函数的参数，当发生函数调用时，需要给形参分配存储单元，形参变量是实参变量的副本;如果传递的是对象，还将调用拷贝构造函数。因此，**当参数传递的数据较大时，用引用比用一般变量传递参数的效率和所占空间都好。**

### memset()和malloc的定义和区别

memset()函数的功能是:**将一块内存空间的每个字节都设置为指定的值**。这个函数通常用于初始化一个内存空间，或者清空一个内存空间。

```c++
void *memset(void *s, int c, size_t n); 
```

- s指向要填充的内存块。它的作用是告诉函数要填充的一块空间的起点在哪.
- c它是要填充的值，通常是一个无符号字符,它的作用是告诉函数这块空间要填充成哪个值.
  - **这个值虽然是以int型传递的,但在填充时函数会先将该值转换成无符号char型再填充内存**

- n是要被设置该值的字符数。它的作用是告诉函数一共需要将多少个字节的空间设置成要填充的值.
- 返回类型是一个指向存储区s的指针。它的作用是在函数运行结束后返回这块空间的起始地址

总的作用：**将已开辟内存空间** s 的首 n 个字节的值设为值 c。

注意：**memset只接受0x00-0xFF的赋值**

malloc函数的原型：

```
（void *）malloc（size_t size）
```

malloc 函数接受一个 size_t 类型的参数 size，表示要分配的内存块的大小（以字节为单位）。它返回一个指向分配内存块起始位置的 void* 类型指针，即通用指针。内存分配成功之后，malloc函数返回这块内存的首地址，你需要一个指针来接受这个地址。

```
int *ptr = (int *) malloc(sizeof(int) * length);
```

malloc分配了内存，但没有为它指定名字。然而，它却可以返回那块内存第一个字节的地址。
因此，可以把那个地址赋值给一个指针变量，并使用该指针来访问那块内存。

### calloc和malloc的区别

**calloc()函数**的功能是:**为num个大小为size的元素开辟一块空间,并且把空间的每个字节初始化为0.**

```cpp
//num:需要动态开辟的元素的个数.
//size:需要开辟的每个元素的大小(以字节为单位).
void* calloc (size_t num, size_t size);
```

如果在calloc()函数在开辟的过程中遇到了**无法分配请求的内存块**(即**遇到了开辟失败的情况**),那么就会**返回一个NULL指针**,对NULL指针的解引用操作是不被允许的,因此calloc的**返回值**一定要进行**检查**!

malloc()函数生成的**空间**内容是**不会初始化**,calloc**则会开辟一段已经全部初始化为0的空间**.

### memset 动态内存分配的问题。关于0和0x00

memset是对字节进行操作！

其赋值赋的是ASSCII码转为二进制赋值。

例子：

```c++
int array[5] = {1,4,3,5,2};
for(int i = 0; i < 5; i++)
    cout<<array[i]<<" ";
    cout<<endl;
memset(array,1,5*sizeof(int));  // 这里期望对 int 数组 赋初值为1

for(int k = 0; k < 5; k++)
    cout<<array[k]<<" ";
    cout<<endl;
```

输出的结果：

```
1 4 3 5 2
16843009 16843009 16843009 16843009 16843009
```

为什么呢？

　　因为memset是以字节为单位就是对array指向的内存的4个字节进行赋值，每个都用ASCII为1的字符去填充，转为二进制后，1就是00000001,占一个字节。一个INT元素是4字节，合一起就是00000001 00000001 00000001 00000001，就等于16843009，就完成了对一个INT元素的赋值了。所以**用memset对非字符型数组赋初值是不可取的！**



所以会有采用16进制的形式进行赋值的写法比如：

```c++
memset(a, 0x00, sizeof(a));
memset(a, 0xff, sizeof(a));
```



例如有一个结构体Some x，可以这样清零：

```
memset( &x, 0, sizeof(Some) );
```

如果是一个结构体的数组Some x[10]，可以这样：

```
memset( x, 0, sizeof(Some)*10 );
```

可以写成：

```
memset( x, 0x00, sizeof(Some)*10 );
```

与0 没有差异。



```
memset(pt,0xff,sizeof(pt))
```

这里使用0xff 。0xff是16进制的表达方式,0x是16进制的前缀,ff表示的是二进制的11111111

会将int所占四个字节的每个字节都赋值成0xff,所以最后为11111111111111111111111111111111为-1。(化为二进制补位，然后再赋值)。

### free后的变量是什么状态，是否需要再赋值NULL

```
void free (void* ptr);
```

- 先前通过调用 malloc、calloc 或 realloc 分配的内存块将被释放，使其再次可用于进一步分配。 
- 如果 ptr 不指向用上述函数分配的内存块，则会导致未定义的行为。
-  如果 ptr 是空指针，则该函数不执行任何操作。 
- 请注意，此函数不会更改 ptr 本身的值，因此它仍然指向相同的（现在无效）位置。

以上定义意味着，free 后只是把指针变量所指向的内存块的资源释放了，但是指针变量还是指向这个地址(内存被释放不包含数据的无效的位置)，变成了野指针，如果这个地址被其他程序分配占用，此时又复用了这个指针那么就会存在问题。所以free之后最好再将指针置为空，避免野指针的问题。

### 引用，左值，右值

在 C++ 中，引用是一个指向某个对象的别名，它在声明时必须被初始化，并且它的生命周期与其所绑定的对象一致。在赋值、函数传参等场景中，将引用与相应的对象绑定在一起，称为引用绑定。而 "cannot bind" 则表示无法将该右值和左值引用进行绑定，即无法将右值与左值引用绑定在一起。

"lvalue" 是一个 C++ 中的术语，表示可以出现在赋值语句左边（左值）的东西，通常是一个变量、数组元素或者指向对象的指针。lvalue 表示一个可寻址的对象，也就是说编译器可以生成指向它的指针。

左值引用就是指向 lvalue 类型的引用，它可以被更改。在 C++ 中，不能将右值（rvalue）绑定到左值引用上，因为右值表示的是临时对象，不具有可寻址性，不能取指针。所以不能将右值赋值给左值引用。


### 获取可变模板参数包的参数类型

ref:https://blog.csdn.net/xinkuokuo/article/details/72511284

```c++
	template <typename... Args>
	void PrintArgs(const char *desc, Args&&... args)
	{
		int argn = sizeof...(Args);
		const char *argc[] = { typeid(Args).name()... };
		cout << desc << " [ size : " << argn << " ] ";
		for (int i = 0; i < argn; i++)
		{
			cout << " [ " << argc[i] << " ] ";
		}
		cout << endl;
	}
```

结构体初始化为空的方法

```
memset(name, 0, sizeof(name));
```



### **存储内存地址用int还是long**

long比较好

**野指针的问题**：https://blog.csdn.net/liuchunjie11/article/details/80969689

### **对指针进行free， delete 和赋值 NULL ，nullptr 和0的区别。**



### **内存泄露是什么情况**

内存申请、使用之后，忘了归还（free）。这会导致程序无法长时间使用，否则内存占用就会无限增长、直至崩溃。

此外，使用不同方式申请的、归还时却用了另一种方式，这都会引起小至程序崩溃、大到数据破坏的问题。



**free报错问题**

1 释放一个空指针，这个就不用多说了，短点调试不会也会打印吧 printf("%x",p);可以打印出16进制数

2 重复释放，这个问题也很好解决，在所有的释放语句后都赋值指针为空，按照1来排查

3 释放一个非自己申请的内存，或者释放的指针指向的地方不是本进程申请的。这个的排查方式就是在所有的MALLOC申请的时候打印出地址，看看和释放的对应不对应。具体看1

4 申请的内存块写过界了或者被写过界了，此时内存块就被破坏了，释放的时候为了避免释放掉其他有用的数据，是会报错，这个时候只能靠自己的能力一步步看下每次对内存的操作，比如拷贝，书写有没有踩掉其他块的内存，具体问题具体分析。



### **初始化的指针是否必须释放？**

是的需要释放， 目前看到的都释放了。



### **string 字符串和char字符串的问题**

比如n个目标检测的类别的输入，怎么表示？

```c++

const char *locationFilename  // 类别文件路径
char *label[] // 存储类别字符串

const char *model_path = argv[1];  //这里传给locationFilename
const std::vector<std::string> CLASS_NAMES = {"drone", "bird"};
// 可以替换成
const char* CLASS_NAMES[] = {"drone", "bird"};
```



也就是说char * 可以存一个字符数组。 

char *label[]  就可以存多个字符数组。

cstring 是C语言头文件string.h的C++版本



### **什么时候函数加static？**

- 使用static关键字声明的函数是静态函数，它们的作用域被限制在定义它们的源文件中，它们不能被其他文件中的函数调用。静态函数只能在定义它们的文件中使用。

- 静态变量和函数只能被定义一次，不能在其他文件中再次定义。

```c++
static int read_image_jpeg(const char* path, image_buffer_t* image)
{}
```



### **什么时候变量这样写?**

```c++
static const char* colorspaceName[TJ_NUMCS] = {"RGB", "YCbCr", "GRAY", "CMYK", "YCCK"};
```

变量只在当前文件中使用， 且不希望值被更改。



### **读文件的几个函数**

```c++
FILE* jpegFile = NULL; //   定义了一个FIle类型的指针
unsigned long jpegSize;
unsigned char* jpegBuf = NULL;  // 定义了一个unsigned char类型的指针
// 打开一个文件，返回指向该文件的指针
if ((jpegFile = fopen(path, "rb")) == NULL) {
    printf("open input file failure\n");
}
//ftell： 得到当前文件位置指针相对于文件首地址的偏移字节数 ，参数（1.文件指针）
//ftell返回当前文件指针的位置。这个位置是指当前文件指针相对于文件开头的位移量。
//fseek：设置文件指针stream位置， 参数（1.文件指针，2.编译量，3.指针基地址） 设置成功返回0
// 先将当前指针移动到文件最后， 然后返回当前指针位置，赋值给size，然后再移动到文件开头 SEEK_SET为文件开头。
if (fseek(jpegFile, 0, SEEK_END) < 0 || (size = ftell(jpegFile)) < 0 || fseek(jpegFile, 0, SEEK_SET) < 0) {
    printf("determining input file size failure\n");
}
if (size == 0) {
    printf("determining input file size, Input file contains no data\n");
}

jpegSize = (unsigned long)size;
// 动态分配一个内存区域
if ((jpegBuf = (unsigned char*)malloc(jpegSize * sizeof(unsigned char))) == NULL) {
    printf("allocating JPEG buffer\n");
}
//从文件流读取数据 ,如参（1，数据块指针（接收数据），2 单个数据大小， 3.数据个数 ， 4.文件指针）
// 成功读取的元素总数会以 size_t 对象返回，size_t 对象是一个整型数据类型。如果总数与 nmemb 参数不同，则可能发生了一个错误或者到达了文件末尾。
if (fread(jpegBuf, jpegSize, 1, jpegFile) < 1) {
    printf("reading input file");
}
//关闭文件流
fclose(jpegFile);
jpegFile = NULL;
```



### **jpeg读文件的逻辑**

先直接读，读的unsigned char类型， 存在jpegBuf。

然后对jpegBuf进行解码。得到图像信息，宽高尺寸，子采样，颜色空间等

然后将结构体内存的unsigned char类型的指针赋值给sw_out_buf,。

如果为空动态分配一块内存。

然后对jpegBuf进一步，将jpeg图像信息，解码到sw_out_buf中

再将sw_out_buf的值赋值给传进来的结构体的virt_addr.



### **代码区、常量区、静态区（全局区）、堆区、栈区？**

代码区：存放程序的代码，即CPU执行的机器指令，并且是只读的。
常量区：存放常量(程序在运行的期间不能够被改变的量，例如: 10，字符串常量”abcde”， 数组的名字等)
静态区（全局区）：静态变量和全局变量的存储区域是一起的，一旦静态区的内存被分配, 静态区的内存直到程序全部结束之后才会被释放

- 堆区：

​	由程序员调用malloc()函数来主动申请的，需使用free()函数来释放内存，若申请了堆区内存，之后忘记释放内存，很容易造成内存泄漏

堆区是调用malloc函数来申请内存空间，这部分空间使用完后需要调用free()函数来释放。
void * mallc(size_t);函数的输入是分配的字节大小，返回是一个void*型的指针，该指针指向分配空间的首地址，void *型指针可以任意转换为其他类型的指针。

- 栈区：

  栈区由编译器自动分配释放，存放函数的**参数值、返回值和局部变量**，在程序运行过程中实时分配和释放，栈区由操作系统自动管理，无须手动管理。栈区是先进后出原则，即先进去的被堵在屋里的最里面，后进去的在门口，释放的时候门口的先出去。



**动态分配内存区域记得free就行了。**

### 如何初始化类，如何调用类中的成员函数

new完需要delete。而new申请的对象，则只有调用到delete时再会执行析构函数，如果程序退出而没有执行delete则会造成内存泄漏。



### 几个头文件分别用到了哪些函数



以下几个都是c的常用库函数

- **stdio .h** 头文件定义了三个变量类型、一些宏和各种函数来执行输入和输出。

​		printf ， 宏NULL，EOF，文件操作FILE ， fopen，fseek等，

- **stdlib .h** 头文件定义了四个变量类型、一些宏和各种通用工具函数。

  free() , malloc()，qsort， abs

- **string .h** 头文件定义了一个变量类型、一个宏和各种操作字符数组的函数。

  memset()   memcpy 字符串比较查找赋值等。

- **stdint.h**是c99中引进的一个标准C库的头文件。

  调用uint8_t，uint16_t，uint32_t，uint32_t等类型时需要调用头文件#include <stdint.h>，而不能直接如同char，int一样直接调用。

对应的c++的几个常用库函数

- **#include <iostream>**
- \#include <algorithm>
- #include <cstring



### **模板， 智能指针，参数包**

```c++
template <typename T>
struct MakeUniqueResult {
  using scalar = std::unique_ptr<T>;
};

template <typename T>
struct MakeUniqueResult<T[]> {
  using array = std::unique_ptr<T[]>;
};

template <typename T, size_t N>
struct MakeUniqueResult<T[N]> {
  using invalid = void;
};

//同一个结构体名模板匹配不同的数据类型

//std::unique_ptr智能指针
template <typename T, typename... Args>
//typename 表明 MakeUniqueResult<T>::scalar 是类型
//表示 make_unique()函数返回类型为 MakeUniqueResult<T>::scalar

// Args... args为参数包传入函数
//通过通用引用(T&&)和std::forward使得函数将参数以其原始值类别传递给另一个函数
typename MakeUniqueResult<T>::scalar make_unique(Args &&... args) {  // NOLINT
  return std::unique_ptr<T>(new T(std::forward<Args>(args)...));  // NOLINT(build/c++11)
}

// 上面make_unique函数使用模板和可变参数接收任意数量和类型的参数，然后通过std::forward将这些参数以它们原始的形式传递给new T()这个 函数，这个函数是构造一个T类型的对象，并将其赋值给T类型的智能指针

```



### **explict**

关键字explicit

作用：只能用于修饰只有一个参数的类构造函数，表明该构造函数是显式的，类构造函数默认是implicit隐式的。可以阻止不应该允许的经过转换构造函数进行的隐式转换发生，避免不合适的类型转换。

使用建议：尽量所有单参数的构造函数都加explicit，极少数的拷贝构造函数可以不声明explicit。

只需要用于类内的单参数构造函数前面（除了第一个参数以外其他参数都有默认值的时候，explicit也有效）。由于无参数的构造函数和多参数的构造函数总是显式调用，加explict无意义。

### main函数的参数 argc 和 argv

一般入门C或者C++基础知识时，主函数都是直接用的下面形式：

```cpp
#include<iostream>
using namespace std;

int main(){
   cout<<"hello world"<<endl;
   return 0;
}
```

而在C++标准中，其实main函数的主要形式有：

```cpp
int main(void);
int main(int argc,char *argv[])// 等于 int main(int argc,char **argv);
```

这两个参数主要是用来保存程序运行时传递给main函数的命令行参数的。

- **argc：是argument count 的缩写，保存运行时传递给main函数的参数个数。**

- **argv：是argument vector 的缩写，保存运行时传递main函数的参数，类型是一个字符指针数组，每个元素是一个字符指针，指向一个命令行参数。**

argv[0]指向程序运行时的全路径名；

argv[1] 指向程序在命令行中执行程序名后的第一个字符串；

argv[2] 指向程序在命令行中执行程序名后的第二个字符串；

以此类推直到argv[argc]......

argv[argc] 在C++中指向nullptr，在C语言中指向NULL。



### 深拷贝和浅拷贝的区别

默认的拷贝行为一般是浅拷贝，它将原始对象中所在内存中的数据按照二进制位复制到 目标对象所在的内存。但是当该对象存在其他资源，比如动态分配的内存、指向其他数据的指针等，浅拷贝无法 正确的拷贝这些资源，需要显式的定义拷贝构造函数，以完整地拷贝对象的所有数据。

深拷贝它除了会将原有对象的所有成员变量拷贝给新对象，还会为新对象再分配一块内存，并将原有对象所持有的内存也拷贝过来。这样做的结果是，原有对象和新对象所持有的动态内存是相互独立的，更改一个对象的数据不会影响另外一个对象。

这种将对象所持有的其它资源一并拷贝的行为叫做深拷贝，我们必须显式地定义拷贝构造函数才能达到深拷贝的目的。

### this指针

在每个成员函数中都包含一个特殊的指针，这个指针的名字是固定的，称为this。它是指向本类对象的指针，它的值是当前被调用的成员函数所在的对象的起始地址。

this指针是隐式使用的，作为参数被传递给成员函数

```c++
// 程序中定义的成员函数
int Box::volume()
{
	return (x*y*z);
}
// C++编译器处理为
int Box::volume(Box * this)
{
	return (this->x * this->y * this->z);
}
// 在调用成员函数a.volume时，实际上时用以下方式调用
a.volume(&a);	// 将对象a的地址传递给形参this，然后按this指向去引用各成员
```



### 如何接收传出的结构体指针。是否需要初始化内存。

接收传出的结构体指针，需要声明一个结构体指针变量，不需要初始化内存，只需要将传出的指针赋值给该变量。但是要记得释放该指针变量指向的内存区域。



### **结构体和类的初始化和内存释放**

https://blog.csdn.net/XZ2585458279/article/details/124716701

**结构体内参数的初始化**

```
typedef struct {
    int id;
    int count;
    object_detect_result results[OBJ_NUMB_MAX_SIZE];
} object_detect_result_list;
```

消除上面的宏OBJ_NUMB_MAX_SIZE， 通过传入变量来定义

```c++
//ref:  https://blog.csdn.net/woxincd/article/details/6214246
#include <stdio.h>   
#include <stdlib.h>   
#include <string.h>   
  
struct student{   
  char *name;   
  int score;   
  struct student* next;   
}stu,*stu1;    
  
int main(){    
  stu.name = (char*)malloc(sizeof(char)); /*1.结构体成员指针需要初始化*/  
  strcpy(stu.name,"Jimy");   
  stu.score = 99;   
  
  stu1 = (struct student*)malloc(sizeof(struct student));/*2.结构体指针需要初始化*/  
  stu1->name = (char*)malloc(sizeof(char));/*3.结构体指针的成员指针同样需要初始化*/  
  stu.next  = stu1;   //结构体中的指针也要初始化，这里将另一个指针地址赋值给它了
  strcpy(stu1->name,"Lucy");   
  stu1->score = 98;   
  stu1->next = NULL;   //结构体中的指针也要初始化，这里赋值为NULL
  printf("name %s, score %d /n ",stu.name, stu.score);   
  printf("name %s, score %d /n ",stu1->name, stu1->score);   
  free(stu1);   
  return 0;   
}  
```



### 结构体定义的5中方式

结构体就是一个可以包含不同数据类型的一个结构，它是一种可以自己定义的数据类型。首先，结构体可以在一个结构中声明不同的数据类型；第二，相同结构的结构体变量是可以相互赋值的。
下面是定义结构体的五种方式：

第一种：

```
struct Student
{
	std::string strName;
	std::string strClass;
	double dScore;
};
```


声明1：

```
struct Student stu;
stu.name="zhangsan";
stu.score=99;
```

声明2：

```
Student stu;
stu.name="zhangsan";
stu.score=99;
```


第二种：

```
struct Student
{
	std::string strName;
	std::string strClass;
	double dScore;
}Stu;
```


第二种与第一种相比，多了Stu。Stu是定义的一个结构体实例化对象，相当于第一种struct Student stu中的stu。

```
声明：
//这种方式已有实例化对象，也可以根据第一种创建新的对象。
赋值：
//已有实例，所以直接赋值即可
Stu.name="zhangsan";
Stu.score=99;
```


第三种：

```
struct 
{
	std::string strName;
	std::string strClass;
	double dScore;
}Stu;
```


无名定义，且定义了一个结构体实例化对象Stu，赋值方式同第二种。

第四种：

```
typedef struct Student
{
	std::string strName;
	std::string strClass;
	double dScore;
}Stu;
```


重定义结构体，这里使用了typedef关键字，此关键字的作用就是声明数据类型的别名，所以类型为struct Student，别名为Stu。

```
声明1：
//同第一种
声明2：
Stu stu1;//以结构体别名声明一个结构变量
```


第五种：

```
typedef struct
{
	std::string strName;
	std::string strClass;
	double dScore;
}Stu;
```


重定义结构体，类型为Stu

声明：

```
Stu stu

```

ref：https://blog.csdn.net/weixin_42326676/article/details/122997960



### **结构体初始化后其中的原始变量是什么状态， 其中的指针需要手动释放？**

和外面初始化变量没区别，其中指针不会自动分配内存区域，需求手动申请和释放。



### 结构体的拷贝

**结构体深拷贝 :** 如果要实现结构体的深拷贝 , 需要在 浅拷贝 的基础上 , 重新为 指针 在堆内存中分配数据 ;

```c++
/**
 * @brief copy_student 执行深拷贝操作
 * @param to
 * @param from
 */
void copy_student(Student *to, Student *from)
{
    // 结构体内存拷贝
    // 该拷贝是浅拷贝
    memcpy(to, from, sizeof (Student));

    // 结构体直接赋值 , 与上面的代码作用相同
    // 该拷贝也是浅拷贝
    //*to = *from;


    // 重新为 address 分配内存
    to->address = (char *)malloc(20);

    // 将 from 中的地址字符串数据 拷贝到 to 中
    strcpy(to->address, from->address);
}

```



### cmake关键字的使用

set_target_properties()



file(GLOB_RECURSE ROOT_SRC_FILES

​    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.c

​    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cc

​    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp

)

list(APPEND SRC_FILES ${ROOT_SRC_FILES})

AUX_SOURCE_DIRECTORY





### **cmake install配置**

### cmake配置交叉编译

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wl,--allow-shlib-undefined -ldl")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wl,--allow-shlib-undefined -ldl")





for循环中， 定义了一个指针变量，比如结构体指针变量，怎样释放资源。

c++ 异常时返回null的方式，处理错误的方式。

编译器差异导致的代码执行结果差异.交叉编译器的理解。

同样的代码，同样的cmakelist文件和编译脚本，3568上编译和本地交叉编译结果不一样。



### 模板函数。类模板。

### long long 类型

**回调函数**

回调函数的定义和使用。

回调函数的好处。

回调函数应用场景。



### override关键字

如果派生类在虚函数声明时使用了override描述符， 那么该函数必须重载其基类中的同名函数，否则代码将无法通过编译。

override明确地表示一个函数是对基类中一个[虚函数](https://so.csdn.net/so/search?q=虚函数&spm=1001.2101.3001.7020)的重载。更重要的是，它会检查基类虚函数和派生类中重载函数的签名不匹配问题。如果签名不匹配，编译器会发出错误信息。

override表示**函数应当重写基类中的虚函数(用于派生类的虚函数中)。**

### 返回局部变量指针问题



### 多个转换运算符之间的差异

static_cast

const_cast

reinterpret_cast

### #ifdef __cplusplus extern “C”

extern "C"的主要作用就是为了能够正确实现C++代码调用其他C语言代码。加上extern "C"后，会指示编译器这部分代码按C语言的进行编译，而不是C++的。由于C++支持函数重载，因此编译器编译函数的过程中会将函数的参数类型也加到编译后的代码中，而不仅仅是函数名；而C语言并不支持函数重载，因此编译C语言代码的函数时不会带上函数的参数类型，一般之包括函数名。

\#ifdef __cplusplus //而这一部分就是告诉编译器，如果定义了__cplusplus(即如果是cpp文件， extern "C"{ //因为cpp文件默认定义了该宏),则采用C语言方式进行编译

由于C、C++编译器对函数的编译处理是不完全相同的，尤其对于C++来说，支持函数的重载，编译后的函数一般是以函数名和形参类型来命名的。

例如函数void fun(int, int)，编译后的可能是（不同编译器结果不同）_fun_int_int(不同编译器可能不同，但都采用了类似的机制，用函数名和参数类型来命名编译后的函数名)；而C语言没有类似的重载机制，一般是利用函数名来指明编译后的函数名的，对应上面的函数可能会是_fun这样的名字。



extern "C"包含双重含义，从字面上可以知道，首先，被它修饰的目标是"extern"的；其次，被它修饰的目标代码是"C"的。

- extern是C/C++语言中表明函数和全局变量的作用范围的关键字，该关键字告诉编译器，其申明的函数和变量可以在本模块或其他模块中使用。extern对应的关键字是static，static表明变量或者函数只能在本模块中使用，因此，被static修饰的变量或者函数不可能被extern C修饰。

- 被extern "C"修饰的变量和函数是按照C语言方式进行编译和链接的。

### #pragma once与#ifndef #define #endif的异同

1、#pragma once和起到和#ifndef #define #endif的相同点

他们都可以做到防止头文件的内容被重复包含的作用

2、#pragma once和起到和#ifndef #define #endif的不同点

#ifndef #define #endif受C/C++标准的支持，不受编译器的任何限制
较老的编译器不支持#pragma once，如gcc 3.4，兼容性不够好
#ifndef #define #endif可以针对一个文件的部分代码，而#pragma once只能针对整个文件
