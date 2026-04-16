**real-esrgan运行环境问题：**

1. basicsr库安装

装basicsr得用aliyun镜像！！使用清华源会出现报错，提示依赖 tb-nightly，但是pip找不到这个包。

```
pip install basicsr==1.4.2 -i https://mirrors.aliyun.com/pypi/simple
```

2. 运行会报错`ModuleNotFoundError: No module named 'torchvision.transforms.functional_tensor' `。

将basicsr下的文件`~/miniconda3/envs/sr/lib/python3.10/site-packages/basicsr/data/degradations.py`进行修改

`from torchvision.transforms.functional_tensor import rgb_to_grayscale`

替换为`from torchvision.transforms.functional import rgb_to_grayscale`



