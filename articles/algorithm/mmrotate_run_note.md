# mmrotate 使用记录                  

2024.10.08

### 环境安装

```bash
# 本地cuda11.7
conda create --name mmrotate python=3.9
conda activate mmrotate

pip install torch==2.0.1 torchvision==0.15.2
# 直接安装 # 这里花了很久很久
pip install -v -e .

# 安装用于管理openmmlab库和模型的openmim
pip install -U openmim
# 下载测试用文件
mim download mmrotate --config oriented_rcnn_r50_fpn_1x_dota_le90 --dest .


#重装numpy 转为1.
pip uninnstall numpy
pip install numpy==1.19.5
#
pip uninstall scipy
pip install scipy==1.9.0
#
pip uninstall Matplotlib
pip install matplotlib==3.5.0

# 最后可以运行了
python demo/image_demo.py demo/demo.jpg oriented_rcnn_r50_fpn_1x_dota_le90.py oriented_rcnn_r50_fpn_1x_dota_le90-6d2b2ce0.pth --out-file result.jpg

```

```bash
# 运行mim 命令
# 出错：your numpy version is 1.19.5.Please upgrade numpy to >= 1.22.4 to use this pandas version
# 重装pandas 安装较老的版本
pip uninstall pandas
pip install pandas==1.3.0

# 成功运行mim命令
mim list 
```
显示如下：
mmcv-full  1.7.2      https://github.com/open-mmlab/mmcv
mmdet      2.28.2     https://github.com/open-mmlab/mmdetection
mmrotate   0.3.4      /media/sun/disk2/workspace/obb_proj/code/mmrotate

参考文档docs/zh_cn/faq.md进行版本检查。

### 推理测试

运行脚本,测试环境是否安装好

#### 直接推理

调用的mmdet库

```bash
python demo/image_demo.py demo/dota_demo.jpg oriented_rcnn_r50_fpn_1x_dota_le90.py oriented_rcnn_r50_fpn_1x_dota_le90-6d2b2ce0.pth --out-file result_huge.jpg
```

#### 切大图推理

调用的mmrotate下的api中的切图推理

```bash
python demo/huge_image_demo.py \
    demo/dota_demo.jpg \
    oriented_rcnn_r50_fpn_1x_dota_le90.py \
    oriented_rcnn_r50_fpn_1x_dota_le90-6d2b2ce0.pth 

# 最好修改一下，加 --out-file 保存为指定文件，使用matplot显示后选择保存图像有问题。
python demo/huge_image_demo.py \
    /media/sun/disk2/workspace/obb_proj/正摄图片/1/DOM_GEO_JPG.jpg \
    oriented_rcnn_r50_fpn_1x_dota_le90.py \
    oriented_rcnn_r50_fpn_1x_dota_le90-6d2b2ce0.pth \
    --out-file /media/sun/disk2/workspace/obb_proj/正摄图片/1/DOM_GEO_JPG_result_patch1024.jpg
```

### DOTA数据集进行测试和训练

#### DOTA下载及切图处理

下DOTA数据集,解压tar包，修改下面json文件的读图和读标注的路径，进行切图处理。
```shell
# 需要下载这个包
pip install shapely

python tools/data/dota/split/img_split.py --base-json \
  tools/data/dota/split/split_configs/ss_trainval.json

python tools/data/dota/split/img_split.py --base-json \
  tools/data/dota/split/split_configs/ss_test.json
```

#### 测试及训练

运行这里需要根据配置找到数据集配置文件`configs/_base_/datasets/dotav1.py`，检查并修改数据路径。

```bash
python ./tools/test.py \
  configs/rotated_retinanet/rotated_retinanet_obb_r50_fpn_1x_dota_le90.py \
  checkpoints/rotated_retinanet_obb_r50_fpn_1x_dota_le90-c0097bc4.pth \
  --show-dir work_dirs/vis
```
运行完生成了可视化的结果。

