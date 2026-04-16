本地电脑存在多个python版本。需要python3.10以上版本。对python进行更新。

```
➜  ~ python2 --version
Python 2.7.18
➜  ~ python3 --version
Python 3.8.10
➜  ~ python --version 
Python 3.9.12
```

安装方式：

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
```



安装时issue：

**执行sudo add-apt-repository ppa:deadsnakes/ppa时出现**

> E: 仓库 “file:/var/cudnn-local-repo-ubuntu2004-8.4.0.27  Release” 不再含有 Release 文件。 N: 无法安全地用该源进行更新，所以默认禁用该源。 N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。 E: 仓库 “file:/var/nv-tensorrt-local-repo-ubuntu2004-10.7.0-cuda-11.8  Release” 不再含有 Release 文件。 N: 无法安全地用该源进行更新，所以默认禁用该源。 N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。 E: 仓库 “file:/var/nv-tensorrt-local-repo-ubuntu2004-8.6.0-cuda-11.8  Release” 不再含有 Release 文件。 N: 无法安全地用该源进行更新，所以默认禁用该源。 N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。 E: 仓库 “https://download.docker.com/linux/ubuntu focal Release” 不再含有 Release 文件。 N: 无法安全地用该源进行更新，所以默认禁用该源。 N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。

1. 更新软件源列表

   首先，尝试更新你的软件源列表，以确保所有仓库都是最新的：

   ```
   sudo apt-get update
   ```

   如果仍然收到相同的错误，请继续以下步骤。

2. 检查并修复 `/etc/apt/sources.list` 和 `/etc/apt/sources.list.d/` 目录下的文件
   - **打开 `/etc/apt/sources.list` 文件，检查是否有指向已失效仓库的条目。如果有，请注释掉（在行首添加 `#`）或删除这些条目。**
   - 同样地，**检查 `/etc/apt/sources.list.d/` 目录下所有的 `.list` 文件，对其中指向已失效仓库的条目进行相应的处理。**

3. 针对特定问题处理

   **对于 NVIDIA 相关的本地仓库问题 (`nv-tensorrt-local-repo` 和 `cudnn-local-repo`)如果你不需要这些特定版本的 TensorRT 或 cuDNN，可以考虑删除或重命名相关 `.list` 文件来禁用它们**：

   ```bash
   # 将这些相关.list文件进行重命名备份来禁用
   sudo mv /etc/apt/sources.list.d/nv-tensorrt-local-repo-ubuntu2004-10.7.0-cuda-11.8.list /etc/apt/sources.list.d/nv-tensorrt-local-repo-ubuntu2004-10.7.0-cuda-11.8.list.bak
   sudo mv /etc/apt/sources.list.d/nv-tensorrt-local-repo-ubuntu2004-8.6.0-cuda-11.8.list /etc/apt/sources.list.d/nv-tensorrt-local-repo-ubuntu2004-8.6.0-cuda-11.8.list.bak
   sudo mv /etc/apt/sources.list.d/cudnn-local-repo-ubuntu2004-8.4.0.27.list /etc/apt/sources.list.d/cudnn-local-repo-ubuntu2004-8.4.0.27.list.bak
   ```

   

**Docker 仓库问题**

对于 Docker 的问题，**确认你使用的 Ubuntu 版本是否与 Docker 官方支持的版本匹配。如果正确无误但依然遇到问题，你可以手动添加 Docker 的 GPG 密钥，并确保使用正确的仓库地址**：

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```



