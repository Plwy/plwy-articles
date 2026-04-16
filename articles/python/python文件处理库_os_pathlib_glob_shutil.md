对常用的文件处理时用到的库和方法进行总结。

- **os**
- **glob**
- **shutil**
- **pathlib**

## os

### 常用

- `os.path.join()`   

  路径拼接。

- `os.listdir() `

  遍历文件夹中的文件，返回文件名列表，不会遍历子文件夹，只返回子文件夹名

- `os.path.walk()`

  遍历文件夹中的文件，可以深度遍历子文件夹。

  得到文件夹下所有文件，示例：

  ```python
  import os
  root_dir = "/root/datas"
  file_paths = []
  for c_dir, sub_dirs, files in os.walk(root_dir):
      if len(files) == 0:
          continue
      else:
          for file in files:
              file_path = os.path.join(c_dir, file)
      		file_paths.append(file_path)
  print(file_paths)
  ```

  使用 os.walk 函数开始遍历从 root_dir 开始的目录树。os.walk 会生成一个三元组 (c_dir, sub_dirs, files)：

  - c_dir 是当前正在遍历的目录路径。
  - sub_dirs 是一个列表，包含 root 下的所有子目录名（不包括符号链接指向的目录）。
  - files 是一个列表，包含 root 下的所有非目录文件名（同样，不包括符号链接指向的文件）。

  使用生成器方式得到文件夹下所有文件，示例：

  ```python
  import os
  def tral_dir(base_dir):
      for c_dir, sub_dirs, files in os.walk(root_dir):
          for file in files:
              file_path = os.path.join(c_dir, file)
              yield file_path
  
  root_dir = "/root/datas"
  file_paths = []
  for filepath in tral_dir(root_dir):
      file_paths.append(fi
  ```

- `os.path.basename()`

  得到文件名。比如`/root/datas/1.txt` ， 函数处理后返回`1.txt`

- `os.path.exists()`

  判断文件是否存在。

- `os.path.isdir()`

  判断路径是否是文件夹。

- `os.path.isfile()`

  判断路径是否是文件。

- `os.path.splitext()`

  将路径字符串分离为文件名与扩展名。`/root/datas/1.txt` 处理后返回`('/root/datas/1', '.txt')`

