# IOS开发环境

## 开发版本问题

**Xcode 版本， macOS版本， 支持的Swift版本， 以及支持的macOS，IOS, watchOS, tvOS, visionOS的版本对应关系：**

https://xcodereleases.com/

查看支持的版本并下载，否则会出现不兼容，此外不同的Xcode项目文件在不同的Xcode软件上也会出现不支持，需要修改项目包中的版本。

 iOS SDK 已经集成于 Xcode 中，可直接进行开发，但是如果要在真机上运行，一定得看真机的IOS版本号， 保证当前开发环境的macOS版本和Xcode的版本能支持该IOS版本。

**真机iOS版本号查看**

`真机->设置->通用->关于本机->iOS版本`  比如：17.1.2

**开发用的mac查看macOS版本号**

左上角苹果标志-> 关于本机。 比如：`macOS Catalina 10.15.6`, `macOS Monterey 12.4`等



## 项目中的文件说明

- 每个xcode项目下都会有一个`.xcodeproj`后缀的文件，双击会打开该xcode项目。

- `Base.lproj`和下面的`.storyboard`是什么?  界面设计器。

- `Assets.xcassets `文件夹用于存放资源文件，比如图片。该目录下的两个文件夹：

  `AccentColor.colorset` 

  AppIcon.appiconset `该目录为app图标的配置文件。

- `Info.plist` 文件？`information property list file`（属性列表文件），简称 `Info.plist`。

  Info.plist可用来构建任意数据，这些数据在运行时是可访问的。Info.plist是每个bundle的专属配置，Info.plist文件中的keys和values描述了许多要应用于该bundle的行为以及配置选项。**Xcode工程通常会自动创建一个Info.plist，并且提供许多合适的keys以及其对应的默认的values**。我们可以修改或增加keys和values。

- 如何配置框架。

  比如添加opencv框架，直接到去下载编译好的框架[opencv2.framework](https://github.com/nihui/opencv-mobile/releases) 或者[opencv原版](https://opencv.org/releases/) ,然后将`.framework`文件夹拖到xcode项目中

- 关于单元测试和UI测试

​		在创建项目时， 选择`include Tests` 后项目会自动生成两个文件夹及文件， `projnameTests`和`projnameUITests`。这两个文件项目中不是必要的，可以删		掉，如果需要进行单元测试和UI测试可以留着使用。

## IOS开发的背景了解

NEXTSTEP为NeXT创新的面向对象操作系统。NeXT电脑公司（随后更名为NeXT软件公司）是一间设立在美国加利福尼亚州红木城的电脑公司，专门制造和开发高等教育和商业市场上的工作站电脑。NeXT是由苹果公司（当时称为苹果电脑）的创办人史蒂夫·乔布斯于1985年被苹果公司辞退后同年成立。****

Cocoa 是从1980年代由 NeXT 开发的编程环境NeXTSTEP 和 OPENSTEP 演变而来。Cocoa（IOS上的叫Cocoa Touch）是一个面向对象的软件组件—---类的集成套件，它使开发者可以快速创建强壮和全功能的 Mac OS X （IOS）应用程序。

Cocoa包含了很多框架，其中最最核心的有两个：
（1）Foundation框架；

Foundation框架包含所有和界面显示无关的类。首先出现在OpenStep中。在Mac OS X中，它是基于Core Foundation的。作为通用的面向对象的函数库，Foundation提供了字符串，数值的管理，容器及其枚举，分布式计算，事件循环，以及一些其它的与图形用户界面没有直接关系的功能。其中用于类和常数的“NS”前缀来自于NeXTSTEP。它可以在Mac OS X和iOS中使用。
（2）Application Kit（AppKit）框架（Cocoa Touch中叫UIKit框架）。

Application Kit框架包含实现图形的、事件驱动的用户界面需要的所有对象:窗口、对话框、按键、菜单、滚动条、文本输入框。。

“应用程序工具包”，或称AppKit（Application Kit）是直接衍生自NeXTSTEP的AppKit的。它包含了程序与图形用户界面交互所需的代码。它是基于Foundation建立的，也使用“NS”前缀。它只能在Mac OSX中使用。

“用户界面工具包”，或称UIKit（User Interface Kit），是用于iOS的图形用户界面工具包。与AppKit不同，它使用“UI”的前缀。



# Object C

- `#import `  底层会先判断这个文件是否被包含，如果被包含会忽略，否则才会包含。

- Foundation框架， 该框架中提供了一些最基础的功能，输入和输出和一些数据类型。`#import <Foudation/Foundation.h>`
- 字符串，分为C字符串和OC字符串。 有@前缀的为OC字符串 `NSString*str= @“java”;`
- OC程序的编译，链接和执行。
  1. 代码格式， 编写符合语法规范的OC源代码：`.m`文件 和`.h`文件
  2. 编译，编译为目标文件 `cc -c xx.m`  过程包含了：预处理，语法检查，编译。 最终生成`.o`文件。
  3. 链接， `cc xx.o` 如果使用了框架中的函数或类，那么链接时需指定`cc xx.o -framework frameworkname`
  4. 执行，链接后生成了`.out`可执行文件， 可直接运行。

- 类的定义

  1.类的声明

  2.类的实现

```objective-c
#import <Foundation/Foundation.h>
// 声明
@interface Person : NSObject
{
	NSString *_name;
    int _age;
}
- (void)run;
- (void)eatWithFood:(NSString *)foodName;
- (int)sunWithNum1:(int) num1 andNum2:(int)num2;
@end
// 实现
@implementation Person
- (void)run
{
    NSLog(@"i am running");
}
- (void)eatWithFood:(NSString *)foodName
{
    NSLog(@"i am eating", foodName);
}
- (int)sumWithNum1:(int)num1 andNum2:(int)num2
{
    int num3 = num1+num2;
    return num3;
}
@end
   
int main()
{
    // 调用
    Person *p1 = [Person new];
    [p1 eatWithFood:@"hanbaobao"];
    int sum = [p1 sumWithNum1:10 andNum2:20];
}
```

- 

# Swift

如果创建的是 OS X playground 需要引入 Cocoa ：

如果我们想创建 iOS playground 则需要引入 UIKit :

我们可以使用 **import** 语句来引入任何的 Objective-C 框架（或 C 库）到 Swift 程序中。例如 **import cocoa** 语句导入了使用了 Cocoa 库和API，我们可以在 Swift 程序中使用他们。

Cocoa 本身由 Objective-C 语言写成，Objective-C 又是 C 语言的严格超集，所以在 Swift 应用中我们可以很简单的混入 C 语言代码，甚至是 C++ 代码。



## 语法特性

1.swift注释与C一致 ,// /**/, 但是可以使用多行注释嵌套，Swift 的多行注释可以嵌套在其他多行注释内部。

