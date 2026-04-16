## python包安装问题

### 库打包安装方式

| 目的                   | 典型命令           | 备注                                                         |
| ---------------------- | ------------------ | ------------------------------------------------------------ |
| 普通安装（wheel）      | `pip install .`    | 临时在 `build/` 里打 wheel 再装；干净、可缓存。              |
| 可编辑安装（开发模式） | `pip install -e .` | 用 PEP 660 机制，只在 site-packages 放一个 `.pth` 或 `.egg-link`，代码原地不动。 |
| 手动打 wheel/源码包    | `python -m build`  | 生成 `dist/*.whl` 和 `dist/*.tar.gz`，之后可 `pip install dist/xxx.whl`。 |

打包相关的新旧命令对照

| 老命令（已不推荐）                  | 现代命令                  | 说明           |
| :---------------------------------- | :------------------------ | :------------- |
| `python setup.py sdist`             | `python -m build --sdist` | 生成源码发布包 |
| `python setup.py bdist_wheel`       | `python -m build --wheel` | 生成 wheel     |
| `python setup.py sdist bdist_wheel` | `python -m build`         | 一次生成两种包 |
| `python setup.py develop`           | `pip install -e .`        | 可编辑安装     |

> 从 setuptools 2023 起，`setup.py develop` 已被标记为 **legacy**，官方文档直接建议改用 `pip install -e .`。

### setup.py 和setup.cfg和pyproject.toml差异

| 方法                                                      | 是否可以单独使用？     | 说明                                                         |
| :-------------------------------------------------------- | :--------------------- | :----------------------------------------------------------- |
| **1.  `setup.py`（单独使用）**                            | **可以**               | 传统的、标准的、通过 Python 脚本定义包安装逻辑               |
| **2.  `setup.cfg`**                                       | **不可以完全单独使用** | 声明式的、静态配置（INI 格式），但不能定义复杂的动态逻辑     |
| **3. `pyproject.toml`（单独使用）**                       | **可以完全单独使用**   | 定义构建系统与工具链                                         |
| **4.  `pyproject.toml`+ `setup.cfg`（推荐组合）**         | **推荐**               | `pyproject.toml`定义构建后端（如 setuptools），`setup.cfg`定义包元数据等 |
| **5. `pyproject.toml`+ `setup.py`（也可组合）**           | 可以，但不推荐         | 混用，逐渐淘汰 `setup.py`                                    |
| **6.  仅 `pyproject.toml`（无 setuptools 后端或包定义）** | **不行**               | 仅配置构建系统，没有告诉 Python 如何构建/安装包              |

### Others

- **为什么现在很多项目都要安装后运行？**

是否是因为需要将当前项目安装到当前 Python 环境中，从而可以在任意路径下调用包中的模块。

- **可以怎样将当前项目安装成包？**

使用`setup.py `或 `pyproject.toml`构建包。

- **当同时存在pyproject.toml和setup.py时 使用pip install -e .安装的是哪个？**

当项目目录下同时存在 `pyproject.toml` 和 `setup.py` 文件时，`pip install -e .` 的行为遵循 PEP 517 和 PEP 660 的标准。具体来说：

1. **如果 `pyproject.toml` 中声明了 `[build-system]` 表**，指定了 `build-backend`（例如 `setuptools.build_meta`），那么 pip 将会使用这个 **现代构建后端** 来处理安装，包括可编辑安装（editable install）。此时，`pyproject.toml` 中的配置是主导，而 `setup.py` 则作为构建后端（如 setuptools）的辅助配置文件。
2. **如果 `pyproject.toml` 存在，但没有声明 `[build-system]` 表**，那么 pip 会默认使用传统的 setuptools 构建系统，并退回到读取 `setup.py` 来处理安装。
3. **如果 `pyproject.toml` 不存在**，pip 则会完全依赖于 `setup.py` 来进行安装。

因此，在现代 Python 打包实践中，**`pyproject.toml` 的优先级高于 `setup.py`**。当两者同时存在，且 `pyproject.toml` 正确配置了构建系统时，`pip install -e .` 会根据 `pyproject.toml` 中的设置来执行安装，而不是直接执行 `setup.py`。**如果只有pyproject.toml我是否可以直接用pip install -e .来安装**