训练
```bash
python tools/train.py oriented_rcnn_r50_fpn_1x_dota_le90.py \
    --work-dir work_dirs/oriented_rcnn_r50_fpn_1x_dota_le90     
```

## torchserve服务部署

参考docs/zh_cn/useful_tools.md

主要步骤

- 1.安装两个包：`torch-model-archiver`,`torch-model-archiver`
- 2.`torch-model-archiver`通过脚本或者命令行，将torch模型转为用于torchserve部署的`.mar`包
- 3.torchserve命令行启动模型服务
- 4.curl服务请求测试



1.安装torch-model-archiver 用于打包模型

```bash
pip install torch-model-archiver
```
2.转.mar包
运行
```bash
python tools/deployment/mmrotate2torchserve.py oriented_rcnn_r50_fpn_1x_dota_le90.py oriented_rcnn_r50_fpn_1x_dota_le90-6d2b2ce0.pth --output-folder zsl_server/oriented_rcnn_r50_fpn_1x_dota_le90 --model-name oriented_rcnn_r50_fpn_1x_dota_le90
```
报错
>AttributeError: 'Namespace' object has no attribute 'config_file'
尝试将版本降一降

```bash
# 卸载当前torch-model-archiver  0.12.0
pip uninstall torch-model-archiver 
# 安装更早的版本
pip install torch-model-archiver==0.6.0 
```
然后就运行成功了，在指定输出目录生成了xxx.mar的文件

也可不使用提供的脚本，使用`torch-model-archiver`命令行生成`.mar`包：

```bash
# 创建输出目录
mkdir output_dir
# 生成.mar文件到输出目录
torch-model-archiver  --model-name oriented_rcnn_r50_fpn_1x_dota_le90 --version 1.0 --model_file oriented_rcnn_r50_fpn_1x_dota_le90.py --serialized-file oriented_rcnn_r50_fpn_1x_dota_le90-6d2b2ce0.pth --handler tools/deployment/mmrotate_handler.py --export_path output_dir
```
运行成功后指定输出目录生成了`oriented_rcnn_r50_fpn_1x_dota_le90.mar`的文件

3.
上面的转出脚本，涉及到`handler`字段，其对应着一个自定义脚本`tools/deployment/mmrotate_handler.py`，该脚本中定义了一个`MMRotateHandler`的类，其继承自`ts.torch_handler.base_handler.BaseHandler` .包含了以下几个函数

- initalize

  调用了mmrotate的api 的模型加载接口，用来加载模型文件

- preprocess

  将输入请求转为list ndarray

- inference

  调用了mmrotate的api 的推理接口。

- postprocess

  对推理结果进行解析，及返回结果构造

4.

```bash
# 先安装torchserve
pip install torchserve

# 命令行启动服务
torchserve --start --model-store zsl_server/oriented_rcnn_r50_fpn_1x_dota_le90/ --models oriented_rcnn_r50_fpn_1x_dota_le90=oriented_rcnn_r50_fpn_1x_dota_le90.mar ----disable-token-auth
```
报错`ModuleNotFoundError: No module named 'nvgpu'`,安装一下`pip install nvgpu`
再运行，没得报错了，哦嚯嚯。
要加`--disable-token-auth`字段，否则curl请求会一直报错400
```
{
  "code": 400,
  "type": "InvalidKeyException",
  "message": "Token Authorization failed. Token either incorrect, expired, or not provided correctly"
}
```
5.
使用`curl`请求工具进行服务端口请求测试
```bash
curl http://localhost:8080/ping
```
返回`"status": "Healthy"`

再使用图像进行请求测试：
```bash
curl http://localhost:8080/predictions/oriented_rcnn_r50_fpn_1x_dota_le90 -T demo/dota_demo.jpg
```
返回一大串如下检测结果，说明服务启动成功。
```bash
...
  {
    "class_name": "large-vehicle",
    "bbox": [
      210.56906127929688,
      858.6914672851562,
      73.94198608398438,
      24.669469833374023,
      -0.9828579425811768
    ],
    "score": 0.5078285336494446
  }
```













