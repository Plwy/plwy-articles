

## **启动x-anylabeling**

```bash
conda activate xlabel
cd X-AnyLabeling
python anylabeling/app.py
```



## Yolo格式标签文件导入和导出

**导入**

在x-anylabeling中打开 labelImg  yolo格式标注好的.txt标签文件。

1.先打开图像文件夹，在anylabel中打开图像文件

2.点击`导入`-> `导入yolo水平框标签`

3.选择具体的标签文件， 即为 `classes.txt` 文件

4.然后 下一步打开目录， 这里的目录指存储所有.txt标签文件的目录，比如`labels`。提示是否覆盖，选择是。

5.然后可以看到.txt标签已经被导入，界面出现标注框，此外，`image`同级目录下出现`.json`文件,为xlabel格式的标注文件，其将yolo格式标注转为了xlabel json格式。

**导出**

1.选择`导出`->`导出yolo水平框标签`

2.选择具体的标签文件， 即为 `classes.txt` 文件

3.设置导出选项， 导出label的路径，是否跳过空标签文件等。点击确认会在指定label路径下生成yolo格式标签文件。



## **使用自定义模型辅助标注**

到目录`X-AnyLabeling/anylabeling/configs/auto_labeling/`下，创建`my_detect.yaml`文件,举个例子

```yaml
type: yolov8
name: yolov8m-fall-detect
display_name: YOLOv8m car-detect
model_path: /home/user/model/car_detect.onnx
nms_threshold: 0.45
confidence_threshold: 0.45
classes:
  - car
```

然后界面上点击`AI` ，点击选择自定义模型，选择这个yaml文件，然后就可以导入yaml中配置的这个onnx模型。然后点击运行，可以一张张运行，也可以一次运行全部。



## **快捷键**

目标检测最常用的：

上一张下一张图片`A, D`

新建矩形框`R`

删除框，选中后`Del`

可在` anylabeling/configs/xanylabeling_config.yaml`文件下看到其他快捷键的配置。



## **issues**

1.

连按下一张，一直跳转图像画面，只能等待无法退出，最后程序卡死强制退出。再通过命令`python anylabeling/app.py `进入时出现报错:

>... 
>
> File "/home/sun/softwares/X-AnyLabeling/anylabeling/config.py", line 14, in update_dict
>    for key, value in new_dict.items():
>AttributeError: 'NoneType' object has no attribute 'items'

通过删除`~/.xanylabelingrc`文件可成功启动：

```
# 删除前查看发现,程序异常导致该文件为空
rm  ~/.xanylabelingrc 
```

