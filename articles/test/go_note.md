# GoLang

入门和理解

## 安装go编译环境

```bash
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt update
sudo apt install golang-go
```

检查go 安装版本

```bash
go version   
```

## hello world

1.

新建项目目录，初始化包

```bash
mkdir hello && cd hello
go mod init example/hello
```

在hello/目录下生成了一个`go.mod`文件, 用来管理包依赖.

>  go.mod文件通过哈希值来标记每个依赖包的版本，在构建过程中go命令会下载go.mod中的依赖包，下载的依赖包会缓存在本地，以便下次构建。

2.

创建文件，编译运行

```bash
touch hello.go
```

编辑，添加代码:

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

1. 新建了一个`main`的包. 
2. 导入了`fmt`的标准库,.

```bash
go run .
```

输出结果。

3.

编译可执行文件输出到当前目录下，并运行

```bash
go build -o hello # 执行完当前目录生成hello 可执行文件
./hello
```



## 调用外部包

修改hello.go的代码为如下：

```go
package main

import "fmt"
import "github.com/mazeyqian/asiatz"

func main() {
    fmt.Println("Hello, World!")
    utcTime, err := asiatz.ShanghaiToUTC("10:00")
    if err != nil {
         fmt.Println("Error")
         return
    }
    fmt.Println("UTC Time:", utcTime) // Output: 02:00
}
```

然后执行：

```
go mod tidy
```

执行完会输出如下：

```
go: finding module for package github.com/mazeyqian/asiatz
go: found github.com/mazeyqian/asiatz in github.com/mazeyqian/asiatz v1.1.3
```

表明其自动寻找到了外部依赖包 。

此外，当前目录下会生成一个go.sum的文件，其用于记录每个依赖包的哈希值。

go.mod文件的内容也发生了变换，添加了新的依赖项。

编译运行

```
go run .
```

输出：

```
Hello, World!
UTC Time: 02:00
```

## Emm

### go env

`go env` 命令查看当前go环境变量

###  **go modules**

只有启用了`go modules` 模式才能执行 go module相关命令，如`go mod init 项目名称`, `go mod tidy`等

```bash
# 设置go module为开启状态
go env -w GO111MODULE=on 

## GOPROXY的默认值为https://proxy.golang.org，最好设为国内代理
go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct
```

- GO111MODULE 设置为 on，表示使用` go modules `模式。go v1.13之后默认开启 go module.

   开启后将会使用模块查找依赖包的方法（go.mod），而不会在GOPATH目录下查找。代码文件也就可以放置在GOPATH/src外的任何目录下。

- 设置代理，防止包下载失败

> go module是类似于java中的maven,是包的管理工具，在没有这个go module之前，都是配置本地的GOPATH，创建的每个项目也都必须创建在这个GOPATH的src目录下，且项目的go文件不能重名
>
> **`GO111MODULE`**:默认是为空，有三个值，on（开启）、off（关闭）、auto（自动）

god mod常用命令

```bash
go mod init  # 初始化go.mod
go mod tidy  # 更新依赖文件
go mod download  # 下载依赖文件
go mod vendor  # 将依赖转移至本地的vendor文件
go mod edit  # 手动修改依赖文件
go mod graph  # 打印依赖图
go mod verify  # 校验依赖
go mod help # go mod 帮助
```

### go mod tidy

`go mod tidy`此命令会自动分析项目中的所有代码，更新 `go.mod` 和 `go.sum` 文件，确保它们与实际代码使用的依赖项一致。它主要有以下功能：

- 移除未使用的依赖项：从 go.mod 文件中删除那些在代码中不再使用的依赖项。
- 添加缺失的依赖项：添加代码中使用但尚未记录在 go.mod 文件中的依赖项。
- 更新 go.sum 文件：确保 go.sum 文件中包含所有依赖项的正确校验和。

### go.mod 和go.sum 文件

**go.sum的作用以及为什么要把go.mod和go.sum分开**
为了确保一致性构建，Go引入了go.mod文件通过哈希值来标记每个依赖包的版本，在构建过程中go命令会下载go.mod中的依赖包，下载的依赖包会缓存在本地，以便下次构建。

考虑到下载的依赖包有可能是被黑客恶意篡改的，以及缓存在本地的依赖包也有被篡改的可能，单单一个go.mod文件并不能保证一致性构建。

