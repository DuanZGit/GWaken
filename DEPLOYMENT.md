# 部署说明

## 部署到不同平台的说明

### 1. 部署到 Heroku

1. 安装 Heroku CLI:
```bash
# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# macOS
brew tap heroku/brew && brew install heroku
```

2. 登录 Heroku:
```bash
heroku login
```

3. 创建应用:
```bash
heroku create your-app-name
```

4. 设置构建包:
```bash
heroku buildpacks:set heroku/python
```

5. 部署:
```bash
git push heroku main
```

6. 打开应用:
```bash
heroku open
```

### 2. 部署到 PythonAnywhere

1. 在 PythonAnywhere 注册账户
2. 创建新 Web 应用
3. 选择 Manual Configuration (Django, Flask, etc.)
4. 选择 Python 3.x
5. 在 Bash 终端中克隆项目:
```bash
cd ~
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

6. 创建虚拟环境并安装依赖:
```bash
mkvirtualenv --python=/usr/bin/python3.8 sleep-monitor
pip install -r requirements.txt
```

7. 配置 Web 应用:
   - WSGI 配置文件: `~/your-repo-name/sleep_monitor/api/sleep_api.py`
   - 应用路径: `/home/yourusername/your-repo-name`

### 3. 部署到 AWS EC2

1. 启动 EC2 实例 (Ubuntu)
2. 连接到实例
3. 安装依赖:
```bash
sudo apt update
sudo apt install python3-pip git
```

4. 克隆并部署:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
pip3 install -r requirements.txt
```

5. 使用 Gunicorn 运行:
```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 sleep_monitor.api.sleep_api:app
```

6. 设置 Nginx 反向代理 (可选):

### 4. 部署到 Google Cloud Run

1. 准备 Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "sleep_monitor.api.sleep_api:app"]
```

2. 构建并部署:
```bash
gcloud run deploy --image gcr.io/PROJECT-ID/sleep-monitor --platform managed
```

### 5. Docker 部署

创建 Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "sleep_monitor.run_api", "5000"]
```

构建和运行:
```bash
docker build -t sleep-monitor .
docker run -p 5000:5000 sleep-monitor
```

### 6. 本地部署

1. 克隆仓库:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. 创建虚拟环境:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖:
```bash
pip install -r requirements.txt
```

4. 运行 API 服务:
```bash
python -m sleep_monitor.run_api
```

## 环境变量配置

根据部署环境，您可能需要设置以下环境变量：

```bash
# 端口设置
PORT=5000

# 调试模式
FLASK_DEBUG=0  # 生产环境中设为0

# 蓝牙设备配置
BLUETOOTH_DEVICE_ADDRESS=

# API密钥（如果使用）
ACCESS_TOKEN=your_token_here
```

## 配置文件

确保部署时包含正确的 config.json 文件，或通过环境变量配置参数。

## 注意事项

1. 在生产环境中运行时，不要使用内置的 Flask 开发服务器
2. 使用 Gunicorn 或 uWSGI 等 WSGI 服务器
3. 配置适当的日志记录
4. 设置适当的安全头
5. 在云环境中，蓝牙功能可能受限，建议使用模拟模式