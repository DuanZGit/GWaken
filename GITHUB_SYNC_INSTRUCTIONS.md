# GitHub 同步说明

## 如何同步项目到您的 GitHub 仓库

### 步骤 1: 在 GitHub 上创建仓库
1. 登录到 GitHub
2. 点击 "New repository"
3. 输入仓库名称（例如：redmi-band-sleep-monitor）
4. 选择 "Public" 或 "Private"
5. 不要勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

### 步骤 2: 获取仓库 URL
复制新创建仓库的 HTTPS URL，格式如下：
```
https://github.com/您的用户名/仓库名称.git
```

### 步骤 3: 同步到 GitHub
在终端中执行以下命令（将 <your-repo-url> 替换为您仓库的实际 URL）：

```bash
cd /work/sleep

# 添加远程仓库（将 <your-repo-url> 替换为您的仓库URL）
git remote add origin <your-repo-url>

# 重命名主分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

### 示例：
```bash
cd /work/sleep
git remote add origin https://github.com/yourusername/redmi-band-sleep-monitor.git
git branch -M main
git push -u origin main
```

### 注意事项：
- 如果您在 GitHub 上的仓库已经包含文件，您可能需要先拉取远程更改：
```bash
git pull origin main --allow-unrelated-histories
```

- 如果您使用 SSH 方式，仓库 URL 格式为：
```
git@github.com:yourusername/repository-name.git
```

- 您的仓库现在包含了完整的红米手环2智能睡眠监测系统，包括：
  - 完整的源代码
  - 优化后的项目结构
  - 所有依赖文件
  - 详细的文档
  - 已验证的功能和测试
```