为了解决Go module的这一安全隐患，Go开发团队在引入go.mod的同时也引入了go.sum文件，用于记录每个依赖包的哈希值。

在构建时，如果本地的依赖包hash值与go.sum文件中记录得不一致，则会拒绝构建。

因此，该文件记录了每个依赖模块的校验和，用于确保依赖的安全性和可重现性。在执行 go build 或 go run 时，Go 会检查 go.sum 文件以确保依赖的完整性。

同时，由于这两个文件分别负责不同的分工：区分模块信息和依赖校验信息，来确保项目的依赖管理的准确性和安全性，要把它们放在不同的文件。



ref:

https://github.com/xinliangnote/Go



## 语法

简单介绍了解大概，目的是能读懂代码，记和其他语言的差异处。

**适用场景：**

1. 并发执行任务
协程可以非常方便地启动大量的任务并发执行，提高程序的性能和吞吐量。在计算密集型的任务中，可以利用多个协程进行并行计算，加快任务的执行速度。在IO密集型的任务中，可以通过协程来并发处理多个IO操作，提高程序的响应能力。

2. 高并发服务器
协程非常适合用于构建高并发的服务器程序。通过协程和通道，可以实现高效的并发编程模型。每个客户端连接可以对应一个协程，这样可以同时处理多个客户端请求，提高服务器的并发处理能力。

3. 异步IO操作
协程可以很方便地处理异步IO操作。通过协程和通道，可以实现非阻塞的IO操作，并在IO操作完成后通知相应的协程继续执行。这样可以避免在IO操作上浪费过多的时间，提高程序的响应速度。

### 变量

```go
var age int // 没有初始化就为零值
var a string = "abc" // 声明一个变量并初始化
var a = "abc" // 声明一个变量并初始化，根据值自行判定变量类型。

var b, c int = 1, 2
//方式一:声明并初始化，一般用于声明全局变量
var  level int =  1 

//方式二:短变量声明并初始化，一般是用于声明局部变量
// 如果变量已经使用 var 声明过了，再使用 := 声明变量，就产生编译错误
i := 1  //声明一个变量 i 其初始值为1

//相当于
var i int
i = 1

//批量声明
var (
    a int
    b string
    c []float32
)
```

### 指针

```go
package main

import "fmt"

func main() {
   var a int= 20   /* 声明实际变量 */
   var ip *int        /* 声明指针变量 */

   ip = &a  /* 指针变量的存储地址 */

   fmt.Printf("a 变量的地址是: %x\n", &a  )

   /* 指针变量的存储地址 */
   fmt.Printf("ip 变量储存的指针地址: %x\n", ip )

   /* 使用指针访问值 */
   fmt.Printf("*ip 变量的值: %d\n", *ip )
}
```

`&`取出地址，`*`根据地址取出地址指向的值

### 函数

func function_name( [parameter list] ) [return_types] {
   函数体
}

```go
package main

import "fmt"

func swap(x, y string) (string, string) {
   return y, x
}

func main() {
   a, b := swap("Google", "Runoob")
   fmt.Println(a, b)
}
```

### 数组和切片

创建数组

```go
var numbers [5]int
var numbers = [5]int{1, 2, 3, 4, 5}
numbers := [5]int{1, 2, 3, 4, 5}
balance := [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
```

数组遍历和访问

```go
package main

import "fmt"

func main() {
   var i,j,k int
   // 声明数组的同时快速初始化数组
   balance := [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}

   /* 输出数组元素 */         ...
   for i = 0; i < 5; i++ {
      fmt.Printf("balance[%d] = %f\n", i, balance[i] )
   }
   
   balance2 := [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
   /* 输出每个数组元素的值 */
   for j = 0; j < 5; j++ {
      fmt.Printf("balance2[%d] = %f\n", j, balance2[j] )
   }

   //  将索引为 1 和 3 的元素初始化
   balance3 := [5]float32{1:2.0,3:7.0}  
   for k = 0; k < 5; k++ {
      fmt.Printf("balance3[%d] = %f\n", k, balance3[k] )
   }
}
```



切片可以理解为动态数组，与数组相比切片的长度是不固定的。

创建切片

```go
//声明一个未指定大小的数组来定义切片
var identifier []type
//或使用 make() 函数来创建切片
var slice1 []type = make([]type, len)
//也可以简写为
slice1 := make([]type, len) //len为切片初始长度
//将 arr 中从下标 startIndex 到 endIndex-1 下的元素创建为一个新的切片。
s := arr[startIndex:endIndex] 
```