2.不要求在每行语句的结尾使用分号(;)，但当你在同一行书写多条语句时，必须用分号隔开：



3.打印变量输出

```swift
print("\(name)的官网地址为：\(site)")
var A = 10
var B = 20
print("A + B 结果为：\(A + B)")
```



4.可选（Optional）类型，用于处理值缺失的情况。可选表示"那儿有一个值，并且它等于 x "或者"那儿没有值"。

**可选类型在声明时候使用`?` ， 获取值时使用`!`。**

以下两种声明是相等的：

```swift
var optionalInteger: Int?
var optionalInteger: Optional<Int>
```

如果一个可选类型的实例包含一个值，你可以用后缀操作符 ！来访问这个值，如下所示：

```swift
optionalInteger = 42
optionalInteger! // 42
```

> 使用`!`来获取一个不存在的可选值会导致运行时错误。使用`!`来强制解析值之前，一定要确定可选包含一个非`nil`的值。



5.

```swift
let vnModel = try VNcoreMLModel(for:model)
```





6.

常量使用关键字 **let** 来声明；

变量使用关键字 **var** 来声明；



7.

for 循环

```swift
//
for index in 1...5 {
    print("\(index) 乘于 5 为：\(index * 5)")
}

//
var someInts:[Int] = [10, 20, 30]
for index in someInts {
   print( "index 的值为 \(index)")
}

// 
for value in array[1..<array.count] {
    if value < currentMin {
        currentMin = value
    } else if value > currentMax {
        currentMax = value
    }
}

//
for _ in 1..<b {
    res = res * a
}

```



8。

```swift
// 使用字符串字面量
var stringA = "Hello, World!"
// String 实例化
var stringB = String("Hello, World!")


//Swift 的字符是一个单一的字符字符串字面量，数据类型为 Character。
//Swift 中不能创建空的 Character（字符） 类型变量或常量
let char1: Character = "A"

```

9.

数组

```swift
var someInts = [Int]()  // 空数组
var someInts:[Int] = [10, 20, 30]
var someInts = [Int](repeating: 10, count: 3)  //  长度为3,初始值10的数组
var someVar = someInts[0]
someInts.append(30)
someInts += [40]
```

10.

函数，关键字 func

```
func funcname() -> datatype {
   return datatype
}
```

返回一个





如下函数返回一个元组，如果你不确定返回的元组一定不为nil，那么你可以返回一个可选的元组类型。你可以通过在元组类型的右括号后放置一个问号来定义一个可选元组，例如(Int, Int)?或(String, Int, Bool)?

```swift
import Cocoa

func minMax(array: [Int]) -> (min: Int, max: Int)? {
    if array.isEmpty { return nil }
    var currentMin = array[0]
    var currentMax = array[0]
    for value in array[1..<array.count] {
        if value < currentMin {
            currentMin = value
        } else if value > currentMax {
            currentMax = value
        }
    }
    return (currentMin, currentMax)
}
if let bounds = minMax(array: [8, -6, 2, 109, 3, 71]) {
    print("最小值为 \(bounds.min)，最大值为 \(bounds.max)")
}

```



```swift
//可变参数通过在变量类型名后面加入（...）的方式来定义。

import Cocoa

func vari<N>(members: N...){
    for i in members {
        print(i)
    }
}
vari(members: 4,3,5)

```

11.下标脚本 关键字`subscript`

```swift
import Cocoa

struct subexample {
    let decrementer: Int
    subscript(index: Int) -> Int {
        return decrementer / index
    }
}
let division = subexample(decrementer: 100)

print("100 除以 9 等于 \(division[9])")
print("100 除以 2 等于 \(division[2])")
```



12.构造，析构，继承，重写

构造: **`init(){}`**

析构: **`deinit{}`**

重写：**override**

```swift
class StudDetails
{
    var mark1: Int;
    var mark2: Int;
    
    init(stm1:Int, results stm2:Int)
    {
        mark1 = stm1;
        mark2 = stm2;
    }
    
    func show()
    {
        print("Mark1:\(self.mark1), Mark2:\(self.mark2)")
        print("这是超类 SuperClass")
    }
}

class Tom : StudDetails
{
    init()
    {
        super.init(stm1: 93, results: 89)
    }
    override func show() {
        print("这是子类 SubClass")
    }
    
}

let tom = Tom()
tom.show()

```

防止类重写：通过在关键字class前添加**final**特性（final class）来将整个类标记为 final 的，这样的类是不可被继承的，否则会报编译错误。



13.

使用do catch处理异常

```swift
do {
　　var str = try testFunc(str: "three")
} catch MyError.one {
　　print("MyError.one")
} catch MyError.two {
　　print("MyError.two")
} catch let error as MyError {
　　print(error)
}

```



14.

类型检查使用 **is** 关键字。

向下转型，用类型转换操作符**(as? 或 as!)**

当你不确定向下转型可以成功时，用类型转换的条件形式(as?)。条件形式的类型转换总是返回一个可选值（optional value），并且若下转是不可能的，可选值将是 nil。只有你可以确定向下转型一定会成功时，才使用强制形式(as!)。当你试图向下转型为一个不正确的类型时，强制形式的类型转换会触发一个运行时错误。



15.

**try关键字**

举个栗子：将Json 反序列化为字典

```
 let dict = JSONSerialization.jsonObject(with: data, options: [])
```


大家都知道 将Json 反序列化为字典 不一定能成功，当然大家可以用可选绑定来处理 我们这里以try的三种形式分别来处理这个问题，方便理解try

- 解决方式一: 强行try (try!)

```
let dict = try! JSONSerialization.jsonObject(with: d, options: [])
```

存在的问题: 当请求结果不是标准的json数据时, 会造成程序崩溃 ，所以try! 需要确定一定能序列化成功才可使用， 类似as!

解决方式二: 可选try (try?)

```
let dict = try? JSONSerialization.jsonObject(with: d, options: [])
```


特点: 能反序列化成功, 就给你返回成功的值; 不能成功就给你返回nil

解决方式三: 默认try (try) 注意: 一定要配合 do{}catch{} 使用

    do{
        let dict = try JSONSerialization.jsonObject(with: d, options: [])
           print(dict)
    }catch{
       // catch 中默认提供error信息, 当序列化不成功是, 返回error
           print(error)
    }
只要do后面大括号中的代码抛出了异常, 就会执行catch
如果do后面大括号中没有抛出异常, 那么catch后面大括号中的代码不执行



## 代码解析



```swift
    let colors:[UIColor] = {
        var colorSet:[UIColor] = []
        for _ in 0...80 {
            let color = UIColor(red: CGFloat.random(in: 0...1), 
                                green: CGFloat.random(in: 0...1),
                                blue: CGFloat.random(in: 0...1), 
                                alpha: 1)
            colorSet.append(color)
        }
        return colorSet
    }()
```







lazy 延时加载

