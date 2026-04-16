rk 4卡板环境安装



1.安装conda

拷贝`Miniconda3-py310_25.5.1-0-Linux-aarch64.sh`文件到`/root`目录下

```
chmod +x Miniconda3-py310_25.5.1-0-Linux-aarch64.sh
bash ./Miniconda3-py310_25.5.1-0-Linux-aarch64.sh
# 最后选择yes 生成~/.bashrc文件，里面有conda自启动的脚本。
```

2.修改系统环境变量

```
vi /etc/profile
```

添加以下内容

```bash
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/root/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/root/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/root/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/root/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

export PATH="/root/miniconda3/bin:$PATH"  # commented out by conda initialize
export HF_ENDPOINT=https://hf-mirror.com
```

启用

```
source /etc/profile
```

完成后就会开启终端自启动conda



3.修改conda源

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --show channels
conda config --set show_channel_urls yes
```

4.修改系统时间

```
date -s "2025-07-10 17:00:03"
```

5.创建conda环境

```
conda create --name llm_seg python=3.10 -y
```

6.修改pip源

```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