### map

无序键值对集合

```go
// 创建一个空的 Map
m := make(map[string]int)

// 创建一个初始容量为 10 的 Map
m := make(map[string]int, 10)

// 使用字面量创建 Map
m := map[string]int{
    "apple": 1,
    "banana": 2,
    "orange": 3,
}

// 获取键值对
v1 := m["apple"]
v2, ok := m["pear"]  // 如果键不存在，ok 的值为 false，v2 的值为该类型的零值

// 获取 Map 的长度
len := len(m)

// 遍历 Map
for k, v := range m {
    fmt.Printf("key=%s, value=%d\n", k, v)
}

// 删除键值对
delete(m, "banana")
```



### range

https://www.runoob.com/go/go-range.html

```go
package main

import "fmt"

// 声明一个包含 2 的幂次方的切片
var pow = []int{1, 2, 4, 8, 16, 32, 64, 128}

func main() {
   // 遍历 pow 切片，i 是索引，v 是值
   for i, v := range pow {
      // 打印 2 的 i 次方等于 v
      fmt.Printf("2**%d = %d\n", i, v)
   }
}
```

输出：

```
2**0 = 1
2**1 = 2
2**2 = 4
2**3 = 8
2**4 = 16
2**5 = 32
2**6 = 64
2**7 = 128
```

## cgo

### 简单调用c动态库的例子

**1.先用c写个简单的库**

mylib.h

```c
#ifndef MYLIB_H
#define MYLIB_H

#ifdef __cplusplus
extern "C" {
#endif

int add(int a, int b);

#ifdef __cplusplus
}
#endif

#endif // MYLIB_H
```

mylib.c

```c
#include <stdio.h>

int add(int a, int b) {
  return a+b;
}
```

编译，编译完生成动态库libmylib.so

```bash
gcc -fPIC -shared -o libmylib.so mylib.c
```

创建一个c文件测试该库

mylib_test.c

```c
#include <stdio.h>
#include "mylib.h"

int main() {
  int c = add(1,2);
  printf("sum is :%d \n",c);
  return 0;
}
```

编译，运行

```bash
gcc mylib_test.c -L./ -lmylib -o test.out
./test
```

可成功输出结果，说明库生成正确。



**2.创建go项目并调用库**

cgo_test.go

```go
package main

/*
#cgo LDFLAGS: -L. -lmylib
#include "mylib.h"
*/
import "C"
import "fmt"
func main() {
    c := C.add(100, 100)
    fmt.Printf("sum is %d ",c)
}
```

编译，运行, 可以看到输出打印结果。

```bash
go mod init cgo_test
go mod tidy
go build cgo_test.go
./cgo_test
```

项目的目录结果大致如下：

```bash
├── cgo_demo		# go 项目，库调用测试
│   ├── cgo_demo.go
│   ├── go.mod
│   ├── libmylib.so	# 拷贝自mylib
│   └── mylib.h		# 拷贝自mylib
└── mylib		# c 项目，生成库
    ├── libmylib.so	# 生成的动态库
    ├── mylib.c
    ├── mylib.h
    ├── mylib_test.c
    └── test.out	# 生成的可执行文件
```



ref:

https://github.com/chai2010/gopherchina2018-cgo-talk/blob/master/index.md

https://www.jianshu.com/p/74987c2e984a

## 微服务

常用的Go微服务框架：

- **Gin**：一个轻量级的Web框架，提供了高性能的HTTP路由和中间件机制。
- **Echo**：另一个高性能的Web框架，支持丰富的中间件和插件，易于扩展。
- **Go Micro**：专为微服务设计的框架，提供了服务发现、负载均衡、消息传递等一整套微服务架构的解决方案。

在选择Go微服务框架时，开发者需要综合考虑项目需求、团队技能水平和性能要求。以下是一些选择指南：

- **Gin**：适合需要高性能和简洁API的项目，特别是小型和快速迭代的应用。
- **Echo**：适合需要高性能和丰富功能的项目，特别是中大型和企业级应用。
- **Go Micro**：适合需要完整微服务架构解决方案的项目，特别是复杂的分布式系统和大规模微服务架构。

### echo demo easy

下面脚本测试echo的get post方法。