- **为什么建议 `pyproject.toml`构建包**

  - 现代化：符合 PEP 517 / 518，是当前 Python 打包推荐标准 

  - 统一构建 ：不再依赖单独的 `setup.py`，构建过程更规范


  - 灵活后端：可以使用 `setuptools`（兼容老项目）、`poetry`、`flit`、`hatch`等构建工具


  - 被 pip 认可：pip 和所有现代工具都会优先查找 `pyproject.toml`来构建包 


  - 支持复杂配置：比如构建依赖、可选依赖、版本控制等  



## setup.cfg

`setup.cfg`是 setuptools 提供的一种 静态配置文件（INI 格式），用于定义你的 Python 包的元数据（如名称、版本、依赖等），而无需编写 Python 代码形式的 `setup.py`。它通常与 `pyproject.toml`一起使用（特别是在现代打包中），或者在一些简单项目中 可以完全替代 `setup.py`。

`modelscope`项目的`setup.cfg`:

```ini
[isort]
line_length = 79
multi_line_output = 0
known_standard_library = setuptools
known_first_party = modelscope
known_third_party = json,yaml
no_lines_before = STDLIB,LOCALFOLDER
default_section = THIRDPARTY

[yapf]
BASED_ON_STYLE = pep8
BLANK_LINE_BEFORE_NESTED_CLASS_OR_DEF = true
SPLIT_BEFORE_EXPRESSION_AFTER_OPENING_PAREN = true
SPLIT_BEFORE_ARITHMETIC_OPERATOR = true

[codespell]
skip = *.ipynb
quiet-level = 3
ignore-words-list = patten,nd,ty,mot,hist,formating,winn,gool,datas,wan,confids

[flake8]
max-line-length = 120
select = B,C,E,F,P,T4,W,B9
ignore = F401,F403,F405,F821,W503,E251
exclude = docs/src,*.pyi,.git

[darglint]
ignore=DAR101

```



## setup.py

simple

```python
from setuptools import setup, find_packages

setup(
    name="haha",
    version="v1.1",
    packages=find_packages(),
    include_package_data=True, 
    description="haha Python Package",
    author="zhaosilu",
    author_email="zhaosilu1125oto@gmail.com",
    python_requires=">=3.9",
)
```

`modelscope的setup.py`， 涉及：

读取 README.md 作为长描述

动态获取版本号

解析 requirements.txt 文件，提取依赖项

资源打包相关（拷贝模型、配置、文档等）



## pyproject.toml

