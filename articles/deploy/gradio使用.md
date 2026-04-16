## 基础设置

一个展示demo包含，音视频文本输入，和按钮。

```python
import gradio as gr
 
top_md="""
## 介绍
- 哈哈哈
"""
def start_click(text_input):
    data = "*"*5+text_input+"*"*5
    return data

with gr.Blocks(theme=gr.themes.Default) as service:
    gr.Markdown(top_md)
    with gr.Row():
        with gr.Column():
            with gr.Row():
                video_input = gr.Video(label="视频输入 | Video Input")
                audio_input = gr.Audio(label="音频输入 | Audio Input")
            with gr.Column():
                gr.Examples([
                            'https://isv-data.oss-cn-hangzhou.aliyuncs.com/ics/MaaS/ClipVideo/%E4%B8%BA%E4%BB%80%E4%B9%88%E8%A6%81%E5%A4%9A%E8%AF%BB%E4%B9%A6%EF%BC%9F%E8%BF%99%E6%98%AF%E6%88%91%E5%90%AC%E8%BF%87%E6%9C%80%E5%A5%BD%E7%9A%84%E7%AD%94%E6%A1%88-%E7%89%87%E6%AE%B5.mp4'
                            ],
                            [video_input],
                            label='示例视频 | Demo Video')
                gr.Examples(['https://isv-data.oss-cn-hangzhou.aliyuncs.com/ics/MaaS/ClipVideo/%E9%B2%81%E8%82%83%E9%87%87%E8%AE%BF%E7%89%87%E6%AE%B51.wav'],
                            [audio_input],
                            label='示例音频 | Demo Audio')
                # with gr.Column():
                #     text_input = gr.Textbox(label="文本输入")
        with gr.Column():
            with gr.Row():
                text_input = gr.Textbox(label="文本输入")
            with gr.Row():
                start_button = gr.Button("Start", variant="primary")
    start_button.click(fn=start_click,
                       inputs=[text_input],
                       outputs=[text_input])
    # service.launch(share=True, server_port=7860, server_name='0.0.0.0', inbrowser=False)
    service.launch(share=True, server_port=7860, server_name='127.0.0.1', inbrowser=False)
```



## 流式输出

在聊天文本框中流式输出对话内容。

非流式返回结果：

```python
import gradio as gr
import random
import time
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()      # 对话框
    msg = gr.Textbox()      # 输入文本框
    clear = gr.ClearButton([msg, chatbot]) # 清除按钮
    def bot(message, history):
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        history.append((message, bot_message))
        time.sleep(1)
        return "", history
    
    msg.submit(bot, [msg, chatbot], [msg, chatbot])
demo.launch()
```

流式返回结果：

```python
import gradio as gr
import random
import time

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    # user_message: 用户输入的消息。
    # history：聊天记录（一个二维列表，每条记录是 `[用户消息, 机器人回复]`）。
    def user(user_message, history):
        return "", history + [[user_message, None]]


    def bot(history):
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            time.sleep(1/20)
            yield history

    # 链式调用，在submit的回调函数执行完成后，执行bot函数
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch()
```

 `.submit` 和 `.then` 配合实现了以下流程：

1. 用户在文本框中输入消息并按下回车。
2. user函数被调用：
   - 清空文本框。
   - 将用户消息添加到聊天记录中。
3. bot函数被调用：
   - 随机生成机器人回复。
   - 模拟打字效果逐字更新聊天记录。
4. 最终，聊天记录在界面上实时更新，显示用户消息和机器人回复。



**demo.queue()**

- 启用 **Gradio 的队列机制**。
- Gradio 的队列允许多个用户同时访问应用时，处理请求的顺序被排队执行。
- 如果不启用队列，多个用户的请求可能会同时触发回调函数，导致冲突或不一致的行为。
- 是否必要
  - 如果你的应用是单用户使用（例如本地测试），这行代码不是必须的。
  - 如果你的应用需要支持多用户并发访问，建议保留这行代码以确保请求按顺序处理。

ref:

https://blog.csdn.net/qq_51116518/article/details/138087005







## gr.state()

**gr.State** 是 Gradio 提供的一个特殊组件，用于存储和管理应用的状态变量，目的是在后台存储一些变量方便访问和交互。

- 特点：
  - 它是一个不可见的组件，用户界面中不会直接显示。
  - 用于在回调函数之间传递和共享数据。
  - 状态变量的值会在每次回调函数执行时更新。

```python
import gradio as gr
 
demo = gr.Blocks(css="""#btn {color: red} .abc {font-family: "Comic Sans MS", "Comic Sans", cursive !important}""")
 
with demo:
    default_json = {"a": "a"}
 	# 设置状态变量num，初始值为0
    num = gr.State(value=0)
    # 用于显示当前数字的平方,初始值为0
    squared = gr.Number(value=0)
    # 
    btn = gr.Button("Next Square", elem_id="btn", elem_classes=["abc", "def"])
 	# 设置状态变量stats，初始值为0
    stats = gr.State(value=default_json)
    #
    table = gr.JSON()
 
    def increase(var, stats_history):
        var += 1
        stats_history[str(var)] = var**2
        return var, var**2, stats_history, stats_history
 
    btn.click(increase, [num, stats], [num, squared, stats, table])
 
if __name__ == "__main__":
    demo.launch()
```

该代码实现这样的功能：

1. 用户点击按钮后，数字递增并计算其平方。
2. 更新状态并将结果显示在界面上。

gr.state()在当前代码中的作用,两个状态变量。

1. num:
   - 存储当前的数字。
   - 每次点击按钮时，increase函数会更新它的值。
2. stats:
   - 存储一个 JSON 对象，用于记录每个数字及其平方。
   - 每次点击按钮时，increase函数会更新这个 JSON 对象。

**json格式的数据展示**:`gr.JSON()`

