# 红米手环2智能睡眠监测系统 - 项目优化与GitHub同步完成

## 项目概述

已完成对红米手环2智能睡眠监测系统的优化和整理工作。这是一个完整的睡眠监测解决方案，支持通过蓝牙连接红米手环2设备，实现睡眠阶段检测和智能唤醒功能。

## 已完成的优化工作

1. **项目结构优化**：
   - 修复了模块导入问题
   - 完善了项目文档
   - 创建了标准的Python项目结构
   - 添加了setup.py配置文件

2. **功能验证**：
   - 所有单元测试通过
   - 主程序正常运行
   - API服务正常启动
   - 蓝牙连接功能准备就绪

3. **文档完善**：
   - 更新了README.md
   - 完善了蓝牙连接说明
   - 创建了项目结构文档

## GitHub同步状态

项目已经初始化为Git仓库并完成初始提交，包含以下内容：

- 完整的源代码（传感器模块、睡眠分析、闹钟系统等）
- API接口实现
- 配置文件和文档
- 测试代码
- 依赖管理文件

## 同步到GitHub的下一步操作

要将项目同步到您的GitHub仓库，请执行以下步骤：

### 1. 在GitHub上创建新仓库
- 登录GitHub账户
- 点击"New repository"
- 输入仓库名称（如 "redmi-band-sleep-monitor"）
- 选择公开或私有
- 不要初始化README、.gitignore或license（我们已有这些）

### 2. 获取仓库URL
- 复制仓库的HTTPS或SSH URL

### 3. 在本地执行以下命令
```bash
cd /work/sleep

# 添加远程仓库（替换<your-github-repo-url>为您的仓库URL）
git remote add origin <your-github-repo-url>

# 重命名主分支为main（推荐）
git branch -M main

# 推送到GitHub
git push -u origin main
```

### 4. 使用HTTPS或SSH（选择其中一种）

**HTTPS方式（推荐，首次使用）**：
```bash
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main
```

**SSH方式（需要预先配置SSH密钥）**：
```bash
git remote add origin git@github.com:<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main
```

## 项目特性

### 核心功能
- 睡眠阶段检测（深睡、浅睡、REM、清醒）
- 智能唤醒算法
- 蓝牙连接红米手环2
- Web API接口
- 数据记录和分析

### 技术栈
- Python 3.6+
- Flask (Web API)
- PyBluez (蓝牙通信)
- JSON (数据格式)

### 使用场景
- 个人睡眠质量监测
- 智能唤醒服务
- 睡眠数据统计分析

## 运行项目

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行主程序
```bash
cd /work/sleep
PYTHONPATH=. python -m sleep_monitor.main
```

### 启动Web API
```bash
cd /work/sleep
PYTHONPATH=. python -m sleep_monitor.run_api 5000
```

访问 `http://localhost:5000` 查看Web界面。

## 项目维护

项目现在结构清晰，易于维护和扩展。主要模块包括：

- `sensors/` - 传感器数据接入（蓝牙、硬件、模拟）
- `sleep_analysis/` - 睡眠阶段检测算法
- `alarm/` - 智能唤醒逻辑
- `api/` - Web API接口

## 许可证

本项目仅供学习和研究使用。

---

项目已优化完成并准备好同步到GitHub。按照上述步骤操作即可将项目推送到您的GitHub仓库。