# python 服务相关

什么是WSGI，ASGI

WSGI和ASGI区别

常见python web框架 ，服务器







## WSGI

### **WSGI是什么**

WSGI(Web Server Gateway Interface， Web服务网关接口)，指定了web服务器和Python web应用或web框架之间的标准接口，以提高web应用在一系列web服务器间的移植性。 具体可查看 [官方文档](https://link.zhihu.com/?target=https%3A//www.python.org/dev/peps/pep-0333/)

从以上介绍我们可以看出：

1. **WSGI是一套接口标准协议/规范；**
2. 通信（作用）区间是Web服务器和Python Web应用程序之间；
3. **目的是制定标准，以保证不同Web服务器可以和不同的Python程序之间相互通信**

### **WSGI的作用**

Web服务器需要和web应用程序进行通信，但是web服务器有很多种啊，Python web应用开发框架也对应多种啊，所以WSGI应运而生，定义了一套通信标准。试想一下，如果不统一标准的话，就会存在Web框架和Web服务器数据无法匹配的情况，那么开发就会受到限制，这显然不合理的。



## ASGI

### ASGI 是什么？

ASGI 全称 (Asynchronous Server Gateway Interface, 异步服务网关接口)。它**定义了一套标准接口规范，用于连接 Web 服务器和应用程序框架，实现异步处理请求和响应**。ASGI 的目标是提供高性能、可伸缩和灵活的 Web 应用程序开发体验。

### 为什么需要 ASGI？

传统的 Python Web 服务器（如 WSGI）在处理请求时通常采用同步的方式，即每个请求都会阻塞服务器线程，导致服务器无法同时处理大量并发请求。而 **ASGI 规范引入了异步编程模型，使得服务器能够以非阻塞的方式处理请求，实现更好的并发性能和扩展性。**

ASGI 还允许使用异步的应用程序框架，例如使用异步函数 async、协程或异步 IO asyncio 操作来处理请求。这种异步编程模型可以提供更高的性能，并允许处理复杂的并发操作，如长轮询、WebSocket 等。另外，ASGI 还支持中间件和插件机制，使得开发者可以方便地扩展和定制服务器和应用程序的功能。

### 如何使用 ASGI？

要使用 ASGI，你需要选择一个符合 ASGI 规范的服务器和一个符合 ASGI 规范的应用程序框架。

- 服务器：**常见的 ASGI 服务器包括 Uvicorn、Daphne、Hypercorn 等**。你可以使用 pip 安装它们，并按照各自的文档进行配置和启动。

- 应用程序框架：**常见的 ASGI 应用程序框架包括 FastAPI、Starlette、Django、Tornado 等。**这些框架都符合 ASGI 规范，并提供了异步处理请求和响应的功能。你可以选择其中一个框架，根据文档编写应用程序逻辑，并将其与 ASGI 服务器进行绑定。

在配置和启动 ASGI 服务器时，你需要指定应用程序的入口点，即 ASGI 应用程序对象。服务器将会监听指定的地址和端口，并开始接收来自客户端的请求，将其传递给应用程序进行处理。

## Web 应用程序开发框架和 Web 服务器

### 常见的 Python Web 应用程序开发框架

1. **Django**
   - **类型**：全功能、高级框架
   - 特点：
     - 内置 ORM（对象关系映射）
     - 自带管理后台
     - 强大的用户认证系统
     - 支持异步视图（从 Django 3.1 开始）
     - 社区活跃，文档丰富
   - **适用场景**：适合构建复杂、数据驱动的应用程序，如企业级应用、大型网站等。
2. **Flask**
   - **类型**：轻量级微框架
   - 特点：
     - 灵活性高，易于扩展
     - 没有内置数据库抽象层或表单验证等组件，但可以通过插件扩展
     - 支持同步和异步视图（从 Flask 2.0 开始）
     - 学习曲线平缓，适合快速开发小型到中型应用
   - **适用场景**：适合小型项目、API服务、微服务架构等。
3. **FastAPI**
   - **类型**：现代、高性能框架
   - 特点：
     - 异步优先，基于 Python 的 `async` 和 `await`
     - 自动生成交互式 API 文档（Swagger UI 和 ReDoc）
     - 极高的性能，接近 Node.js 和 Go
     - 强大的数据验证和序列化支持（通过 Pydantic）
   - **适用场景**：适合构建高性能的 API 服务、微服务、实时应用等。

4.**Tornado**

- **类型**：异步网络库和Web框架
- 特点：
  - 内置异步处理能力
  - 支持 WebSocket 和长连接
  - 高并发处理能力强
- **适用场景**：适合需要处理大量并发连接的应用，如实时聊天应用、游戏服务器等。

### 常见的 Python Web 服务器

1. **Gunicorn**

   - **类型**：WSGI HTTP 服务器
   - 特点：
     - 高性能，支持多进程和多线程
     - 易于配置和部署
     - 广泛用于生产环境中的 WSGI 应用
   - **适用场景**：适合运行基于 WSGI 的应用，如 Django 和 Flask。

2. **uWSGI**

   - **类型**：WSGI/HTTP/Unix Socket 服务器
   - 特点：
     - 支持多种协议（包括 WSGI、HTTP、WebSocket 等）
     - 配置灵活，性能强大
     - 可以作为应用服务器直接运行 Python 应用
   - **适用场景**：适合需要高度定制化和高性能的应用。

3. **Uvicorn**

   - **类型**：ASGI HTTP 服务器
   - 特点：
     - 高性能，专注于异步应用
     - 支持 ASGI 标准，适用于 FastAPI 等异步框架
     - 轻量且易于配置
   - **适用场景**：适合运行异步应用，如 FastAPI、Starlette 等。

4. **Hypercorn**

   - **类型**：ASGI HTTP 服务器

   - 特点：
     - 支持 ASGI 标准
     - 与 Uvicorn 类似，但有一些额外的功能和配置选项

   - **适用场景**：适合运行异步应用，特别是那些需要更多配置选项的应用。





> 
>
> 以上为通义返回结果



### Uvicorn和Fastapi的关系

- Uvicorn是一个ASGI服务器,专注于异步应用的高性能部署。它支持 ASGI 协议。
- Fastapi是一个web框架,它本身是基于ASGI标准实现的。这意味着Fastapi应用支持ASGI接口。
- 由于两者都支持ASGI标准,所以Uvicorn能够直接运行Fastapi应用。
- 通常情况下,使用Fastapi开发web api应用,然后使用Uvicorn来部署和运行这些Fastapi应用。



**为什么flask可以单独构建web应用程序，fastAPi需要和uvicorn结合使用？**

- fastAPI为纯web应用程序框架，其需要结合uvicorn ASGI服务器一起使用构建Web应用程序。
- flask本身包含了一个简单的内置开发服务器，这使得开发者可以直接运行Flask应用进行测试和开发，而不需要额外的服务器软件。Flask的内置服务器并不适合生产环境，因为它缺乏处理高并发、安全性和性能优化的能力。因此，在生产环境中部署Flask应用时，通常会与一个WSGI服务器（如Gunicorn或uWSGI）结合使用。



## **总结**

- WSGI和ASGI是两种标准接口，WSGI主要处理同步请求，适合传统的HTTP请求响应模式。ASGI是WSGI的一个扩展，旨在支持异步编程模型，如WebSocket、HTTP2等需要长时间连接的协议。
- Python Web应用程序开发框架有:
  - **Flask**： 轻量的Web框架，基于WSGI协议构建。
  - **FastAPI**：高性能Web框架支持异步编程。
  - **Django**：全能的Web框架，基于WSGI，也可配置支持ASGI。
- Web服务器和网关
  - **Uvicorn**：是一个ASGI服务器，专门用来运行异步Python web应用程序。它可以高效地运行FastAPI和其他ASGI兼容的应用程序。
  - **uWSGI**：是一种WSGI服务器，能够部署各种WSGI应用。也支持其他协议，包括HTTP和WebSocket。
- 使用选择
  - 简单HTTP服务可使用，两种简单的WSGI服务器， 如flask和Gunicorn
  - 对于需要高并发处理的服务，比如使用了WebSocket的应用， 使用fastAPI+uvicorn的组合模式
  - 对于复杂的web项目，使用Django更好，其内置了许多功能比如后台管理，认证系统等。
- flask和django都包含了一个简单的内置开发服务器。fastAPI需要搭配服务器使用如uvicorn才能运行。生产环境建议使用专门的Web服务器。
- Django有内置服务器，使得其开发阶段很方便，但是为保证生产环境更高的性能、稳定性和安全性，可选择更专业的网络服务器。比如方案 Django+Uvicorn+Nginx， Django+Uwsgi+Nginx，Django+Gunicorn+Nginx等



[讲WSGI](https://www.cnblogs.com/wongbingming/p/11002978.html)

https://blog.csdn.net/jsjsjs1789/article/details/136458203

[一文读懂WSGI和ASGI](https://blog.csdn.net/p515659704/article/details/110411508)

https://blog.csdn.net/jsjsjs1789/article/details/136458203

