RESTful API 设计是一种基于 **REST（Representational State Transfer，表述性状态转移）** 架构风格来构建 Web API 的方法。它的核心思想是把服务器上的资源（如用户、订单、文章等）通过 **统一资源标识符（URI）** 暴露出来，并使用标准的 HTTP 方法（GET、POST、PUT、DELETE 等）对这些资源进行操作，从而让客户端与服务器之间进行清晰、简洁、可扩展的数据交互。

------

## 一、REST 的核心概念

1. **资源（Resource）** 一切皆是资源，比如：用户、商品、评论、文件等。 每个资源都有一个唯一的 URI（统一资源标识符），例如： `/users/123 /articles/456/comments`
2. **表述（Representation）** 资源可以有多种表现形式，比如 JSON、XML、HTML。 RESTful API 通常使用 JSON 作为数据格式。
3. **状态转移（State Transfer）** 客户端通过发送请求改变服务器资源的状态。 每次请求都包含足够的信息让服务器完成操作，并且不依赖会话状态（无状态）。
4. **统一接口（Uniform Interface）** 使用标准的 HTTP 方法和状态码。 资源通过 URI 标识，操作通过 HTTP 方法定义。

------

## 二、RESTful API 的设计原则

| 原则               | 说明                                                         |
| ------------------ | ------------------------------------------------------------ |
| **资源导向**       | API 围绕资源设计，而不是围绕操作设计。例如 `/orders`表示订单集合，`/orders/1001`表示某个订单。 |
| **使用 HTTP 方法** | 用标准方法表达意图： GET（获取）、POST（创建）、PUT（全量更新）、PATCH（部分更新）、DELETE（删除） |
| **无状态**         | 每个请求必须包含所有必要信息，服务器不保存客户端会话。       |
| **可缓存**         | 响应应明确是否可缓存，提高性能。                             |
| **分层系统**       | 客户端不知道是直接连到服务器还是中间有代理、网关。           |
| **统一接口**       | 使用一致的 URI 命名、数据格式、错误处理方式。                |

------

## 三、常见设计实践

### 1. URI 设计

- 使用名词，不用动词： ✅ `/users` ❌ `/getUser`
- 使用复数形式表示资源集合： `/products`而不是 `/product`
- 用路径表示层级关系： `/users/123/orders`表示用户 123 的所有订单

### 2. HTTP 方法使用

| 方法   | 作用         | 示例                                 |
| ------ | ------------ | ------------------------------------ |
| GET    | 获取资源     | `GET /users/123`                     |
| POST   | 创建新资源   | `POST /users`（请求体含用户信息）    |
| PUT    | 全量更新资源 | `PUT /users/123`（提供完整用户对象） |
| PATCH  | 部分更新     | `PATCH /users/123`（只传要改的字段） |
| DELETE | 删除资源     | `DELETE /users/123`                  |

### 3. 状态码使用

| 状态码                    | 含义           | 使用场景             |
| ------------------------- | -------------- | -------------------- |
| 200 OK                    | 成功           | GET/PUT/PATCH 成功   |
| 201 Created               | 资源创建成功   | POST 成功            |
| 204 No Content            | 成功但无返回体 | DELETE 成功          |
| 400 Bad Request           | 请求错误       | 参数缺失或格式错误   |
| 401 Unauthorized          | 未认证         | 缺少或无效 token     |
| 403 Forbidden             | 权限不足       | 用户无权访问         |
| 404 Not Found             | 资源不存在     | URI 错误或资源已删除 |
| 500 Internal Server Error | 服务器错误     | 后端异常             |

### 4. 版本控制

- 在 URI 或请求头中加入版本号： URI：`/api/v1/users` Header：`Accept: application/vnd.myapp.v1+json`

### 5. 过滤、排序、分页

- 查询参数实现： 过滤：`/users?role=admin` 排序：`/users?sort=created_at&order=desc` 分页：`/users?page=2&limit=20`

------

## 四、示例：用户管理 API

| 功能         | 请求                                                         | 说明         |
| ------------ | ------------------------------------------------------------ | ------------ |
| 获取所有用户 | `GET /api/v1/users`                                          | 返回用户列表 |
| 获取单个用户 | `GET /api/v1/users/123`                                      | 返回用户详情 |
| 创建用户     | `POST /api/v1/users` { "name": "Alice", "email": "alice@example.com" } | 新建用户     |
| 更新用户     | `PUT /api/v1/users/123` { "name": "Alice", "email": "new@email.com" } | 全量更新     |
| 部分更新     | `PATCH /api/v1/users/123` { "email": "new@email.com" }       | 只改邮箱     |
| 删除用户     | `DELETE /api/v1/users/123`                                   | 删除该用户   |

------

## 五、优点

- 简单、易理解、易调试
- 与 HTTP 协议天然契合
- 可扩展性强，适合前后端分离架构
- 被大多数现代 Web 框架（如 Express、Django REST framework、Spring Boot）广泛支持

------

## 六、总结

**RESTful API 设计 = 以资源为中心 + 用 HTTP 方法操作 + 标准化 URI 和响应**

它不是一种强制标准，而是一种被广泛接受的最佳实践。好的 RESTful API 应该：

- 清晰
- 一致
- 可预测
- 易于维护

需要我为你整理一份「RESTful API 设计规范清单」方便实际开发时参考吗？这样你可以直接对照检查自己的 API 是否符合标准。