**懒加载语法：lazy var varName:varType = {}()**

```swift
    lazy var yoloRequest:VNCoreMLRequest! = {
        do {
            let model = try yolov8s().model
            //与if语句相同的是，guard也是基于一个表达式的布尔值去判断一段代码是否该被执行。
            //与if语句不同的是，guard只有在条件不满足的时候才会执行这段代码
            //你可以把guard近似的看做是Assert，但是你可以优雅的退出而非崩溃
            guard let classes = model.modelDescription.classLabels as? [String] else {
                fatalError()
            }
            self.classes = classes
            let vnModel = try VNCoreMLModel(for: model)
            let request = VNCoreMLRequest(model: vnModel)
            return request
        } catch let error {
            fatalError("mlmodel error.")
        }
    }()
```



延迟加载主要有以下两个使用的场景：

1. 属性的初始值依赖于其他的属性值，只有其他的属性值有值之后才能得出该属性的值。
2. 属性的初始值需要大量的计算。





```swift
    func detection(pixelBuffer: CVPixelBuffer) -> UIImage? {
        do {
            let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer)
            try handler.perform([yoloRequest])
            guard let results = yoloRequest.results as? [VNRecognizedObjectObservation] else {
                return nil
            }
            var detections:[Detection] = []
            for result in results {
                let flippedBox = CGRect(x: result.boundingBox.minX, y: 1 - result.boundingBox.maxY, width: result.boundingBox.width, height: result.boundingBox.height)
                let box = VNImageRectForNormalizedRect(flippedBox, Int(videoSize.width), Int(videoSize.height))

                guard let label = result.labels.first?.identifier as? String,
                        let colorIndex = classes.firstIndex(of: label) else {
                        return nil
                }
                let detection = Detection(box: box, confidence: result.confidence, label: label, color: colors[colorIndex])
                detections.append(detection)
            }
            let drawImage = drawRectsOnImage(detections, pixelBuffer)
            return drawImage
        } catch let error {
            return nil
            print(error)
        }
    }
```





# ISSUES

1.

build 时候报错

>  There are no accounts registered with Xcode. Add your developer account to Xcode

- 解决办法：在 Xcode  Preference -> Acoounts->+ ,添加 Apple ID 账号

2.

开发者账号，一年688！！！



------
xcode等版本关系对应表，收藏。

