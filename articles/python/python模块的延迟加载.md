## 延迟加载

### 传统的模块导入方式（即时加载 / 非延迟）

```python
import torch
from myproject.models import some_model
from myproject.models.some_model import SomeClass
```

这些导入操作会在 Python 解释器执行到这一行代码时，立即执行！

也就是说：

1. Python 会立刻加载整个模块（包括其依赖）
2. 执行模块里的所有顶层代码（比如函数定义、类定义、可能的 print、配置加载、网络请求等）
3. 如果某个模块导入失败（比如缺少依赖），程序直接报错崩溃
4. 即使你根本没用到某些模块，它们也被加载进来了，浪费内存和启动时间

### 延迟加载（Lazy Import/按需加载）

> **不是在一开始就加载所有模块，而是等到用户真正去访问某个模块、类、函数时，才去加载它。**

写 from myproject.models import SomeModel，但此时并不会真的去加载 SomeModel所在的模块。

只有当你真正写出 model = SomeModel(...)或者访问 SomeModel的属性时，Python 才去真正地 import 它。

这样带来的好处是：

1. 极大加快程序启动速度（特别是大型库，比如有几十甚至上百个子模块）

2. 减少不必要的依赖加载（比如用户只用 OCR 模型，却不用 NLP 模块，那么 NLP 模块及其依赖就不会被加载）

3. 避免启动时报错（比如某个子模块依赖某个库，但用户根本不用它，就不会因为缺少该库导致程序启动失败）

4. 节省内存开销

## 真正的访问

```python
# 假设这是懒加载模式下的导入
from myproject.models import text_generation

# 下面这行才是“真正访问”
model = text_generation.TextGenerator("some-model-name")
```

在上面的例子中：

- 当你写 `from myproject.models import text_generation`时，**并不会真的加载 text_generation 模块**
- 只有当你 **实际创建对象 `TextGenerator(...)`时，才会触发对 `text_generation`的访问，此时才会真正去加载对应的模块**



## 延迟加载如何实现的

`LazyImportModule`是一个自定义的 Python 模块类，它继承自 `types.ModuleType`，**它伪装成一个普通的模块，但实际上对模块内的属性访问进行了拦截和控制。**关键点在于它重写了： `__getattr__(self, name: str) -> Any`**

这是 Python 在你访问一个模块中 **不存在的属性时调用的魔术方法**。

比如你写：

```python
import some_lazy_module
obj = some_lazy_module.SomeClass  # 假设 SomeClass 还没被真正导入
```

如果 `some_lazy_module`是一个普通的模块，Python 会尝试直接获取 `SomeClass`，如果找不到就报错。

但如果 `some_lazy_module`是一个 `LazyImportModule`，那么当访问 `some_lazy_module.SomeClass`时：

1. `__getattr__('SomeClass')`被触发
2. 检查 `SomeClass`是否属于需要延迟加载的类
3. **如果还没加载，则动态调用 `importlib.import_module()`去真正加载那个子模块**
4. 然后返回真正的 `SomeClass`对象
5. **以后再访问 `SomeClass`就直接返回缓存值，不用重复加载**

### 举个现实中的例子 

#### 没有 LazyImport（普通导入，Eager 方式）

假设你的库结构如下：

```bash
myproject/
├── __init__.py
├── models/
│   ├── __init__.py         ← 这里导入了所有模型：textgen, imagecls, objdet...
│   ├── textgen.py          ← 包含 TextGenerator
│   ├── imagecls.py         ← 包含 ImageClassifier
│   └── objdet.py           ← 包含 ObjectDetector
```

然后在 `models/__init__.py`中你写了：

```python
from .textgen import TextGenerator
from .imagecls import ImageClassifier
from .objdet import ObjectDetector
```

那么问题来了：

- **只要有人 `import myproject.models`，就会加载所有三个类及其依赖**
- **如果用户只用文本生成，但图像分类模块依赖某个很重的库（比如 OpenCV、TensorFlow），也会被强行加载**
- **如果某个子模块依赖缺失，整个 myproject.models 都导入失败！**
- **启动速度变慢，尤其是模块很多时**

#### 使用 LazyImport（推荐方式）

在 `models/__init__.py`中你不再直接导入所有类，而是：

```python
import sys
from myproject.utils.lazy_import import LazyImportModule

# 定义一个字典，告诉 LazyImport 哪些名称对应哪些模块
_import_structure = {
    "textgen": ["TextGenerator"],
    "imagecls": ["ImageClassifier"],
    "objdet": ["ObjectDetector"],
}

# 当前模块名
current_module_name = __name__

# 把当前模块替换为一个 LazyImportModule
sys.modules[current_module_name] = LazyImportModule(
    name=current_module_name,
    module_file=__file__,
    import_structure=_import_structure,
    module_spec=__spec__,
)
```

