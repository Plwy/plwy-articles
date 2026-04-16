(**CVPR2024)CSTA: CNN-based Spatiotemporal Attention for Video Summarization**

# CSTA 运行记录

[paper](https://openaccess.thecvf.com/content/CVPR2024/papers/Son_CSTA_CNN-based_Spatiotemporal_Attention_for_Video_Summarization_CVPR_2024_paper.pdf)
[code](https://github.com/thswodnjs3/CSTA) :commit 11c7bc5fe19a365e5c41b86345944e7f1844c751

通过空间注意力和时间注意力来使得网络能够准确预测帧的重要度得分。

## QuickRun
```bash
conda create --name CSTA python=3.9 -y
conda activate CSTA
pip install torch==2.2.1 torchvision==0.17.1
pip install h5py
pip install numpy==1.19.5
pip install scipy==1.9.0
```
按照readme下，下载数据以及预训练模型，整理成对应的目录结构。（split.tar 都解压成.pt）
然后运行

```bash
python inference.py
```
出现了一个错误
>     ...
>
>     scores = output.squeeze().clone().detach().cpu().numpy().tolist()
>     RuntimeError: CUDA error: an illegal memory access was encountered
>     CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
>     For debugging consider passing CUDA_LAUNCH_BLOCKING=1.
>     Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.

在 inference.py 代码 开头处加上

```python
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
```
再运行，没得问题了。成功输出以下一堆信息：
```
PARAMS: 8.35M
...  # 此处省略
[FINAL - SumMe]Kendall:0.247, Spear:0.276
...  # 此处省略
[FINAL - TVSum]Kendall:0.194, Spear:0.254
```
eccv16_dataset_summe_google_pool5.h5文件里加载出来，是video及对应的feature和gtscore， 以及change_points, n_frames, picks, user_summary

这里的指标结果评价调用的scipy库中的函数，计算的Kendall(肯德尔)相关系数和 Spearman(斯皮尔曼)相关系数，这两个是反映等级相关程度的统计分析指标，都可以用于评估视频摘要质量和用户评分之间的一致性，判断视频摘要是否能够准确反映用户认为重要的内容。


## 测试生成视频摘要
再下两个包

```bash
 pip install opencv-python 
 pip install tqdm
```
1. 输入一个长视频文件，生成该视频的视频摘要。
```bash
python generate_video.py --input_is_file true \
    --file_path ./St_Maarten_Landing.mp4 \
    --ext mp4 \
    --save_path ./output/ \
    --weight_path ./weights/TVSum/split5.pt
```
运行结束在output下生成了视频摘要文件。结果特别不错。
2. 输入包含几个视频的文件夹，生成多个视频的视频摘要
```bash
python generate_video.py --input_is_file False \
    --dir_path ./test_videos \
    --ext mp4 \
    --save_path ./output/ \
    --weight_path ./weights/TVSum/split5.pt
```
运行结束在output下生成了多个视频摘要文件。       

推理流程梳理：

1.config = get_config() # 配置
2.video_proc = VideoPreprocessor()
配置特征提取器和采样帧数。
3.model = set_model()
配置CSTA网络模型
4.n_frames, features, cps, pick = video_proc.run()
每隔n帧进行特征提取。通过特征使用kts得到镜头片段。
5.output = model(features)
特征输入模型，得到预测结果。（应该是每一帧的重要度得分）
6.selections = generate_summary(n_frames, output, cps, pick)
得到摘要视频帧，使用了Knapsack算法，传入的是shot片段得分。
7.frames = pick_frames() ；produce_video()
从视频中得到选取的所有帧，并生成为视频。

## 训练

模型输入为数据集提供的feature，模型输出结果直接和数据集提供的gtscore计算loss 采用的MSEloss.
```bash
python train.py
```
报错：
> RuntimeError: cuDNN version incompatibility: PyTorch was compiled  against (8, 9, 2) but found runtime version (8, 8, 0). PyTorch already comes bundled with cuDNN. One option to resolving this error is to ensure PyTorch can find the bundled cuDNN. Looks like your LD_LIBRARY_PATH contains incompatible version of cudnn. Please either remove it from the path or install cudnn (8, 9, 2)

cuDNN 版本不兼容：PyTorch 是针对 (8, 9, 2) 编译的，但发现运行时版本 (8, 8, 0)。PyTorch 已与 cuDNN 捆绑在一起。解决此错误的一个选项是确保 PyTorch 可以找到捆绑的 cuDNN。
这个是因为安装的pytorch时安装了torch版本对应的cudnn，与本地的cudnn版本不一致，默认读取了本地的cudnn，导致torch和cudnn不兼容。可以修改LD_LIBRARY_PATH为编译时的cudnn版本路径，移除LD_LIBRARY_PATH中的本地版本cudnn路径，或者安装8.9.2的版本。

不想重装本地cudnn，最终解决办法，重装了torch 和torchvision。
```bash
# 本地 cuda 11.7 cudnn 8.8.0
# 降了下torch版本
pip uninstall torch torchvision 
pip install torch==2.0.1 torchvision==0.15.2 
```
然后顺利运行。