my simple:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "haha"
version = "v1.1"
description = "haha Python Package"
authors = [
    {name = "zhaosilu", email = "zhaosilu1125oto@gmail.com"},
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"

dependencies = []

[tool.setuptools.packages.find]
where = ["."] 
include = ["haha*"]
exclude = ["tests*", "docs*", "outputs*", "weights*"]

```

可使用`pip installl -e .` 进行安装



### 重要的选项和格式

根据 `ultralytics`和`ragflow`项目下的pyproject.toml文件

以下为ultralystics的toml阉割版

```toml
[build-system]
requires = ["setuptools>=70.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ultralytics"
dynamic = ["version"]
description = "Ultralytics YOLO 🚀 for SOTA object detection, multi-object tracking, instance segmentation, pose estimation and image classification."
readme = "README.md"
requires-python = ">=3.8"
license = { "text" = "AGPL-3.0" }
keywords = ["machine-learning"]
authors = [
    { name = "Glenn Jocher", email = "glenn.jocher@ultralytics.com" },
    { name = "Jing Qiu", email = "jing.qiu@ultralytics.com" },
]
maintainers = [
    { name = "Ultralytics", email = "hello@ultralytics.com" },
]
classifiers = [
    "Development Status :: 4 - Beta",
]

# 必要依赖
dependencies = [
    "numpy>=1.23.0",
    "matplotlib>=3.3.0",
]

# 可选依赖
[project.optional-dependencies]
dev = [
    "ipython",
    "pytest",
]
export = [
    "numpy<2.0.0", # TF 2.20 compatibility
    "onnx>=1.12.0,<1.18.0", # ONNX export
]


[project.urls]
"Homepage" = "https://ultralytics.com"
"Source" = "https://github.com/ultralytics/ultralytics"
"Documentation" = "https://docs.ultralytics.com"
"Bug Reports" = "https://github.com/ultralytics/ultralytics/issues"
"Changelog" = "https://github.com/ultralytics/ultralytics/releases"


[project.scripts]
yolo = "ultralytics.cfg:entrypoint"
ultralytics = "ultralytics.cfg:entrypoint"

# Tools settings -------------------------------------------------------------------------------------------------------
[tool.setuptools]  # configuration specific to the `setuptools` build backend.
packages = { find = { where = ["."], include = ["ultralytics", "ultralytics.*"] } }
# Tests included below for checking Conda builds in https://github.com/conda-forge/ultralytics-feedstock
package-data = { "ultralytics" = ["**/*.yaml", "**/*.sh", "../tests/*.py"], "ultralytics.assets" = ["*.jpg"], "ultralytics.solutions.templates" = ["*.html"]}

[tool.setuptools.dynamic]
version = { attr = "ultralytics.__version__" }

[tool.pytest.ini_options]
addopts = "--doctest-modules --durations=30 --color=yes"
markers = [
    "slow: skip slow tests unless --slow is set",
]
norecursedirs = [".git", "dist", "build"]

[tool.coverage.run]
source = ["ultralytics/"]
data_file = "tests/.coverage"
omit = ["ultralytics/utils/callbacks/*"]

[tool.isort]
line_length = 120
multi_line_output = 0

[tool.yapf]
based_on_style = "pep8"
spaces_before_comment = 2
column_limit = 120
coalesce_brackets = true
spaces_around_power_operator = true
space_between_ending_comma_and_closing_bracket = true
split_before_closing_bracket = false
split_before_first_argument = false

[tool.ruff]
line-length = 120

[tool.ruff.format]
docstring-code-format = true

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.docformatter]
wrap-summaries = 120
wrap-descriptions = 120
pre-summary-newline = true
close-quotes-on-newline = true
in-place = true

[tool.codespell]
ignore-words-list = "crate,nd,ned,strack,dota,ane,segway,fo,gool,winn,commend,bloc,nam,afterall"
skip = '*.pt,*.pth,*.torchscript,*.onnx,*.tflite,*.pb,*.bin,*.param,*.mlmodel,*.engine,*.npy,*.data*,*.csv,*pnnx*,*venv*,*translat*,__pycache__*,*.ico,*.jpg,*.png,*.mp4,*.mov,/runs,/.git,./docs/??/*.md,./docs/mkdocs_??.yml'

```

上面的这些`tool`:

| 段落                                                   | 工具名称         | 一句话作用                                                   | 删掉会怎样                                            |
| :----------------------------------------------------- | :--------------- | :----------------------------------------------------------- | :---------------------------------------------------- |
| `[tool.pytest.ini_options]`                            | **pytest**       | Python 最流行的单测框架；这里决定发现测试的方式、命令行默认参数。 | 根目录没有 `pytest.ini` 就会用默认值，不影响打包。    |
| `[tool.coverage.run]`                                  | **coverage.py**  | 统计单元测试的代码覆盖率；CI 报告里常见的 “92 % coverage” 就是它算的。 | 没有就测不到覆盖率，打包/安装完全无影响。             |
| `[tool.isort]`                                         | **isort**        | 自动把 `import` 按 PEP 8 规则排序、分段。                    | 不排序 import 也能跑，只是代码风格问题。              |
| `[tool.yapf]`                                          | **YAPF**         | Google 出品的代码格式化工具，把整份 `.py` 文件重排成统一风格。 | 不需要可以删；很多项目改用 `ruff format` 或 `black`。 |
| `[tool.ruff]` + `ruff.format` + `ruff.lint.pydocstyle` | **Ruff**         | 极快的 Python linter + formatter，一条命令搞定 flake8/black/isort/pydocstyle。 | 删掉后需换回 flake8/black 等组合。                    |
| `[tool.docformatter]`                                  | **docformatter** | 专门格式化 docstring（行宽、空行、引号）。                   | 不格式化 docstring 也能跑。                           |
| `[tool.codespell]`                                     | **codespell**    | 检查英文注释 / 文档里的常见拼写错误。                        | 不检查拼写无影响。                                    |

这些都是 **开发体验工具**；跟 `pip install ultralytics` 之后能不能 `import ultralytics` 完全无关。如果只想“打包发布”，可以把所有 `[tool.*]` 段都删掉，项目照样能装、能用，但是看起来牛逼。

