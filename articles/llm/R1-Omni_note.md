## R1-Omni use note

code:https://github.com/HumanMLLM/R1-Omni

1.下载四个模型：

- [R1-Omni](https://modelscope.cn/models/iic/R1-Omni-0.5B)
-  [siglip-224](https://huggingface.co/google/siglip-base-patch16-224)
- [whisper-large-v3](https://huggingface.co/openai/whisper-large-v3)

- [bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased)



2.按照readme中修改，R1-Omni下config.yaml文件的两个模型路径，以及inference.py中的模型路径即可。

3.运行脚本：

```bash
python inference.py --modal video_audio \
  --model_path ./R1-Omni-0.5B \
  --video_path video.mp4 \
  --instruct "As an emotional recognition expert; throughout the video, which emotion conveyed by the characters is the most obvious to you?  Output the thinking process in <think> </think> and final emotion in <answer> </answer> tags."
```

中间缺一些包，pip安装即可。

4.完成后可顺利运行。运行时有很多多余输出，可以不管。
