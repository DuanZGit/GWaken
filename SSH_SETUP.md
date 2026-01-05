# GitHub SSH 密钥配置说明

要将项目推送到您的 GitHub 仓库，您需要配置 SSH 密钥。

## 步骤 1: 生成 SSH 密钥

在您的本地机器上执行以下命令：

```bash
# 生成新的 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 按提示操作：
# 1. 选择保存位置（通常使用默认）
# 2. 设置密码短语（可选，直接回车跳过）
```

## 步骤 2: 添加 SSH 密钥到 ssh-agent

```bash
# 启动 ssh-agent
eval "$(ssh-agent -s)"

# 添加 SSH 私钥到 ssh-agent
ssh-add ~/.ssh/id_ed25519
```

## 步骤 3: 将 SSH 公钥添加到 GitHub

1. 复制公钥内容：
```bash
cat ~/.ssh/id_ed25519.pub
```

2. 登录 GitHub，进入：
   - Settings → SSH and GPG keys → New SSH key

3. 粘贴公钥内容，点击 "Add SSH key"

## 步骤 4: 测试连接

```bash
ssh -T git@github.com
```

## 步骤 5: 推送项目

配置完成后，您可以执行：

```bash
cd /work/sleep
git push -u origin main
```

## 备选方案：使用个人访问令牌

如果您不想配置 SSH，也可以使用个人访问令牌：

1. 在 GitHub 生成个人访问令牌
2. 使用 HTTPS 推送：
```bash
git remote set-url origin https://github.com/DuanZGit/GWaken.git
git push -u origin main
```