- `os.mkdir() ` 和`os.makedirs()`

  os.mkdir(path)，创建目录时需保证其父目录已存在，如果不存在会报异常。

  os.makedirs() 可一次创建多级目录，中间目录不存在也能正常的创建。通常使用

  ```python
  os.makedirs(dirname,  exist_ok=True)
  # 这种写法方便，可避免报错
  ```

  `exist_ok=True`为即使该目录已经存在也不要抛出异常。还有mode参数可设置目录权限,默认值是 `0o777`。

  [makedirs  ref](https://blog.csdn.net/Stromboli/article/details/143945661)

- `os.getcwd()`

- `os.path.abspath()`

- `os.path.dirname()`

### 扩展

##### os.remove（）

描述：用于删除指定路径的文件。如果指定的路径是一个目录，将抛出OSError。

##### os.rename（）

描述：命名文件或目录,能对相应的文件进行重命名

语法：os.rename(src, dst)

##### os.path.samefile( )

描述：判断目录或文件是否相同

语法：os.path.samefile(path1, path2)

##### os.path.split()

描述：把路径分割成 dirname 和 basename，返回一个元组

语法：os.path.split(path)



## glob

可用来查找符合特定规则的目录和文件，它支持*、**、? 、[ ]这四个通配符

### 常用

```python
import glob
root_dir = "/root/datas"

# 匹配root_dir路径下的所有目录和文件，并返回路径列表
path_list1 = glob.glob(root_dir+'/*')
# 得到文件夹下的所有某个后缀命名的文件。（不递归）
# f = glob.glob(root_dir + r'/*.py')
f = glob.glob(root_dir + '/*.py')

###（递归）
# 递归的匹配路径下的所有目录和文件
path_list1 = glob.glob(root_dir+'/**', recursive=True)
# 得到文件夹下的所有某个后缀命名的文件。
f = glob.glob(root_dir + '/**/*.py', recursive=True)
```

### 扩展

**glob.iglob**

获取一个可编历对象，使用它可以逐个获取匹配的文件路径名。与glob.glob()的区别是：glob.glob同时获取所有的匹配路径，而glob.iglob一次只获取一个匹配路径。

```python
import glob
root_dir = "/home/sun/zsl_workspace/common_proj/detect_toolkits/labelformat"
f = glob.iglob(root_dir + '/*.py') #<generator object iglob>
for py in f:
    print(py) 
```



## shutil

### 常用

- shutil.copy()

```python
# 拷贝src_path 文件到 dst_path, 两个都是文件路径，dst_path不是目录路径。
# 实现将src_path文件拷贝到指定的路径下。
shutil.copy(src_path, dst_path)
```

- shutil.copytree()

```python
# 实现将src_dir文件夹,拷贝到指定的路径下。两个都是文件目录，且dst_dir目录必须是空文件夹，或者未被创建。
shutil.copytree(src_dir, dst_dir)
```

- shutil.move()

```python
# 实现将src_path文件移动到指定的路径下。两个都是文件路径，dst_path不是目录路径。
shutil.move(src_p , dst_p)
```

### 扩展

**shutil.copytree(src,dst)**

- 含义：复制文件夹；
- 参数：src表示源文件夹，dst表示目标文件夹；
- 注意：这里只能是移动到一个空文件夹，而不能是包含其他文件的非空文件夹，否则会报错PermissionError；

> 如果目标文件夹中存在其他文件，会报错；
>
> 如果指定任意一个目标文件夹，则会自动创建；

**shutil.rmtree(src)** 

- 含义：删除文件夹；**慎用**
- 参数：src表示源文件夹；
- 注意：区别这里和os模块中remove()、rmdir()的用法，remove()方法只能删除某个文件，rmdir()只能删除某个空文件夹。但是shutil模块中的rmtree()可以递归彻底删除非空文件夹；



## pathlib

The pathlib module – object-oriented filesystem paths(面向对象的文件系统路径) 

### 常用

- **Path()**

可直接拼接路径

```python
filepath = Path(dir_path) / 'test.txt'
```

也可使用joinpath()函数

```python
filepath = Path(dir_path).joinpath('test.txt')
```

- 属性

  - **Path.name**

    获取文件名，包含后缀

    ```python
    Path('my/library/setup.py').name
    #输出 'setup.py'
    ```

  - **Path.stem**

    获取路径中文件或目录的名称部分，但不包含后缀。

  - **Path.suffix**  

    获取文件名的扩展名

  - **Path.parent**    

    得到当前文件父目录，方便和文件名一起拼路径。

    ```python
     tmp_file = Path(file).parent / 'test.txt'
    ```

  - **Path.parents**

    获取所有的上级目录。父目录为Path.parentes[0]

- **Path.resolve()**

获得绝对路径

```python
# 得到的绝对路径不一定存在。 进行了filepath和当前工作目录拼接
absolute_path = Path(filepath).resolve()
```

- **Path.exists()**

判断当前文件或者目录是否存在

- **Path.with_suffix()** 

将当前路径修改为指定后缀

- **Path.with_name()**

将当前路径修改为指定文件名

```python
image_dir = "/home/sun/test_datas/test_images"
filepath = Path(image_dir).joinpath('test.txt')
print(filepath)
print(filepath.with_suffix('.json'))
print(filepath.with_name('haha.png'))
#输出
/home/sun/test_datas/test_images/test.txt
/home/sun/test_datas/test_images/test.json
/home/sun/test_datas/test_images/haha.png
```

- **Path.iterdir()**

迭代此目录中的文件。对于特殊路径“。”和“..”不会产生任何结果。

只能传入已存在目录，只会返回目录下所有文件，包括文件夹，不会遍历子文件下内容。

```python
image_dir = "/home/sun/test_datas/test_images"
image_dirp = Path(image_dir)
# 变量目录下的文件
for fp in image_dirp.iterdir():
    print(fp)
```

- **Path.glob()**

和glob一样可进行规则匹配

```python
filepath = Path('.')
# 列举当前路径下的所有.py文件
list(filepath.glob('**/*.py')) 
```

- **Path.rglob()**

返回当前目录、及子目录下的文件夹

>  **关于目录的遍历**

```python
import pathlib
root_dir = Path("/home/test_datas")

# 1.遍历当前文件夹下文件，包含文件和文件夹名。不包含子文件夹下文件
for fp in root_dir.iterdir():
    print(fp)
    
# 2.遍历当前文件夹下文件，包含文件和文件夹名。不包含子文件夹下文件
# 返回结果和 方法1 一样
for fp in root_dir.glob("*"):
    print(fp)
    
# 3. 遍历当前文件夹下所有文件夹，包括子文件夹下的文件夹
for fp in root_dir.glob("**"):
    print(fp)
    
# 4. 遍历当前文件夹下所有文件夹，包括子文件夹下的文件夹
# 返回结果和 方法3 一样
for fp in root_dir.rglob("**"):
    print(fp)
    
# 5.遍历当前文件夹下所有文件，包括子文件夹下的文件夹和文件
for fp in image_dirp.rglob("*"):
    print(fp)
```

- **Path.cwd()**

返回当前工作目录的路径

- **Path.mkdir()**

提供了 parents 参数，设置为 True 可以创建多级目录；不设置则只能创建 一层.

exist_ok=True 则目录已存在时不会抛异常。

```python
path = Path("/test/1")
path.mkdir(parents=True, exist_ok=True)
```

- **Path.is_file()**

判断路径是否为文件

- **Path.is_dir()**

判断路径是否为文件夹

- **Path.unlink()**

删除文件。不能删除目录。

- **Path.rmdir()**

删除目录

- **Path.rename()**

重命名文件名。 相较于`with_name()`方法， 不仅能重命名还能移动到指定路径。保证路径能在设备中找到。 重命名的目标路径文件已经存在则会被当前文件直接替换掉，所以要谨慎。

```python
print(Path("/home/test_images/1.jpg").rename("/home/yoyo.jpg"))
print(Path("/home/test_images/yoyo.jpg").rename("/home/test_images/xx/yoyo.txt"))
```

- **Path.replace()**

重命名文件名。 和`rename()`方法一样。差异在于`rename()`在有的操作系统下如果目标文件路径已经存在则会报错。



### 扩展

**1）PurePath**

PurePath访问实际文件系统的“纯路径”，只负责对路径字符串执行操作。PurePath有两个子类，即PurePosixPath和PathWindowsPath，前者用于操作UNIX（包括 Mac OS X）风格的路径，后者用于操作Windows风格的路径。

**2）Path**

Path访问实际文件系统的“真正路径”，Path对象可用于判断对应的文件是否存在、是否为文件、是否为目录等。有两个子类，即PosixPath和WindowsPath，前者用于操作UNIX（包括 Mac OS X）风格的路径，后者用于操作Windows风格的路径。

**3）PurePath和Path的区别**

Path 是 PurePath 的子类，除了支持 PurePath 的各种操作、属性和方法之外，还会真正访问底层的文件系统，包括判断 Path 对应的路径是否存在，获取 Path 对应路径的各种属性（如是否只读、是文件还是文件夹等），甚至可以对文件进行读写。

PurePath 和 Path 最根本的区别在于，PurePath 处理的仅是字符串，而 Path 则会真正访问底层的文件路径，因此它提供了属性和方法来访问底层的文件系统。

**4）UNIX 和 Windows 风格路径区别**

UNIX 风格的路径和 Windows 风格路径的主要区别在于根路径和路径分隔符，UNIX 风格路径的根路径是斜杠（/），而 Windows 风格路径的根路径是盘符（c:）；UNIX 风格的路径的分隔符是斜杠（/），而 Windows 风格路径的分隔符是反斜杠（\）。



**yolov8中一些使用到的pathlib**

```python
import pathlib
# 判断路径后缀格式
is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)

# 使用正则表达式，得到满足要求的文件
Path(labels_dir).resolve().glob('*.json')

# 查找指定路径下的所有 .DS_store 文件，并将它们的路径存储在一个列表中。
# rglob() 递归地遍历指定目录及其所有子目录，寻找与给定模式匹配的所有文件和目录。
files = list(Path(path).rglob('.DS_store'))

# 
path=Path('./labels.cache')
desc = f'{self.prefix}Scanning {path.parent / path.stem}...'
if is_dir_writeable(path.parent):
    if path.exists():
        path.unlink()  # remove *.cache file if exists
        np.save(str(path), x)  # save cache for next time
        path.with_suffix('.cache.npy').rename(path)  # remove .npy suffix
        
#         
cache_path = Path(self.label_files[0]).parent.with_suffix('.cache')


self.samples = [list(x) + [Path(x[0]).with_suffix('.npy'), None] for x in self.samples]


sources = Path(sources).read_text().rsplit() if os.path.isfile(sources) else [sources]


if isinstance(path, str) and Path(path).suffix == '.txt': 
    parent = Path(path).parent
    path = Path(path).read_text().rsplit()

# 
path = Path(dir_path)
txt = ['autosplit_train.txt', 'autosplit_val.txt', 'autosplit_test.txt']  # 3 txt files
for x in txt:
    if (path.parent / x).exists():
        (path.parent / x).unlink()  # remove existing    
#        
f = Path(str(self.file).replace(self.file.suffix, f'_ncnn_model{os.sep}'))

#
for f_debug in 'debug.bin', 'debug.param', 'debug2.bin', 'debug2.param':  
    Path(f_debug).unlink(missing_ok=True)
    
# 
f = Path(str(self.file).replace(self.file.suffix, '_saved_model'))

#
file = self.save_dir / 'labels' / f'{Path(batch["im_file"][si]).stem}.txt'

#
dt = (datetime.now() - datetime.fromtimestamp(Path(path).stat().st_mtime))  # delta

```



ref：

[pathlib 官方文档](https://docs.python.org/3.4/library/pathlib.html)

https://zhuanlan.zhihu.com/p/475661402

https://blog.csdn.net/weixin_44878336/article/details/139494419

