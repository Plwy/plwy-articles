关于服务中进行**懒加载实现高效服用**， 在第一次请求加载模型，后面的请求复用加载的模型。不用的服务启动时显示进行模型初始化。

### 懒加载高效复用

mineru的源码

```python
class ModelSingleton:
    _instance = None
    _models = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_model(
        self,
        lang=None,
        formula_enable=None,
        table_enable=None,
    ):
        key = (lang, formula_enable, table_enable)
        if key not in self._models:
            self._models[key] = custom_model_init(
                lang=lang,
                formula_enable=formula_enable,
                table_enable=table_enable,
            )
        return self._models[key]


def custom_model_init(
    lang=None,
    formula_enable=True,
    table_enable=True,
):
    model_init_start = time.time()
    # 从配置文件读取model-dir和device
    device = get_device()

    formula_config = {"enable": formula_enable}
    table_config = {"enable": table_enable}

    model_input = {
        'device': device,
        'table_config': table_config,
        'formula_config': formula_config,
        'lang': lang,
    }

    custom_model = MineruPipelineModel(**model_input)

    model_init_cost = time.time() - model_init_start
    logger.info(f'model init cost: {model_init_cost}')

    return custom_model
```

**懒加载 + 单例模式**

#### 关键点分析：

| 特性           | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| `__new__` 单例 | 确保整个程序中只有一个 `ModelSingleton` 实例（进程级单例）   |
| `_models` 字典 | 以 `(lang, formula, table)` 为 key，缓存不同配置的模型       |
| `get_model()`  | 如果该配置的模型不存在，就调用 `custom_model_init` 创建并缓存；否则直接返回 |

> ✅ **这就是“懒加载”的核心：第一次请求某个配置的模型时才创建，之后直接复用。**

#### 为什么能做到“不重复初始化”？

1. **Python 进程生命周期长**：FastAPI 服务启动后，整个 Python 进程一直运行。
2. **`ModelSingleton._models` 是模块级静态变量**：只要进程不退出，缓存就不会丢失。
3. **`__new__` 控制单例**：确保 `ModelSingleton()` 每次返回的是同一个对象。
4. **`get_model()` 实现缓存逻辑**：避免重复调用耗时的 `custom_model_init`
