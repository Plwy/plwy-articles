一个简单的flask服务过程的理解

## 例子

一个flask 服务的server和client的例子

server.py

```python
# run: python server.py
import cv2
from flask import Flask, request
from utils import base64_to_img

app = Flask(__name__)
model = model('./rec_model.pt')

@app.route('/RecMethod', methods=['POST', 'GET'])
def detect():
    input_data = eval(request.get_data())   # 得到输入的图像
    rqid = input_data['requestId']
    img_str = input_data['image']
    img_id = input_data['image_id']
    img = base64_to_img(img_str)        # 转base64格式为image

    # 输入模型
    result = model(img, device=device, conf=conf)[0]

    # 接口返回分析数据
    res = {
        'requestId': rqid,
        'image_id': img_id,
        'result': result,
    }
    return res

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=6511)
```

client.py

```python
import requests
import cv2
from utils import base64_to_img

# 设置请求的服务地址
TEST_URL = 'http://127.0.0.1:6511/RecMethod'

def test(img_path):
    img = cv2.imread(img_path)
    data = str({'requestId': '1', 
                'image_id': '22', 
                'image': image_to_base64(img)})
    r = requests.post(url=TEST_URL, data=data, verify=True)
    pred = json.loads(r.content.decode('utf-8'))
    print(pred)

if __name__ == "__main__":
 	test()
```



**Q&A：**

1.`app = Flask(__name__)` 

创建一个Flask的实例,它接收的参数为`__name__`是python的内置变量，表示当前模块或者包的名字。可以用于确定应用程序的根路径和静态文件的位置。

2.`@app.route('/RecMethod', methods=['POST', 'GET'])`

客户端发送url给web服务器，web服务器将url转发给flask程序实例，程序实例需要知道对于每一个url请求启动那一部分代码，所以保存了一个url和python函数的映射关系。处理url和函数之间关系的程序，称为路由在flask中，定义路由最简便的方式，是使用程序实例的app.route装饰器，把装饰的函数注册为路由。

这句话使用app.route装饰器来处理url和函数之间关系，它会将URL和执行的视图函数的关系保存到app.url_map属性上。这里的视图函数就是detect()

`app.route()`是Flask框架中用于定义路由的装饰器函数，它接受一些参数来指定路由的URL规则、请求方法等。

`app.route()`参数如下：

- `rule`（必选）：定义URL规则的字符串，表示要匹配的URL路径。可以包含动态部分，使用尖括号(`< >`)来指定动态部分的名称和类型。例如：`/user/<username>`。
- `view_func`（必选）：用于指定将要执行的**视图函数**，即处理请求的函数。它接受一个函数作为值。这个函数通常是一个Flask应用程序中定义的视图函数，用于处理路由匹配后的请求。

- `methods`（可选）：定义允许的HTTP请求方法。可以是一个字符串或一个包含多个字符串的列表。默认情况下，允许GET请求。例如：`methods=['GET', 'POST']`。
- `endpoint`（可选）：为路由定义一个唯一的端点名称，**用于反向生成URL，即： url_for(‘名称’)**。如果未指定，默认使用视图函数的名称。例如：`endpoint='index'`。
- `defaults`（可选）：为动态部分提供默认值，以便在没有提供相应值时使用。默认值是一个字典。例如：`defaults={'page': 1}`。

3.`app.run(debug=False, host='0.0.0.0', port=6511)`

该条命令启动服务。根据传入的host和port参数初始化一个Werkzeug的WSGI服务器，并通过指定的线程数或进程数来实现并发请求处理。

这里设置的host为'0.0.0.0'，0.0.0.0并不是一个真实的的IP地址，它表示本机中所有的IPV4地址。监听0.0.0.0的端口，就是监听本机中所有IP的端口。所以后面客户端请求使用的127.0.0.0.1这是一个回环地址，意味着数据包会被发送主机的IP层直接获取，所以这个例子就是本地电脑启动服务作为服务器端，并本地模拟客户端请求数据进行测试。

4.`r = requests.post(url=TEST_URL, data=data, verify=True)`

这句话为request库中的post请求函数，用于向服务器发送请求。

- url: 这个参数指定了请求的 URL 地址。在这个例子中，TEST_URL 是一个字符串变量，代表你要向其发送 POST 请求的服务器地
- data: 这个参数可以用来传递要发送的数据。它可以是一个字典 (dict)、列表 (list)、元组 (tuple) 或任何可迭代对象。这些数据会被编码成表单格式并附加到请求体中。这里的 data 变量应当包含了你想要发送的数据。
- verify: 这个布尔值参数控制是否验证 SSL/TLS 证书。如果设置为 True，则会验证服务器的 SSL/TLS 证书。如果设置为 False，则禁用 SSL/TLS 证书验证，这可能会导致安全风险。默认情况下，verify 的值为 True。

app是flask的实例，功能就是接受来自web服务器的请求，浏览器将请求给web服务器，web服务器将请求给app ,app收到请求，通过路由找到对应的视图函数，然后将请求处理，得到一个响应response，然后app将响应返回给web服务器，web服务器返回给浏览器，浏览器展示给用户观看，流程完毕。



ref:

[app = Flask(__name__)相关说明](https://blog.csdn.net/stay_foolish12/article/details/107860908)

[GET 和 POST 到底有什么区别？](https://www.zhihu.com/question/28586791)