| Version           | Release | Build    | Released    | Requires       | Swift                        | SDKs                                                         | Download[¹](https://xcodereleases.com/?scope=release#fn1)    | Release Notes[¹](https://xcodereleases.com/?scope=release#fn1) |
| ----------------- | ------- | -------- | ----------- | -------------- | ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Xcode 15.1        | Release | 15C65    | 11 Dec 2023 | macOS 13.5+    | Swift 5.9.2 (5.9.2.2.56)     | macOS 14.2 (23C53)iOS 17.2 (21C52)watchOS 10.2 (21S355)tvOS 17.2 (21K354) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_15.1/Xcode_15.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-15_1-release-notes) |
| Xcode 15.0.1      | Release | 15A507   | 18 Oct 2023 | macOS 13.5+    | Swift 5.9 (5.9.0.128.108)    | macOS 14.0 (23A334)iOS 17.0 (21A326)watchOS 10.0 (21R354)tvOS 17.0 (21J351) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_15.0.1/Xcode_15.0.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-15_0_1-release-notes) |
| Xcode 15.0        | Release | 15A240d  | 18 Sep 2023 | macOS 13.5+    | Swift 5.9 (5.9.0.128.108)    | macOS 14.0 (23A334)iOS 17.0 (21A325)watchOS 10.0 (21R354)tvOS 17.0 (21J351) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_15/Xcode_15.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-15-release-notes) |
| Xcode 14.3.1      | Release | 14E300c  | 1 Jun 2023  | macOS 13.0+    | Swift 5.8.1 (5.8.0.124.5)    | macOS 13.3 (22E245)iOS 16.4 (20E238)watchOS 9.4 (20T248)tvOS 16.4 (20L489) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14.3.1/Xcode_14.3.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-14_3_1-release-notes) |
| Xcode 14.3        | Release | 14E222b  | 30 Mar 2023 | macOS 13.0+    | Swift 5.8 (5.8.0.124.2)      | macOS 13.3 (22E245)iOS 16.4 (20E238)watchOS 9.4 (20T248)tvOS 16.4 (20L489) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14.3/Xcode_14.3.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-14_3-release-notes) |
| Xcode 14.2        | Release | 14C18    | 13 Dec 2022 | macOS 12.5+    | Swift 5.7.2 (5.7.2.135.5)    | macOS 13.1 (22C55)iOS 16.2 (20C52)watchOS 9.1 (20S71)tvOS 16.1 (20K67) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14.2/Xcode_14.2.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-14_2-release-notes) |
| Xcode 14.1        | Release | 14B47b   | 1 Nov 2022  | macOS 12.5+    | Swift 5.7.1 (5.7.1.135.3)    | macOS 13.0 (22A372)iOS 16.1 (20B71)watchOS 9.1 (20S71)tvOS 16.1 (20K67) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14.1/Xcode_14.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-14_1-release-notes) |
| Xcode 14.0.1      | Release | 14A400   | 26 Sep 2022 | macOS 12.5+    | Swift 5.7 (5.7.0.127.4)      | macOS 12.3 (21E226)iOS 16.0 (20A360)watchOS 9.0 (20R362)tvOS 16.0 (20J373) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14.0.1/Xcode_14.0.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-14_0_1-release-notes) |
| Xcode 14.0        | Release | 14A309   | 12 Sep 2022 | macOS 12.5+    | Swift 5.7 (5.7.0.127.4)      | macOS 12.3 (21E226)iOS 16.0 (20A360)watchOS 9.0 (20R362)tvOS 16.0 (20J373) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_14/Xcode_14.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-14-release-notes) |
| Xcode 13.4.1      | Release | 13F100   | 2 Jun 2022  | macOS 12.0+    | Swift 5.6.1 (5.6.0.323.66)   | macOS 12.3 (21E226)iOS 15.5 (19F64)watchOS 8.5 (19T241)tvOS 15.4 (19L439) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_13.4.1/Xcode_13.4.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-13_4_1-release-notes) |
| Xcode 13.4        | Release | 13F17a   | 16 May 2022 | macOS 12.0+    | Swift 5.6.1 (5.6.0.323.66)   | macOS 12.3 (21E226)iOS 15.5 (19F64)watchOS 8.5 (19T241)tvOS 15.4 (19L439) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_13.4/Xcode_13.4.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-13_4-release-notes) |
| Xcode 13.3.1      | Release | 13E500a  | 11 Apr 2022 | macOS 12.0+    | Swift 5.6 (5.6.0.323.62)     | macOS 12.3 (21E226)iOS 15.4 (19E239)watchOS 8.5 (19T241)tvOS 15.4 (19L439) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_13.3.1/Xcode_13.3.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-13_3_1-release-notes) |
| Xcode 13.3        | Release | 13E113   | 14 Mar 2022 | macOS 12.0+    | Swift 5.6 (5.6.0.323.62)     | macOS 12.3 (21E226)iOS 15.4 (19E239)watchOS 8.5 (19T241)tvOS 15.4 (19L439) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_13.3/Xcode_13.3.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-13_3-release-notes) |
| Xcode 13.2.1      | Release | 13C100   | 17 Dec 2021 | macOS 11.3+    | Swift 5.5.2 (1300.0.47.5)    | macOS 12.1 (21C46)iOS 15.2 (19C51)watchOS 8.3 (19S51)tvOS 15.2 (19K50) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_13.2.1/Xcode_13.2.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-13_2_1-release-notes) |
| Xcode 13.2        | Release | 13C90    | 13 Dec 2021 | macOS 11.3+    | Swift 5.5.2 (1300.0.47.5)    | macOS 12.1 (21C46)iOS 15.2 (19C51)watchOS 8.3 (19S51)tvOS 15.2 (19K50) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_13.2/Xcode_13.2.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-13_2-release-notes) |
| Xcode 13.1        | Release | 13A1030d | 25 Oct 2021 | macOS 11.3+    | Swift 5.5.1 (1300.0.31.4)    | macOS 12.0 (21A344)iOS 15.0 (19A339)watchOS 8.0.1 (19R351)tvOS 15.0 (19J344) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_13.1/Xcode_13.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-13_1-release-notes) |
| Xcode 13.0        | Release | 13A233   | 20 Sep 2021 | macOS 11.3+    | Swift 5.5 (1300.0.31.1)      | macOS 11.3 (20E214)iOS 15.0 (19A339)watchOS 8.0 (19R341)tvOS 15.0 (19J344) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_13/Xcode_13.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-13-release-notes) |
| Xcode 12.5.1      | Release | 12E507   | 21 Jun 2021 | macOS 11.0+    | Swift 5.4.2 (1205.0.28.2)    | macOS 11.3 (20E214)iOS 14.5 (18E182)watchOS 7.4 (18T187)tvOS 14.5 (18L191) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_12.5.1/Xcode_12.5.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-12_5_1-release-notes) |
| Xcode 12.5        | Release | 12E262   | 26 Apr 2021 | macOS 11.0+    | Swift 5.4 (1205.0.26.9)      | macOS 11.3 (20E214)iOS 14.5 (18E182)watchOS 7.4 (18T187)tvOS 14.5 (18L191) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_12.5/Xcode_12.5.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-12_5-release-notes) |
| Xcode 12.4        | Release | 12D4e    | 26 Jan 2021 | macOS 10.15.4+ | Swift 5.3.2 (1200.0.45)      | macOS 11.1 (20C63)iOS 14.4 (18D46)watchOS 7.2 (18S561)tvOS 14.3 (18K559) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_12.4/Xcode_12.4.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-12_4-release-notes) |
| Xcode 12.3        | Release | 12C33    | 14 Dec 2020 | macOS 10.15.4+ | Swift 5.3.2 (1200.0.45)      | macOS 11.1 (20C63)iOS 14.3 (18C61)watchOS 7.2 (18S561)tvOS 14.3 (18K559) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_12.3/Xcode_12.3.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-12_3-release-notes/) |
| Xcode 12.2        | Release | 12B45b   | 12 Nov 2020 | macOS 10.15.4+ | Swift 5.3.1 (1200.0.41)      | macOS 11.0 (20A2408)iOS 14.2 (18B79)watchOS 7.1 (18R579)tvOS 14.2 (18K54) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_12.2/Xcode_12.2.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-12_2-release-notes) |
| Xcode 12.1        | GM      | 12A7403  | 20 Oct 2020 | macOS 10.15.4+ | Swift 5.3 (1200.0.29.2)      | macOS 10.15.6 (19G68)iOS 14.1 (18A8394)watchOS 7.0 (18R382)tvOS 14.0 (18J390) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_12.1/Xcode_12.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-12_1-release-notes/) |
| Xcode 12.0.1      | GM      | 12A7300  | 24 Sep 2020 | macOS 10.15.4+ | Swift 5.3 (1200.0.29.2)      | macOS 10.15.6 (19G68)iOS 14.0 (18A390)watchOS 7.0 (18R382)tvOS 14.0 (18J390) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_12.0.1/Xcode_12.0.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-12_0_1-release-notes) |
| Xcode 12.0        | GM      | 12A7209  | 17 Sep 2020 | macOS 10.15.4+ | Swift 5.3 (1200.0.29.2)      | macOS 10.15.6 (19G68)iOS 14.0 (18A390)watchOS 7.0 (18R382)tvOS 14.0 (18J390) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_12/Xcode_12.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-12-release-notes/) |
| Xcode 11.7        | GM      | 11E801a  | 1 Sep 2020  | macOS 10.15.2+ | Swift 5.2.4 (1103.0.32.9)    | macOS 10.15.6 (19G68)iOS 13.7 (17H22)watchOS 6.2 (17T255)tvOS 13.4 (17L255) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.7/Xcode_11.7.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-11_7-release-notes) |
| Xcode 11.6        | GM      | 11E708   | 15 Jul 2020 | macOS 10.15.2+ | Swift 5.2.4 (1103.0.32.9)    | macOS 10.15.6 (19G68)iOS 13.6 (17G64)watchOS 6.2 (17T255)tvOS 13.4 (17L255) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.6/Xcode_11.6.xip) | [Release Notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-11_6-release-notes) |
| Xcode 11.5        | GM      | 11E608c  | 20 May 2020 | macOS 10.15.2+ | Swift 5.2.4 (1103.0.32.9)    | macOS 10.15.4 (19E258)iOS 13.5 (17F65)watchOS 6.2 (17T255)tvOS 13.4 (17L255) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.5/Xcode_11.5.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_11_5_release_notes) |
| Xcode 11.4.1      | GM      | 11E503a  | 16 Apr 2020 | macOS 10.15.2+ | Swift 5.2.2 (1103.0.32.6)    | macOS 10.15.4 (19E258)iOS 13.4.1 (17E8258)watchOS 6.2 (17T255)tvOS 13.4 (17L255) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.4.1/Xcode_11.4.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_11_4_1_release_notes) |
| Xcode 11.4        | GM      | 11E146   | 24 Mar 2020 | macOS 10.15.2+ | Swift 5.2 (1103.0.32.1)      | macOS 10.15.4 (19E258)iOS 13.4 (17E255)watchOS 6.2 (17T255)tvOS 13.4 (17L255) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.4/Xcode_11.4.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_11_4_release_notes) |
| Xcode 11.3.1      | GM      | 11C505   | 13 Jan 2020 | macOS 10.14.4+ | Swift 5.1.3 (1100.0.282.1)   | macOS 10.15.1 (19B90)iOS 13.2.2 (17B102)watchOS 6.1 (17S80)tvOS 13.2 (17K90) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.3.1/Xcode_11.3.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_11_3_1_release_notes) |
| Xcode 11.3        | GM      | 11C29    | 10 Dec 2019 | macOS 10.14.4+ | Swift 5.1.3 (1100.0.282.1)   | macOS 10.15.1 (19B90)iOS 13.2.2 (17B102)watchOS 6.1 (17S80)tvOS 13.2 (17K90) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.3/Xcode_11.3.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_11_3_release_notes) |
| Xcode 11.2.1      | GM      | 11B500   | 12 Nov 2019 | macOS 10.14.4+ | Swift 5.1.2 (1100.0.278)     | macOS 10.15.1 (19B89)iOS 13.2.2 (17B102)watchOS 6.1 (17S80)tvOS 13.2 (17K90) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.2.1/Xcode_11.2.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_11_2_1_release_notes) |
| Xcode 11.2        | GM      | 11B52    | 31 Oct 2019 | macOS 10.14.4+ | Swift 5.1.2 (1100.0.278)     | macOS 10.15.1 (19B81)iOS 13.2 (17B80)watchOS 6.1 (17S80)tvOS 13.2 (17K81) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.2/Xcode_11.2.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_11_2_release_notes) |
| Xcode 11.1        | GM      | 11A1027  | 7 Oct 2019  | macOS 10.14.4+ | Swift 5.1 (1100.0.270.13)    | macOS 10.15 (19A547)iOS 13.1 (17A820)watchOS 6.0 (17R566)tvOS 13.0 (17J559) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11.1/Xcode_11.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_11_1_release_notes/) |
| Xcode 11.0        | GM      | 11A420a  | 20 Sep 2019 | macOS 10.14.4+ | Swift 5.1 (1100.0.270.13)    | macOS 10.15 (19A547)iOS 13.0 (17A566)watchOS 6.0 (17R566)tvOS 13.0 (17J559) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_11/Xcode_11.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_11_release_notes) |
| Xcode 10.3        | GM      | 10G8     | 22 Jul 2019 | macOS 10.14.3+ | Swift 5.0.1 (1001.0.82.4)    | macOS 10.14.6 (18G74)iOS 12.4 (16G73)watchOS 5.3 (16U567)tvOS 12.4 (16M567) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_10.3/Xcode_10.3.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_10_3_release_notes/) |
| Xcode 10.2.1      | GM      | 10E1001  | 17 Apr 2019 | macOS 10.14.3+ | Swift 5.0.1 (1001.0.82.4)    | macOS 10.14.4 (18E219)iOS 12.2 (16E226)watchOS 5.2 (16T224)tvOS 12.2 (16L225) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_10.2.1/Xcode_10.2.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_10_2_1_release_notes/) |
| Xcode 10.2        | GM      | 10E125   | 25 Mar 2019 | macOS 10.14.3+ | Swift 5.0 (1001.0.69.5)      | macOS 10.14.4 (18E219)iOS 12.2 (16E226)watchOS 5.2 (16T224)tvOS 12.2 (16L225) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_10.2/Xcode_10.2.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_10_2_release_notes) |
| Xcode 10.1        | GM      | 10B61    | 30 Oct 2018 | macOS 10.13.6+ | Swift 4.2.1 (1000.11.42)     | macOS 10.14.1 (18B71)iOS 12.1 (16B91)watchOS 5.1 (16R591)tvOS 12.1 (16J602) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_10.1/Xcode_10.1.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_10_1_release_notes) |
| Xcode 10.0        | GM      | 10A255   | 17 Sep 2018 | macOS 10.13.6+ | Swift 4.2 (1000.11.37.1)     | macOS 10.14 (18A384)iOS 12.0 (16A366)watchOS 5.0 (16R363)tvOS 12.0 (16J364) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_10/Xcode_10.xip) | [Release Notes](https://developer.apple.com/documentation/xcode_release_notes/xcode_10_release_notes) |
| Xcode 9.4.1       | Release | 9F2000   | 19 Jun 2018 | macOS 10.13.2+ | Swift 4.1.2 (902.0.54)       | macOS 10.13.4 (17E189)iOS 11.4 (15F79)watchOS 4.3 (15T212)tvOS 11.4 (15L576) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_9.4.1/Xcode_9.4.1.xip) | [Release Notes](https://developer.apple.com/library/archive/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-DontLinkElementID_1) |
| Xcode 9.4         | Release | 9F1027a  | 29 May 2018 | macOS 10.13.2+ | Swift 4.1.2 (902.0.54)       | macOS 10.13.4 (17E189)iOS 11.4 (15F79)watchOS 4.3 (15T212)tvOS 11.4 (15L576) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_9.4/Xcode_9.4.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-DontLinkElementID_1) |
| Xcode 9.3.1       | Release | 9E501    | 10 May 2018 | macOS 10.13.2+ | Swift 4.1 (902.0.48902.0.48) | macOS 10.13.4 (17E189)iOS 11.3 (15E217)watchOS 4.3 (15T212)tvOS 11.3 (15L211) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_9.3.1/Xcode_9.3.1.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-DontLinkElementID_1) |
| Xcode 9.3         | Release | 9E145    | 29 Mar 2018 | macOS 10.13.2+ | Swift 4.1 (902.0.48)         | macOS 10.13.4 (17E189)iOS 11.3 (15E217)watchOS 4.3 (15T212)tvOS 11.3 (15L211) | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_9.3/Xcode_9.3.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-DontLinkElementID_1) |
| Xcode 9.2         | Release | 9C40b    | 4 Dec 2017  | macOS 10.12.6+ | Swift 4.0.3 (900.0.74.1)     | macOS 17C76iOS 15C107watchOS 15S100tvOS 15K104               | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_9.2/Xcode_9.2.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW936) |
| Xcode 9.1         | Release | 9B55     | 31 Oct 2017 | macOS 10.12.6+ | Swift 4.0.2 (900.0.69.2)     | macOS 17B41iOS 15B87watchOS 15R844tvOS 15J580                | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_9.1/Xcode_9.1.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW881) |
| Xcode 9.0.1       | Release | 9A1004   | 15 Oct 2017 | macOS 10.12.6+ | Swift 4.0 (900.0.65.2)       | macOS 17A360iOS 15A372watchOS 15R372tvOS 15J380              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_9.0.1/Xcode_9.0.1.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW922) |
| Xcode 9.0         | Release | 9A235    | 12 Sep 2017 | macOS 10.12.6+ | Swift 4.0 (900.0.65)         | macOS 17A360iOS 15A372watchOS 15R372tvOS 15J380              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_9/Xcode_9.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW878) |
| Xcode 8.3.3       | Release | 8E3004b  | 5 Jun 2017  | macOS 10.12+   | Swift 3.1 (802.0.53)         | macOS 16E185iOS 14E8301watchOS 14V243tvOS 14W260             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_8.3.3/Xcode_8.3.3.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW870) |
| Xcode 8.3.2       | Release | 8E2002   | 18 Apr 2017 | macOS 10.12+   | Swift 3.1 (802.0.53)         | macOS 16E185iOS 14E269watchOS 14V243tvOS 14W260              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_8.3.2/Xcode_8.3.2.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW853) |
| Xcode 8.3.1       | Release | 8E1000a  | 6 Apr 2017  | macOS 10.12+   | Swift 3.1 (802.0.51)         | macOS 16E185iOS 14E269watchOS 14V243tvOS 14W260              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_8.3.1/Xcode_8.3.1.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW848) |
| Xcode 8.3         | Release | 8E162    | 27 Mar 2017 | macOS 10.12+   | Swift 3.1 (802.0.48)         | macOS 16E185iOS 14E269watchOS 14V243tvOS 14W260              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_8.3/Xcode_8.3.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW160) |
| Xcode 8.2.1       | Release | 8C1002   | 19 Dec 2016 | macOS 10.11.5+ | Swift 3.0.2 (800.0.63)       | macOS 16C58iOS 14C89watchOS 14S471atvOS 14U591               | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_8.2.1/Xcode_8.2.1.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW157) |
| Xcode 8.2         | Release | 8C38     | 12 Dec 2016 | macOS 10.11.5+ | Swift 3.0.2 (800.0.63)       | macOS 16C58iOS 14C89watchOS 14S471atvOS 14U591               | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_8.2/Xcode_8.2.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW9) |
| Xcode 8.1         | Release | 8B62     | 27 Oct 2016 | macOS 10.11.5+ | Swift 3.0.1 (800.0.58.6)     | macOS 16B2649iOS 14B72watchOS 14S471atvOS 14T328             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_8.1/Xcode_8.1.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW24) |
| Xcode 8.0         | Release | 8A218a   | 13 Sep 2016 | macOS 10.11.5+ | Swift 3.0 (800.0.46.2)       | macOS 16A300iOS 14A345watchOS 14S326tvOS 14T328              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_8/Xcode_8.xip) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW78) |
| Xcode 7.3.1       | Release | 7D1014   | 3 May 2016  | macOS 10.11+   | Swift 2.2 (703.0.18.8)       | macOS 15E60iOS 13E230watchOS 13V143tvOS 13Y227               | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_7.3.1/Xcode_7.3.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW217) |
| Xcode 7.3         | Release | 7D175    | 21 Mar 2016 | macOS 10.11+   | Swift 2.2 (703.0.18.1)       | macOS 15E60iOS 13E230watchOS 13V143tvOS 13Y227               | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_7.3/Xcode_7.3.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW233) |
| Xcode 7.2.1       | Release | 7C1002   | 2 Feb 2016  | macOS 10.10.5+ | Swift 2.1.1 (700.1.101.15)   | macOS 15C43iOS 13C75watchOS 13S660tvOS 13U79                 | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_7.2.1/Xcode_7.2.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW264) |
| Xcode 7.2         | Release | 7C68     | 8 Dec 2015  | macOS 10.10.5+ | Swift 2.1.1 (700.1.101.15)   | macOS 15C43iOS 13C75watchOS 13S660tvOS 13U78                 | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_7.2/Xcode_7.2.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW270) |
| Xcode 7.1.1       | Release | 7B1005   | 5 Nov 2015  | macOS 10.10.5+ |                              | macOS 15A278iOS 13B137watchOS 13S343tvOS 13T393              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_7.1.1/Xcode_7.1.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW291) |
| Xcode 7.1         | Release | 7B91b    | 21 Oct 2015 | macOS 10.10.5+ | Swift 2.1 (700.1.101.6)      | macOS 15A278iOS 13B137watchOS 13S343tvOS 13T393              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_7.1/Xcode_7.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW300) |
| Xcode 7.0.1       | Release | 7A1001   | 28 Sep 2015 | macOS 10.10.3+ | Swift 2.0 (700.0.59)         | macOS 15A278iOS 13A340watchOS 13S343                         | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_7.0.1/Xcode_7.0.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW324) |
| Xcode 7.0         | Release | 7A220    | 16 Sep 2015 | macOS 10.10.3+ | Swift 2.0 (700.0.59)         | macOS 15A278iOS 13A340watchOS 13S343                         | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_7/Xcode_7.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW326) |
| Xcode 6.4         | Release | 6E35b    | 30 Jun 2015 | macOS 10.10+   | Swift 1.2 (602.0.53.1)       | macOS 13F34macOS 14D125iOS 12H141                            | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_6.4/Xcode_6.4.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW364) |
| Xcode 6.3.2       | Release | 6D2105   | 18 May 2015 | macOS 10.10+   | Swift 1.2 (602.0.53.1)       | macOS 13F34macOS 14D125iOS 12F69                             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_6.3.2/Xcode_6.3.2.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW368) |
| Xcode 6.3.1       | Release | 6D1002   | 21 Apr 2015 | macOS 10.10+   | Swift 1.2 (602.0.49.6)       | macOS 13F34macOS 14D125iOS 12F69                             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_6.3.1/Xcode_6.3.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW370) |
| Xcode 6.3         | Release | 6D570    | 8 Apr 2015  | macOS 10.10+   | Swift 1.2 (602.0.49.3)       | macOS 13F34macOS 14D125iOS 12F69                             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_6.3/Xcode_6.3.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW378) |
| Xcode 6.2         | Release | 6C131e   | 9 Mar 2015  | macOS 10.9.4+  | Swift 1.1 (600.0.57.4)       | macOS 13F26macOS 14A383iOS 12D508                            | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_6.2/Xcode_6.2.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW412) |
| Xcode 6.1.1       | Release | 6A2008a  | 2 Dec 2014  | macOS 10.9.4+  | Swift 1.1 (600.0.56.1)       | macOS 13F26macOS 14A382iOS 12A365                            | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_6.1.1/xcode_6.1.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW423) |
| Xcode 6.1         | Release | 6A1052d  | 20 Oct 2014 | macOS 10.9.4+  | Swift 1.1 (600.0.54.20)      |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_6.1/56841_xcode_6.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW432) |
| Xcode 6.0.1       | Release | 6A317    | 17 Sep 2014 | macOS 10.9.4+  | Swift 1.0 (600.0.51.4)       | macOS 13F26iOS 12A365                                        | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_6.0.1/xcode_6.0.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW450) |
| Xcode 6.0         | Release | 6A313    | 9 Sep 2014  | macOS 10.9.4+  |                              |                                                              |                                                              | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW453) |
| Xcode 5.1.1       | Release | 5B1008   | 10 Apr 2014 | macOS 10.8+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_5.1.1/xcode_5.1.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW504) |
| Xcode 5.1         | Release | 5B130a   | 10 Mar 2014 | macOS 10.8+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_5.1/xcode_5.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW512) |
| Xcode 5.0.2       | Release | 5A3005a  | 11 Nov 2013 | macOS 10.8+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_5.0.2/xcode_5.0.2.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW536) |
| Xcode 5.0.1       | Release | 5A2053   | 22 Oct 2013 | macOS 10.8+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_5.0.1/xcode_5.0.1.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW544) |
| Xcode 5.0         | Release | 5A1413   | 16 Sep 2013 | macOS 10.8+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_5/xcode_5.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW578) |
| Xcode 4.6.3       | Release | 4H1503   | 12 Jun 2013 | macOS 10.7+    |                              | macOS 11E52macOS 12D75iOS 10B141                             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.6.3/xcode4630916281a.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW600) |
| Xcode 4.6.2       | Release | 4H1003   | 15 Apr 2013 | macOS 10.7+    |                              | macOS 11E52macOS 12D75iOS 10B141                             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.6.2/xcode4620419895a.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW603) |
| Xcode 4.6.1       | Release | 4H512    | 14 Mar 2013 | macOS 10.7+    |                              | macOS 11E52macOS 12D75iOS 10B141                             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.6.1/xcode4610419628a.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW612) |
| Xcode 4.6         | Release | 4H127    | 28 Jan 2013 | macOS 10.7+    |                              | macOS 11E52macOS 12D75iOS 10B141                             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.6/xcode460417218a.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_4.6/release_notes_xcode46gm.pdf) |
| Xcode 4.5.2       | Release | 4G2008a  | 1 Nov 2012  | macOS 10.7+    |                              | macOS 11E52macOS 12C237iOS 10A403                            | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.5.2/xcode4520418508a.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_4.5.2/release_notes_xcode_4.5.2.pdf) |
| Xcode 4.5.1       | Release | 4G1004   | 3 Oct 2012  | macOS 10.7+    |                              | macOS 11E52macOS 12C237iOS 10A403                            | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.5.1/xcode4510417539a.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_4.5.1/release_notes_xcode_4.5.1.pdf) |
| Xcode 4.5         | Release | 4G182    | 19 Sep 2012 | macOS 10.7+    |                              | macOS 11E52macOS 12C237iOS 10A403                            | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.5/xcode_4.5.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW643) |
| Xcode 4.4.1       | Release | 4F1003   | 7 Aug 2012  | macOS 10.7+    |                              | macOS 11E52macOS 12A264iOS 9B176                             | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.4.1/xcode_4.4.1_6938145.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW670) |
| Xcode 4.3.3       | Release | 4E3002   | 7 Jun 2012  | macOS 10.7+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.3.3_for_lion/xcode_4.3.3_for_lion.dmg) |                                                              |
| Xcode 4.3.2       | Release | 4E2002   | 21 Mar 2012 | macOS 10.7+    |                              | iOS 9B176                                                    | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.3.2/xcode_432_lion.dmg) |                                                              |
| Xcode 4.4         | Release | 4F134    | 15 Mar 2012 | macOS 10.7+    |                              | iOS 9B174                                                    | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.4_21362/xcode446938108a.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_4.4_21362/release_notes_xcode44gm.pdf) |
| Xcode 4.3.1       | Release | 4E1019   | 5 Mar 2012  | macOS 10.7+    |                              | iOS 9B176                                                    | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.3.1_for_lion_21267/xcode_431_lion.dmg) |                                                              |
| Xcode 4.3         | Release | 4E109    | 12 Feb 2012 | macOS 10.7+    |                              | iOS 9A334                                                    | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.3_for_lion_21266/xcode_43_lion.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW699) |
| Xcode 4.2.1       | Release | 4D502    | 17 Nov 2011 | macOS 10.7+    |                              | iOS 9A334                                                    | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.2.1_for_lion_21265/installxcode_421_lion.dmg) |                                                              |
| Xcode 4.2         | Release | 4D199    | 12 Oct 2011 | macOS 10.7+    |                              | iOS 9A334                                                    | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.2_for_lion_21264/installxcode_42_lion.dmg) | [Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW713) |
| Xcode 4.2         | Release | 4C199    | 12 Oct 2011 | macOS 10.6.8+  |                              | iOS 9A334                                                    | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.2_for_snow_leopard/xcode_4.2_for_snow_leopard.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_4.2_for_snow_leopard/xcode_4.2_for_snow_leopard_readme.pdf) |
| Xcode 4.1         | Release | 4B110f   | 29 Aug 2011 | macOS 10.6.8+  |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.1_for_snow_leopard_21110/xcode_4.1_for_snow_leopard.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_4.1_for_snow_leopard_21110/xcode_4.1_for_snow_leopard_readme.pdf) |
| Xcode 4.1         | Release | 4B110i   | 20 Jul 2011 | macOS 10.7+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.1_for_lion_21263/installxcode_41_lion.dmg) |                                                              |
| Xcode 4.0.2       | Release | 4A2002a  | 12 Apr 2011 | macOS 10.6.8+  |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.0.2_and_ios_sdk_4.3/xcode_4.0.2_and_ios_sdk_4.3.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_4.0.2_and_ios_sdk_4.3/final_xcode_4.0.2_readme.pdf) |
| Xcode 4.0.1       | Release | 4A1006   | 23 Mar 2011 | macOS 10.6.8+  |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4.0.1_and_ios_sdk_4.3/xcode_4.0.1_and_ios_sdk_4.3.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_4.0.1_and_ios_sdk_4.3/xcode_4.0.1_readme.pdf) |
| Xcode 4.0         | Release | 4A304a   | 9 Mar 2011  | macOS 10.6.8+  |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_4_and_ios_sdk_4.3__final/xcode_4_and_ios_sdk_4.3__final.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_4_and_ios_sdk_4.3__final/xcode_4_rn.pdf) |
| Xcode 3.2.6       | Release | 10M25xx  | 6 Mar 2011  | macOS 10.6.4+  |                              | iOS 4.3                                                      | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.2.6_and_ios_sdk_4.3__final/xcode_3.2.6_and_ios_sdk_4.3.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.2.6_and_ios_sdk_4.3__final/xcode_3_and_ios_sdk_4.3_readme.pdf) |
| Xcode 3.2.5       | Release | 10M2423  | 18 Nov 2010 | macOS 10.6.4+  |                              | iOS 4.2                                                      | [Download](https://developer.apple.com/services-account/download?path=/ios/ios_sdk_4.2__final/xcode_3.2.5_and_ios_sdk_4.2_final.dmg) | [Release Notes](https://download.developer.apple.com/ios/ios_sdk_4.2__final/readme_xcode_3.2.5_and_ios_4.2.pdf) |
| Xcode 3.2.4       | Release | 10M2309  | 6 Sep 2010  | macOS 10.6.2+  |                              | iOS 3.2iOS 4.1                                               | [Download](https://developer.apple.com/services-account/download?path=/ios/ios_sdk_4.1__final/xcode_3.2.4_and_ios_sdk_4.1.dmg) | [Release Notes](https://download.developer.apple.com/ios/ios_sdk_4.1__final/finalv2_about_xcode_3.2.4_and_ios_sdk_4.1.pdf) |
| Xcode 3.2.3       | Release | 10M2262  | 10 Aug 2010 | macOS 10.6.2+  |                              | iOS 3.2iOS 4.0.2                                             | [Download](https://developer.apple.com/services-account/download?path=/ios/ios_sdk_4.0.2__final/xcode_3.2.3_and_ios_sdk_4.0.2.dmg) |                                                              |
| Xcode 3.2.3       | Release | 10M2262  | 6 Jul 2010  | macOS 10.6.2+  |                              | iOS 3.2iOS 4.0.1                                             | [Download](https://developer.apple.com/services-account/download?path=/ios/ios_sdk_4.0.1__final/xcode_3.2.3_and_ios_sdk_4.0.1.dmg) | [Release Notes](https://download.developer.apple.com/ios/ios_sdk_4.0.1__final/final_about_xcode_3.2.3_and_ios_sdk_4.0.1.pdf) |
| Xcode 3.2.2       | Release | 10M2154  | 29 Mar 2010 | macOS 10.6.2+  |                              | iOS 3.2                                                      | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.2.2_developer_tools_beta_20728/xcode322_2148_developerdvd.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.2.2_developer_tools_beta_20728/about_xcode_3.2.2.pdf) |
| Xcode 3.2.1       | Release | 10M2020  | 7 Oct 2009  | macOS 10.6+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.2.1_developer_tools/xcode321_10m2003_developerdvd.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.2.1_developer_tools/about_xcode_3.2.1.pdf) |
| Xcode 3.2         | Release | 10A432   | 26 Aug 2009 | macOS 10.6+    |                              | macOS 10.4macOS 10.5macOS 10.6                               | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.2/xcode3210a432.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.2/about_xcode_3.2.pdf) |
| Xcode 3.1.4       | Release | 9M2809   | 9 Jul 2009  | macOS 10.5.7+  |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.1.4_developer_tools/xcode314_2809_developerdvd.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.1.4_developer_tools/about_xcode_tools_3.1.4.pdf) |
| Xcode 3.1.3       | Release | 9M2736   | 16 Jun 2009 | macOS 10.5.7+  |                              | iOS 3.1.3                                                    | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.1.3_developer_tools/xcode313_2736_developerdvd.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.1.3_developer_tools/about_xcode_tools_3.1.3.pdf) |
| Xcode 3.1.2       | Release | 9M2621   | 23 Nov 2008 | macOS 10.5+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.1.2_developer_tools/xcode312_2621_developerdvd.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.1.2_developer_tools/about_xcode_tools_3.1.2.pdf) |
| Xcode 3.1.1       | Release | 9M2517   | 23 Jul 2008 | macOS 10.5+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.1.1_developer_tools_preview_1/xcode311_9m2517_developerdvd.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.1.1_developer_tools_preview_1/about_xcode_3.1.1_tools.pdf) |
| Xcode 3.1         | Release | 9M2199   | 10 Jul 2008 | macOS 10.5+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.1_developer_tools/xcode31_2199_developerdvd.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.1_developer_tools/about_xcode_tools_3.1.pdf) |
| Xcode 3.0         | Release | 9A581    | 25 Oct 2007 | macOS 10.5+    |                              | macOS 10.3macOS 10.4macOS 10.5iOS 2.0                        | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_3.0/xcode_3.0.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_3.0/xcode_3.0_release_notes.pdf) |
| Xcode 2.5         | Release | 8M2558   | 29 Oct 2007 | macOS 10.4+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_2.5_developer_tools/xcode25_8m2558_developerdvd.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_2.5_developer_tools/relnotesxcode25.pdf) |
| Xcode 2.4.1       | Release | 8M1910   | 30 Oct 2006 | macOS 10.4+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_2.4.1/xcode_2.4.1_8m1910_6936315.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_2.4.1/xcode_2.4.1.readme.pdf) |
| Xcode 2.4         | Release | 8K1079   | 17 Aug 2006 | macOS 10.4+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_2.4/xcode_2.4_8k1079_6936199.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_2.4/xcode_2.4_readme.pdf) |
| Xcode 2.3         | Release | 8M1780   | 23 May 2006 | macOS 10.4+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_2.3/xcode_2.3_8m1780_oz693620813.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_2.3/xcode_2.3_readme_20060522.pdf) |
| Xcode Tools 2.2.1 | Release | 8G1165   | 13 Jan 2006 | macOS 10.4+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_tools_2.2.1/xcode_2.2.1_8g1165_018213632.dmg) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_tools_2.2.1/xcode_2.2.1_readme.pdf) |
| Xcode Tools 2.2   | Release | 8M654    | 10 Nov 2005 | macOS 10.4+    |                              |                                                              |                                                              |                                                              |
| Xcode Tools 2.1   | Release | 8B1024   | 6 Jun 2005  | macOS 10.4+    |                              |                                                              |                                                              |                                                              |
| Xcode Tools 2.0   | Release | 8A428    | 29 Apr 2005 | macOS 10.4+    |                              | macOS 10.2macOS 10.3macOS 10.4                               |                                                              |                                                              |
| Xcode Tools 1.5   | Release | 7K571    | 4 Aug 2004  | macOS 10.3+    |                              |                                                              | [Download](https://developer.apple.com/services-account/download?path=/Developer_Tools/xcode_v1.5/xcode_tools_1.5_cd.dmg.bin) | [Release Notes](https://download.developer.apple.com/Developer_Tools/xcode_v1.5/554_xcode_tools_1.5_read_me.pdf) |
| Xcode Tools 1.2   | Release | 7K249    | 22 Apr 2004 | macOS 10.3+    |                              |                                                              |                                                              |                                                              |
| Xcode Tools 1.1   | Release | 7K224    | 19 Dec 2003 | macOS 10.3+    |                              |                                                              |                                                              |                                                              |
| Xcode Tools 1.0   | Release | 7B85     | 28 Sep 2003 | macOS 10.3+    |                              | macOS 10.1.5 (5S60)macOS 10.2.6 (6L60)macOS 10.3 (7B85)      | [Download](https://developer.apple.com/services-account/download?path=/Mac_OS_X/Mac_OS_X_10.3_Build_7B85/7B85_Xcode_CD.dmg) |                                                              |
