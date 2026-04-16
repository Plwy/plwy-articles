## 使用

Ultralytics YOLO 官方文档[这里](https://docs.ultralytics.com/tasks/detect/#models) 包含了多种任务的包括python和CLI的使用。

### 训练

[train-setting](https://docs.ultralytics.com/modes/train/#train-settings)

**python**

简单的使用：

```python
from ultralytics import YOLO
model = YOLO('yolov8m.pt')  # 使用预训练模型
model.train(data='v8_train.yaml', epochs=100, imgsz=640, batch=16, device=[0,1], workers=4)
```

也可以在yaml中定义模型结构，以及设置一些训练参数：

```python
from ultralytics import YOLO

pre_model_path = 'weights/best.pt'
model = YOLO(pre_model_path)
model.train(task='detect',model='yolov8-gam.yaml',data='data.yaml', device=[0,1,2,3,4,5],batch=18, workers=24, cache=True ,epochs=500, patience=100, optimizer='AdamW', lr0=0.001)
```

**CLI**

```bash
yolo task=detect mode=train model=yolov8m.pt data=fall_v1.yaml name=yolov8m_v1 batch=32 epochs=500 imgsz=640 device=0,1 patience=100 optimizer=AdamW lr0=0.001
```



**训练数据设置**

data.yaml的例子

- 训练多分类时

1.以下这种方法需要将待训练的图像事先分为train, val,test三个文件夹.

```yaml
path: /root/datasets/YOLO_car 
# 使用文件路径
train: train/images  
val: val/images  
test: test/images  
# Classes
nc: 3
names:
  0: car
  1: van
  2: bus
```

2.以下这种方法可以将所有图像都放在一个文件夹，训练时生成对应的`.txt`路径即可。

```yaml
path: /root/datasets/YOLO_car 
train: train.txt 
val: val.txt 
test: test.txt 
# Classes
nc: 3
names:
  0: car
  1: van
  2: bus
```

.txt下写入文件基于path的相对路径即可。



- 训练车牌时，预训练模型为yolo-pose

```yaml
train: /car_plate/train_data 
val: /car_plate/val_detect
test: 

# Keypoints
kpt_shape: [4, 2]  # number of keypoints, number of dims (2 for x,y or 3 for x,y,visible)
flip_idx:  [1, 0, 3, 2] 

# Classes
names:
  0: single
  1: double
```



### 推理

可参考这里[here](https://docs.ultralytics.com/modes/predict/#inference-arguments)包含使用`predict`推理时的相关参数。

预测结果并保存：

**python**

1.

```python
from ultralytics import YOLO

images_path = "test_datas"
model = YOLO("models/best.pt")
model.predict(source=images_path, conf=0.45, iou=0.5, imgsz=640, save=True)
```

这里默认保存在`runs/detect/predict`目录下，无法指定输出目录。

source可以是图像路径、视频文件、目录、URL或用于实时馈送的设备ID。

2.

使用内置plot()方法提取结果并保存。

```python
from ultralytics import YOLO
from PIL import Image

images_path = "test_datas"
model = YOLO("models/best.pt")

results = model.predict(source=images_path,conf=0.45, iou=0.5, imgsz=640)
for i, result in enumerate(results):
    im_bgr = result.plot()
    im_rgb = Image.fromarray(im_bgr[..., ::-1])
    # im_rgb.show()
    result.save(filename=f"results_{i}.jpg")
```

**CLI**

```bash
yolo predict model=weights/best.pt \
    source=mytest/ imgsz=640 \
    name=pred_mytest device=[0,1] conf=0.5 iou=0.5
```

这里会自动生成绘制的结果并保存在目录`runs/detect/pred_mytest`下

### 导出

**python**

```python
from ultralytics import YOLO

model = YOLO('weights/best.pt')
onnx_model = model.export(format="onnx", imgsz=640, opset=12)
```

**CLI**

```bash
yolo mode=export model=weights/best.pt format=onnx imgsz=640 opset=17 device=0
```



## 训练输出结果分析 

- .args.yaml： 记录训练时的配置参数

- P_curve：准确率和置信度之间的关系

- R_curve：召回率和置信度之间的关系

- F1_curve: F1值和置信度之间的关系

- PR_curve： 召回率和准确率之间的关系

- confusion_matrix: 混淆矩阵

- confusion_matrix_normalized： 归一化后的混淆矩阵

- results.csv: 每个epoch的指标和损失以及学习率的记录

- results.png:训练时的在训练集和验证集上的损失变换情况

- val_batch0_pred： 验证集上第0个batch预测的结果可视化

- val_batch0_label： 验证集上第0个batch实际标注的结果可视化

- events.out.tfevents.xxx: 训练日志可用`tensorboard --logdir="."`查看

- labels：对标签数据的统计及可视化

  |                                            |                                          |
  | ------------------------------------------ | ---------------------------------------- |
  | 第一个图是训练集的数据量，每个类别有多少个 | 第二个图是框的尺寸和数量                 |
  | 第三个图是中心点相对于整幅图的位置         | 第四个图是图中目标相对于整幅图的高宽比例 |

- label_correlogram:

  汇总了训练集中的标签数据，体现了标签中心点横纵坐标以及框的高宽间的关系