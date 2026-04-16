**(IEEE2020)DSNet: A Flexible Detect-to-Summarize Network for Video Summarization** 

# DSNet 运行记录

paper:https://liplus.me/publication/dsnet/dsnet.pdf

github:https://github.com/li-plus/DSNet

:commit 1804176e2e8b57846beb063667448982273fca89

## 环境安装

```bash
conda create --name dsnet python=3.9 -y
conda activate dsnet
# 本地cuda 11.7 cudnn 8.8.0  显驱535.183
#这里下载的1.13.1的torch
pip install opencv-python==4.5.2.54
pip install numpy==1.19.5
pip install torch==1.13.1 torchvision==0.14.1
pip install h5py
pip install pyyaml
```

## 运行

- 运行并debug infer.py 梳理推理流程

```bash
 python infer.py anchor-based --ckpt-path ./models/pretrain_ab_basic/checkpoint/tvsum.yml.4.pt --source ../custom_data/videos/iVt07TCkFM0.mp4 --save-path ./iV_output.mp4
```

 每隔 sample_rate 取一帧
对每帧进行特征提取 (特征提取网络是一个googlenet网络)
img (3,224,224)
batch (1,3,224,224)
feat [1, 1024, 1, 1] --> (1024)
features  len =167 --> (167,1024)

总帧数 2500， 每隔15帧，共提取处理帧数167。


将返回的feature(167, 1024),转为[1, 167, 1024]后输入dsnet网络

得到pred_loc(167,4,2) -> (668,2) 
pred_cls(167,4) --> (668,)
经过nms  得到pred_loc,pred_cls->(196,2),(196)
然后经过bbox2summary 得到整个视频序列中所有需要被抽出的视频帧pred_summ
这里得到最终的summary，传入了 dsnet的预测类别，box 以及特征改变片段，片段长度，总序列长度，子采样视频序列，需要采样的视频长度比例。
pred_summ = vsumm_helper.bbox2summary(
            seq_len, pred_cls, pred_bboxes, cps, n_frames, nfps, picks)

总的来说就是：

1. 提特征。先隔多少帧一抽，对抽出的帧提特征。
2. 分镜头。对这些特征进行计算，得到变化镜头的帧片段。
3. 得到帧重要度位置偏移等信息。将特征输入dsnet，得到预测的重要度和中心得分和偏移长度，
4. 细化分镜头得到摘要。再将预测结果和之前的帧特征改变的片段（镜头片段）传入一个函数，得到最终提取的结果片段。

- 运行验证脚本

```bash
# evaluate anchor-based model
python evaluate.py anchor-based --model-dir ../models/pretrain_ab_basic/ --splits ../splits/tvsum.yml ../splits/summe.yml
# evaluate anchor-free model
python evaluate.py anchor-free --model-dir ../models/pretrain_af_basic/ --splits ../splits/tvsum.yml ../splits/summe.yml --nms-thresh 0.4
```
可跑出readme里面的结果。ohohoho。
给出了F1指标和多样性指标。比较抽取的帧和数据集里的人工抽取帧的F1值。

- 训练

脚本没跑。看了下代码看了部分paper理解一下。

训练主要针对的DSNet网络的训练，其loss有 帧类别预测loss_cls, 帧候选提议位置偏移loss_loc。该网络主要预测即每个时间位置的重要性得分、中心得分和片段边界（长度偏移量）。推理阶段会利用预测位置对片段进行细化，并进一步进行非极大值抑制过滤。

Anchor-Based Video Summarization
- 特征提取
  首先使用不带最后三层的 GoogLeNet [52] 来提取特征向量 v_j,采用自注意力机制提取长距离表示w_j,最终的表征为x_j = v_j+w_j

- 时间兴趣建议
  解决同一片段内的重要性得分不等导致片段选择不完整，提出区域建议网络和动作定位方法。
  提取的时间序列片段与gt的摘要片段进行tIoU计算，超过阈值认为是正样本片段。

- 提议分类和回归
  使用一个网络，特征输入后，经过两个分支，得到提议的重要度分数得到分类，和一个关联中心和片段偏移长度，得到位置回归。
  第i帧的gt重要度分数为pi，位置偏移为ti，那么预测的结果，偏移量使用SmoothL1计算损失，重要度分数使用交叉熵计算损失。 对于第i帧的gt 的位置偏移如何得到？ 
  gt 片段和 预测的片段都输入 这个分类和回归网络得到中心位置和长度偏移的值，然后计算最终的gt 位置偏移。所以不需要人工标注，只要都输入该网络即可。

- 最终的key shot 选择
  帧级别的重要度：每帧的重要度打分。
  shot级重要度：片段的重要度打分，片段长度不能超过总视频长的0.15

  对于片段的置信度较低且彼此重叠度较高的使用NMS进行筛选，去除冗余和低质量的片段。

  - 首先使用KTS 核时间分割（一种镜头检测方法）将视频序列分割成多个视频镜头。
  - 然后使用训练的模型来预测帧的重要性分数。得到帧级重要性得分，经过平均计算镜头片段级的重要性得分，来得到最终的摘要片段。