使用`go build echo_simple.go`编译.`./echo_simple`运行。

在浏览器访问`http://localhost:8080/index`进行请求。或者使用`curl`命令

test3 使用命令`curl -d "name=zsl" -d "email=zsl@go.com" http://localhost:8080/index`

```go
//echo_simple.go
package main

import (
	"fmt"
	"github.com/labstack/echo/v4"
    "net/http"
	)

// test 1 : get
func main(){
    e := echo.New()
    fmt.Println("echo 框架测试")
    // Get func
    e.GET("/index", func(c echo.Context) error{
        return c.String(200, "helloworld")
    })

    // start server
    e.Start(":8080")
}


// // test 2: get func
// func main(){
//     e := echo.New()
//     fmt.Println("echo 框架测试")
//     // Get func
//     e.GET("/index", getQueryParam)
//     // start server
//     e.Logger.Fatal(e.Start(":8080"))
// }
// func getQueryParam(c echo.Context) error {
// 	id := "666"
// 	name := "zsl"
// 	return c.String(200, "user id:"+id+" name:"+name)
// }


// // test3: post
// // curl -d "name=zsl" -d "email=zsl@go.com" http://localhost:8080/index
// func main() {
// 	e := echo.New()
//  fmt.Println("echo 框架测试")
// 	e.POST("/index", save)
// 	e.Logger.Fatal(e.Start(":8080"))
// }

// func save(c echo.Context) error {
// 	// Get name and email
// 	name := c.FormValue("name")
// 	email := c.FormValue("email")
// 	return c.String(http.StatusOK, "name:"+name+", email:"+email)
// }

```

### echo demo hard

该脚本创建了一个服务，实现参数请求，然后调用一个本地动态库中的函数实现目标检测，最后将检测结果返回客户端。

app.go

```go
package main

/*
#cgo LDFLAGS: -L./ -ldroneobb -lstdc++
#cgo CPPFLAGS: -I ../include -I /usr/include -I /usr/local/include
#cgo CFLAGS: -std=gnu11
#include<stdio.h>
#include<stdlib.h>
#include"wrapobb.h"
*/
import "C"
import (
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
	"time"
	"unsafe"
)

type Object struct {
	p unsafe.Pointer
}

type Param struct {
	Image     string  `json:"image"`
	Height    float32 `json:"height"`
	Latitude  float32 `json:"latitude"`
	Longitude float32 `json:"longitude"`
	Angle     float32 `json:"angle"`
	Flag      int     `json:"flag"`
}

func NewModel(enginePath string, deviceId int) *Object {
	path := C.CString(enginePath)
	obj := &Object{p: C.yolo(path, C.int(deviceId))}
	C.free(unsafe.Pointer(path))
	return obj
}

func detect(m *Object, img string, score, iou, height, latitude, longitude, angle float32, flag int) string {
	base64 := C.CString(img)
	res := C.detect(m.p, base64, C.float(score), C.float(iou), C.float(height), C.float(latitude), C.float(longitude), C.float(angle), C.int(flag))
	result := C.GoString(res)
	C.free(unsafe.Pointer(base64))
	C.free(unsafe.Pointer(res))
	return result
}

func release(m *Object) {
	C.release(m.p)
}

func main() {
	model := NewModel("./ckpts/obb.engine", 0)
	defer release(model)
	e := echo.New()
	var start time.Time
	//param := new(Param)
	e.POST("/obb", func(c echo.Context) error {
		param := new(Param)
		if err := c.Bind(param); err != nil {
			return c.String(http.StatusBadRequest, "{'msg','invalid param!'}")
		}
		start = time.Now()
		result := detect(model, param.Image, 0.2, 0.4, param.Height, param.Latitude, param.Longitude, param.Angle, param.Flag)
		log.Printf("time: %s,draw flag: %v height: %v infer cost: %s \n", start, param.Flag, param.Height, time.Since(start))
		return c.String(http.StatusOK, result)
	})

	e.GET("/health", func(c echo.Context) error {
		return c.String(http.StatusOK, "OK")
	})
	log.Fatal(e.Start(":1323"))
}

```

## End

ref：

https://go.dev/doc/

https://www.runoob.com/go/go-tutorial.html

https://github.com/xinliangnote/Go.git

[GO PDF资源 汇总](https://blog.csdn.net/weixin_33862188/article/details/92619815)