# GWaken - 项目概述

## 项目名称
GWaken - 智能睡眠监测与唤醒系统

## 项目描述
一个专门适配红米手环2设备的智能睡眠监测系统，能够检测睡眠阶段并在浅睡眠阶段智能唤醒用户。

## 核心功能
1. **睡眠阶段检测**
   - 深度睡眠检测
   - 浅度睡眠检测
   - REM睡眠检测
   - 清醒状态检测

2. **智能唤醒系统**
   - 在浅睡眠阶段唤醒
   - 渐进式震动提醒
   - 个性化唤醒时间

3. **数据采集与分析**
   - 心率监测
   - 体动检测
   - 睡眠质量分析

4. **设备连接**
   - 蓝牙连接红米手环2
   - 传感器数据获取
   - 实时数据同步

5. **Web API接口**
   - RESTful API设计
   - 设备管理接口
   - 数据获取接口
   - 睡眠分析接口

## 技术栈
- **语言**: Python 3.6+
- **框架**: Flask (Web API)
- **库**: PyBluez (蓝牙通信)
- **协议**: JSON数据格式

## 项目结构
```
GWaken/
├── README.md              # 项目说明
├── CHANGELOG.md           # 更新日志
├── requirements.txt       # 依赖包列表
├── setup.py               # 安装配置
├── config.json            # 配置文件
├── Dockerfile             # 容器化配置
├── sleep_monitor/         # 主要代码目录
│   ├── main.py            # 主程序入口
│   ├── run_api.py         # API运行脚本
│   ├── sensors/           # 传感器模块
│   ├── sleep_analysis/    # 睡眠分析模块
│   ├── alarm/             # 闹钟模块
│   ├── api/               # API接口
│   ├── utils/             # 工具模块
│   └── tests/             # 测试模块
└── docs/                  # 文档目录
```

## 部署方式
1. **本地运行**: `python -m sleep_monitor.main`
2. **API服务**: `python -m sleep_monitor.run_api`
3. **Docker部署**: `docker build -t g-waken .`
4. **生产环境**: 使用Gunicorn + Nginx

## 许可证
仅供学习和研究使用

## 最后更新
2026-01-05