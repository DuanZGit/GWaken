# 推送项目到 GitHub

项目已完全准备就绪，您需要在本地环境中使用个人访问令牌完成推送。

## 步骤 1: 生成 GitHub 个人访问令牌

1. 登录 GitHub
2. 进入 Settings → Developer settings → Personal access tokens → Tokens (classic)
3. 点击 "Generate new token"
4. 选择 "repo" 权限（允许对仓库的完全访问）
5. 复制生成的令牌（注意：令牌只显示一次）

## 步骤 2: 推送项目

### 方法 1: 使用命令行（推荐）
```bash
cd /work/sleep

# 使用以下命令推送（将 YOUR_TOKEN 替换为您的实际令牌）
git -c http.extraheader="Authorization: Basic $(echo -n 'DuanZGit:YOUR_TOKEN' | base64)" push --set-upstream origin main
```

### 方法 2: 配置凭据助手
```bash
cd /work/sleep

# 存储凭据
git config --global credential.helper store

# 设置远程仓库URL
git remote set-url origin https://github.com/DuanZGit/GWaken.git

# 第一次推送时输入用户名和令牌
git push --set-upstream origin main
```

### 方法 3: 在 VS Code 或其他 Git 客户端中推送
1. 打开项目文件夹
2. 使用图形界面进行推送
3. 当提示输入密码时，输入您的个人访问令牌

## 验证推送成功

推送完成后，您可以在 https://github.com/DuanZGit/GWaken 查看项目

## 项目信息

- 项目名称: GWaken (智能睡眠监测和唤醒系统)
- 功能: 红米手环2睡眠监测、智能唤醒算法、Web API接口
- 包含: 完整的源代码、配置文件、文档和测试

项目已完全优化，所有功能都已验证通过，随时可以推送至您的GitHub仓库。