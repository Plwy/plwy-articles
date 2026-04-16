

## 日志管理模块样例

来自：`modelscope/utils/logger.py`

```python
# Copyright (c) Alibaba, Inc. and its affiliates.

import importlib.util as iutil
import logging
import os
from typing import Optional

init_loggers = {}

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

default_log_level = int(os.getenv('MODELSCOPE_LOG_LEVEL', str(logging.INFO)))
logging.getLogger('numba').setLevel(logging.INFO)


def get_logger(log_file: Optional[str] = None,
               log_level: int = default_log_level,
               file_mode: str = 'w'):
    """ Get logging logger

    Args:
        log_file: Log filename, if specified, file handler will be added to
            logger
        log_level: Logging level.
        file_mode: Specifies the mode to open the file, if filename is
            specified (if filemode is unspecified, it defaults to 'w').
    """

    logger_name = __name__.split('.')[0]
    logger = logging.getLogger(logger_name)
    logger.propagate = False
    if logger_name in init_loggers:
        add_file_handler_if_needed(logger, log_file, file_mode, log_level)
        if logger.level != log_level:
            logger.setLevel(log_level)
        return logger

    # handle duplicate logs to the console
    # Starting in 1.8.0, PyTorch DDP attaches a StreamHandler <stderr> (NOTSET)
    # to the root logger. As logger.propagate is True by default, this root
    # level handler causes logging messages from rank>0 processes to
    # unexpectedly show up on the console, creating much unwanted clutter.
    # To fix this issue, we set the root logger's StreamHandler, if any, to log
    # at the ERROR level.
    torch_dist = False
    is_worker0 = True
    if iutil.find_spec('torch') is not None:
        from modelscope.utils.torch_utils import is_dist, is_master
        torch_dist = is_dist()
        is_worker0 = is_master()

    if torch_dist:
        for handler in logger.root.handlers:
            if type(handler) is logging.StreamHandler:
                handler.setLevel(logging.ERROR)

    stream_handler = logging.StreamHandler()
    handlers = [stream_handler]

    if is_worker0 and log_file is not None:
        file_handler = logging.FileHandler(log_file, file_mode)
        handlers.append(file_handler)

    for handler in handlers:
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        logger.addHandler(handler)

    if is_worker0:
        logger.setLevel(log_level)
    else:
        logger.setLevel(logging.ERROR)

    init_loggers[logger_name] = True

    return logger


def add_file_handler_if_needed(logger, log_file, file_mode, log_level):
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return

    if iutil.find_spec('torch') is not None:
        from modelscope.utils.torch_utils import is_master
        is_worker0 = is_master()
    else:
        is_worker0 = True

    if is_worker0 and log_file is not None:
        file_handler = logging.FileHandler(log_file, file_mode)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

```

- 支持torch分布式日志，通过is_worker0控制。

  主进程：按用户设置的级别输出日志。

  非主进程：只记录 `ERROR` 级别以上的日志，**避免分布式训练时大量重复日志刷屏**。

- 统一格式与日志级别

- 避免重复日志，支持文件输出。



## **logger和handler的理解**

**Logger**（记录器）是应用程序直接使用的接口，它提供了不同级别的日志记录方法（如 `debug()`、`info()`、`warning()`、`error()` 和 `critical()`）。每个记录器都有一个名称，并且可以配置不同的日志级别和处理器（handlers）。记录器可以通过层级关系组织起来（例如，通过使用点号分隔的命名方式），这样可以方便地控制一组相关记录器的日志行为。

- 这里创建了一个名为 `logger_name` 的 `Logger` 实例。
- `__name__.split('.')[0]` 通常会得到当前模块所属包的名字，这意味着所有来自同一包的模块可以共享同一个 logger。
- `logger.propagate = False`：防止日志消息传播给父级记录器（通常是 root logger），以避免重复日志输出。



