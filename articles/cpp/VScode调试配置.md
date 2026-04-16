# Debug配置

主要是在.vscode下配置两个文件，launch.json和task.json

这两个文件可以自动生成。

**生成launch.json**

Run->AddConfiguration 弹出一个框，选择 C++(GDB/LLDB),  会生成一个launch.json的文件， 此时文件只有version和空的configuration。 选择右下角的 add configuration, 再选择c++/gdb 启动。会默认生成一堆东西。

**生成task.json**

Terminal->Configure tasks-> 弹出一个框， 比如选择CMake：配置。 会默认生成一堆东西。



生成好两个文件，接下来对这两个文件进行修改。这两个文件的主要工作逻辑是这样：

launch.json 中会指定调试器， 调试程序，调试入参。

但是如果对于一个main文件，你想打了断点直接进行调试， 此时你又没有将其进行编译(比如说生成可执行文件)， 那么需要在lauch.json中配置一个task， 这个task会做一些调试前的工作，比如编译生成可执行文件。这时就不用先自己编译好了再进行调试，而是可以直接打了断点f5开始调试。

所以task.json中会指出调试前需要做的事情，比如 设置编译器 ，编译的参数等。



配置文件的修改

launch.json主要有几个需要指定：

- program   要调试的程序，通常是生成的可执行文件
- args   运行该可执行程序时传入的参数
- **miDebuggerPath**  调试用的编译器路径
- **preLaunchTask**  在调试该可执行文件前需要做的操作， 通常指向一个task的label名称。可在task中设置编译操作，生成该可执行文件。

task.json的话看编译的方式，有直接使用g++指令生成活动文件，还有使用cmake编译。

但是主要注意的有:

- type 任务类别， 比如 有 shell, cmake， cppbuild
- label  该任务的id， 之后会被传到launch.json中 ，指定该任务运行。
- command 和args  执行的命令和命令入参



## 调试成功样例

我本地调试yolov8trt成功的配置， 可以打了断点后，直接F5，自动cmake，make生成可执行文件，并跳转到断点处。

launch.json

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) 启动",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/build/yolov8",
            "args": ["../../best.engine",
                    "../001.jpg",
                    "2"],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "为 gdb 启用整齐打印",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                },
                {
                    "description": "将反汇编风格设置为 Intel",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                },
                {
                    "description": "防止 gdb 打开标准库函数",
                    "text": "-interpreter-exec console \"skip -rfu std::.*\"",
                    "ignoreFailures": false
                }
            ],
            "preLaunchTask": "Build_zsl",
            "miDebuggerPath": "/usr/bin/gdb"
        }

    ]
}
```

task.json

```json
{
	"version": "2.0.0",

	"options": {
		"cwd": "${workspaceFolder}/build"
	},
	"tasks": [
		{
			"type": "cmake",
			"label": "CMake: 配置",
			"command": "configure",
			"problemMatcher": [],
			"detail": "CMake 模板 配置 任务"
		},
		{
			"label": "Make_zsl",
			"type": "shell",
			"options": {
				"cwd": "${workspaceFolder}/build"
			},
			"command": "make",
			"group": {
				"kind":"build",
				"isDefault": true,
			},
		},
		{
			"label": "Build_zsl",
			"dependsOrder": "sequence",
			"dependsOn":[
				"CMake: 配置",
				"Make_zsl"

			]
			
		}


	]
}
```



注意：

make任务下这个需要专门指定， 测试时候总是报错，不在build目录下找不到makefile文件。

			"options": {
				"cwd": "${workspaceFolder}/build"
			},



其他地方看到的一些对参数的注释

```json
// tasks.json
{
    // https://code.visualstudio.com/docs/editor/tasks
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Build",  // 任务的名字叫Build，注意是大小写区分的，等会在launch中调用这个名字
            "type": "shell",  // 任务执行的是shell命令，也可以是
            "command": "g++", // 命令是g++
            "args": [
                "'-Wall'",
                "'-std=c++17'",  //使用c++17标准编译
                "'${file}'", //当前文件名
                "-o", //对象名，不进行编译优化
                "'${fileBasenameNoExtension}.exe'",  //当前文件名（去掉扩展名）
            ],
          // 所以以上部分，就是在shell中执行（假设文件名为filename.cpp）
          // g++ filename.cpp -o filename.exe
            "group": { 
                "kind": "build",
                "isDefault": true   
                // 任务分组，因为是tasks而不是task，意味着可以连着执行很多任务
                // 在build组的任务们，可以通过在Command Palette(F1) 输入run build task来运行
                // 当然，如果任务分组是test，你就可以用run test task来运行 
            },
            "problemMatcher": [
                "$gcc" // 使用gcc捕获错误
            ],
        }
    ]
}
```



```json
// launch.json

{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) Launch", //这个应该是F1中出现的名字
            "preLaunchTask": "Build",  //在launch之前运行的任务名，这个名字一定要跟tasks.json中的任务名字大小写一致
            "type": "cppdbg",
            "request": "launch",
            "program": "${fileDirname}/${fileBasenameNoExtension}.exe", //需要运行的是当前打开文件的目录中，名字和当前文件相同，但扩展名为exe的程序
            "args": [],
            "stopAtEntry": false, // 选为true则会在打开控制台后停滞，暂时不执行程序
            "cwd": "${workspaceFolder}", // 当前工作路径：当前文件所在的工作空间
            "environment": [],
            "externalConsole": true,  // 是否使用外部控制台，选false的话，我的vscode会出现错误
            "MIMode": "gdb",
            "miDebuggerPath": "c:/MinGW/bin/gdb.exe",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }]
}
```



# Task

VS Code中执行多个task

方法一

把第2个任务设置成第1个任务的`dependsOn`，就可以在运行第1个任务时，自动先把第2个任务执行了。

方法二

2个方法保持原样（都不用加dependsOn），在后面（必须是后面）加一个新的task。这样在执行这个新的tasks时，会自动执行前面2个任务。
这个方法有个缺点，每执行一个任务，需要按一下ENTER。





# 远程服务器上的容器内的代码调试

下载dev-container， 标志是一个六面体。

按下组合键`ctrl+shift+p` ， 选择  `Dev-container：Attach to Running Container.`

然后会新弹出一个窗口，加载容器内容，然后选择要打开的容器的代码目录。 



