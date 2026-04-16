**git提取需要加密的代码**

先使用git将当前项目中指定commit的代码进行打包。

```bash
# 打包HEAD置信的commit
git archive --format=zip --output=project.zip HEAD
```



Pyarmor可保护python 代码不被泄露，设置加密脚本的有效期限，绑定加密脚本到硬盘、网卡等硬件设备。

## pyarmor安装及代码加密

1. 安装pyarmor库

```bash
pip install pyarmor 
```

2. 加密当前文件夹下的python文件

```bash
cd my_project
pyarmor gen --recursive --output dist/my_project ./
```

`--recursive`递归的加密当前目录下的python文件。并将输出放在dist/my_project目录下。

3. 得到加密后的文件

查看点前目录下生成的dist/my_project文件。包含了以下文件：项目中的.py文件和一个pyarmor_runtime_000000文件夹。（还是可以看到原始项目中的python文件名）

```bash
.
├── llm1.py
├── llm2.py
├── pyarmor_runtime_000000
│   ├── __init__.py
│   └── pyarmor_runtime.so
└── server.py
```

点开任意.py文件，其中内容是类似如下的加密字符

```python
# Pyarmor 9.1.6 (trial), 000000, non-profits, 2025-05-22T11:01:58.084654
from pyarmor_runtime_000000 import __pyarmor__
__pyarmor__(__name__, __file__, b'PY000000\x00\x03\t\x00a\r\r\n\x80\x00\x01\x00\x08\x00\x00\x00\x04\x00\x00\x00@\x00\x00\x00\x86\x11\x00\x00\x12\t\x04\x00e\xd6u\x90ed*/\x9a$\xc9\xe8Z\x84\xab+\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x9f2\xac\'6\xbf\'\r\xe9cJ\xb2\'\x9cd\x9f\xab2\xbf|1\x0eR\xf8M\xf9\xa0\xe1\xd2x\xe0(\xd9n\x11\x0b\xab\x97\x1d\xdd\xfd\xb3\xfc_\x10\x08\xf9qz\xd15-\xb8\x8a\xc6@\xf0\x13%q\xc7\xcd\x0c\x12\x12P"\x12z\xf8W[\x8c5\x85\x17\x8d%p~\xdb.H\xdbm\xd1k\x16\xfa\xd8y\xa1\xe7s\x8a6^\xe2{\x0cYX\xebi|\x9f\xdd\xe6\xb0V\xc8`\xf3\xd084\xee\x01p\xf3kPm\xe8\xc1\xcb`
```

4. 运行加密后的脚本

加密后的脚本可以直接运行，就像普通的 Python 脚本一样。

```python
cd dist/my_project
# 需要切换到必要的运行环境下
conda activate test
python server.py
```

运行时需要确保在运行加密脚本时，其所在环境包含了运行时支持库。



## 加密及docker打包测试

打包docker镜像，加密docker内的python源码。

先构建一个简单的python项目。依赖opencv

dockerfile示例：

```dockerfile
FROM nvidia/cuda:12.6.0-cudnn-devel-ubuntu22.04-python3.11

WORKDIR /app

# 安装 PyArmor和相关依赖库
RUN pip install --no-cache-dir pyarmor -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件到容器
COPY . /app

# 使用 PyArmor 加密项目
# 加密文件替换掉原始文件
RUN pyarmor gen --recursive ./ && \
    cp -r dist/* . && \
    rm -rf dist

# 暴露端口
EXPOSE 8077

# 启动服务
CMD ["python", "server.py"]
```

构建加执行：

```bash
docker build -t pyarmor:test .
docker run -d -p 8077:8077 --name test pyarmor:test
# 进入容器可查看到文件已加密处理
docker exec -it test bash 
```





**pyarmor版本更新问题**

执行

```
pyarmor obfuscate --recursive --output dist/my_project ./server.py
```

报错:

```
Pyarmor 8.0+ has only 3 commands: gen, reg, cfg
Please replace `pyarmor` with `pyarmor-7` to run old commands
```

这是因为在 PyArmor 8.0 的版本更新中，官方对命令行接口进行了重大重构，弃用了旧版的命令（如 obfuscate, pack 等），改为一套新的命令体系。如果希望继续使用旧版命令（比如 obfuscate），你需要运行旧版本的 PyArmor 命令解释器：pyarmor-7。

可使用旧版本命令：

```
pyarmor-7 obfuscate --recursive --output dist/my_project ./server.py
```

或新命令替代

```
pyarmor gen --recursive --output dist/my_project ./
```

这个命令会加密 当前目录下的所有 Python 文件，并将输出放在 dist/my_project 目录下。