**Handler**（处理器）负责将日志记录输出到不同的目的地。比如，你可以有一个处理器将错误信息发送到电子邮件，另一个处理器将调试信息写入文件，还有一个处理器将所有信息打印到控制台等。每个处理器都可以设置自己的日志级别过滤器、格式化器（Formatter）等。

这里有两种类型的处理器被使用：

- **StreamHandler**：输出日志到流（通常是标准输出或标准错误输出）。

- **FileHandler**：将日志写入到指定的文件中。



**Logger** 负责生成日志消息，并决定这些消息的重要性（即日志级别）。它还可以包含多个处理器。

**Handler** 则负责决定如何处理这些日志消息，包括它们应该被输出到哪里（比如控制台、文件等）、采用什么样的格式等。



##  基于loguru的日志系统

这里使用`loguru`库实现日志管理，相较于原生`logging`有以下优势：

彩色日志, 文件切割, 异步写入, 日志轮转等实现十分简单易用。



```python
import os
import sys
import time
import logging
from types import FrameType
from typing import cast
from loguru import logger


class Logger:
    """输出日志到文件和控制台"""

    def __init__(self, log_dir="./log"):
        # 文件的命名
        log_name = f"{time.strftime('%Y-%m-%d', time.localtime()).replace('-', '_')}.log"
        log_path = os.path.join(log_dir, log_name)
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 判断日志文件夹是否存在，不存则创建
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        # 日志输出格式
        formatter = "{time:YYYY-MM-DD HH:mm:ss} | {level}: {message}"
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        self.logger.add(sys.stdout,
                        format="<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 进程名
                               "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                               ":<cyan>{line}</cyan> | "  # 行号
                               "<level>{level}</level>: "  # 等级
                               "<level>{message}</level>",  # 日志内容
                        )
        # 日志写入文件
        self.logger.add(log_path,  # 写入目录指定文件
                        format='{time:YYYYMMDD HH:mm:ss} - '  # 时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 进程名
                               '{module}.{function}:{line} - {level} -{message}',  # 模块名.方法名:行号
                        encoding='utf-8',
                        retention='7 days',  # 设置历史保留时长
                        backtrace=True,  # 回溯
                        diagnose=True,  # 诊断
                        enqueue=True,  # 异步写入
                        rotation="00:00",  # 每日更新时间
                        # rotation="5kb",  # 切割，设置文件大小，rotation="12:00"，rotation="1 week"
                        # filter="my_module"  # 过滤模块
                        # compression="zip"   # 文件压缩
                        )

    def init_config(self):
        LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")

        # change handler for default uvicorn logger
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in LOGGER_NAMES:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler()]

    def get_logger(self):
        return self.logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


def init_log():
    loggers = Logger()
    log = loggers.get_logger()
    return loggers, log
```

调用：

```python
from log_utils import init_log
loggers, logger = init_log()
app = FastAPI()
@app.get("/get_hello")
async def get_hello():
    logger.info(f"return success")
    return {"data": "hello"}    


if __name__ == '__main__':
    app_config = uvicorn.Config("server:app", host="0.0.0.0", port=8000)
    server = uvicorn.Server(app_config)
    loggers.init_config()
```

**`InterceptHandler` 类**：

拦截所有通过 logging 模块输出的日志（如第三方库 uvicorn、requests 等）。将这些日志统一转发给 loguru 的 logger，实现日志输出的统一管理。

- 这里通过继承自`logging.Handler` 使其可以作为标准 `logging` 模块中的一个处理器使用。

- 重写了 `logging.Handler` 类中用来发送日志记录的`emit`方法。
- 通过循环调用栈，寻找日志的发起者，即确定哪个文件的哪一行代码触发了这条日志。
- 确定了正确的级别和调用者信息，使用 loguru.logger.opt()方法 发送日志。

**`init_config()`实现**

这里专门接管 `Uvicorn`（FastAPI 服务器）相关的日志，使其也按照 `loguru` 的格式和输出方式。

通过将`InterceptHandler()`设置为指定名称记录器的唯一处理器。（如uvicorn这些记录器）