这意味着,当用户写：

```
from myproject.models import textgen
model = textgen.TextGenerator(...)
```

- `import myproject.models`时，**不会加载任何子模块**
- `from myproject.models import textgen`时，**仍然不会加载真正的 textgen 模块**
- **只有当你执行 `textgen.TextGenerator(...)`时，才会真正去导入 `textgen.py`并加载 `TextGenerator`类**



## 有 LazyImport 和没有的区别

| 场景             | 没有 LazyImport（传统导入）                 | 有 LazyImport（延迟加载）                     |
| :--------------- | :------------------------------------------ | :-------------------------------------------- |
| **导入时机**     | import 语句执行时，立即加载所有子模块和依赖 | 只有在用户真正访问某个类/函数时才加载对应模块 |
| **启动速度**     | 慢（尤其是模块多、依赖复杂时）              | 快（只加载用到的部分）                        |
| **内存占用**     | 高（所有模块常驻内存）                      | 低（按需加载，不用不加载）                    |
| **依赖管理**     | 一旦某个子模块依赖缺失，整个导入失败        | 缺少某个依赖？没关系，只要你不访问它          |
| **灵活性**       | 弱（所有模块必须能导入）                    | 强（可以按需提供功能模块）                    |
| **错误提示时机** | 启动时报错（可能用户根本不用那个模块）      | 真正使用时才报错，更精准                      |



## LazyImport 样例代码

`__init__.py`

```python
from typing import TYPE_CHECKING

from myproject.utils.import_utils import LazyImportModule

if TYPE_CHECKING:
    from .yolo import YOLOv12_ONNX
    from .grounding_dino import GroundingDINO

else:
    _import_structure = {'yolo': ['YOLOv12_ONNX'],
                         'grounding_dino': ['GroundingDINO']}

    import sys

    sys.modules[__name__] = LazyImportModule(
        __name__,
        globals()['__file__'],
        _import_structure,
        module_spec=__spec__,
        extra_objects={},
    )

```

`import_utils.py`

```python
# ref: modelscope/utils/import_utils.py
import importlib
import logging
import os
from importlib import import_module
from itertools import chain
from pathlib import Path
from types import ModuleType
from typing import Any

from xt_maas.utils.logger import get_logger

logger = get_logger(log_level=logging.WARNING)


class LazyImportModule(ModuleType):
    def __init__(self,
                 name,
                 module_file,
                 import_structure,
                 module_spec=None,
                 extra_objects=None,
                 try_to_pre_import=False,
                 extra_import_func=None):
        super().__init__(name)
        self._modules = set(import_structure.keys())
        self._class_to_module = {}
        for key, values in import_structure.items():
            for value in values:
                self._class_to_module[value] = key
        # Needed for autocompletion in an IDE
        self.__all__ = list(import_structure.keys()) + list(
            chain(*import_structure.values()))
        self.__file__ = module_file
        self.__spec__ = module_spec
        self.__path__ = [os.path.dirname(module_file)]
        self._objects = {} if extra_objects is None else extra_objects
        self._name = name
        self._import_structure = import_structure
        self._extra_import_func = extra_import_func
        if try_to_pre_import:
            self._try_to_import()

    def _try_to_import(self):
        for sub_module in self._class_to_module.keys():
            try:
                getattr(self, sub_module)
            except Exception as e:
                logger.warning(
                    f'pre load module {sub_module} error, please check {e}')

    # Needed for autocompletion in an IDE
    def __dir__(self):
        result = super().__dir__()
        # The elements of self.__all__ that are submodules may or may not be in the dir already, depending on whether
        # they have been accessed or not. So we only add the elements of self.__all__ that are not already in the dir.
        for attr in self.__all__:
            if attr not in result:
                result.append(attr)
        return result

    def __getattr__(self, name: str) -> Any:
        if name in self._objects:
            return self._objects[name]
        if name in self._modules:
            value = self._get_module(name)
        elif name in self._class_to_module.keys():
            module = self._get_module(self._class_to_module[name])
            value = getattr(module, name)
        elif self._extra_import_func is not None:
            value = self._extra_import_func(name)
            if value is None:
                raise AttributeError(
                    f'module {self.__name__} has no attribute {name}')
        else:
            raise AttributeError(
                f'module {self.__name__} has no attribute {name}')

        setattr(self, name, value)
        return value

    def _get_module(self, module_name: str):
        try:
            # module_name_full = self.__name__ + '.' + module_name
            return importlib.import_module('.' + module_name, self.__name__)
        except Exception as e:
            raise RuntimeError(
                f'Failed to import {self.__name__}.{module_name} because of the following error '
                f'(look up to see its traceback):\n{e}') from e

    def __reduce__(self):
        return self.__class__, (self._name, self.__file__,
                                self._import_structure)

```

