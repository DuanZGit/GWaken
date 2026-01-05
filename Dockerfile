FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装系统依赖和Python包
RUN apt-get update && apt-get install -y \
    bluez \
    bluetooth \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建配置文件目录
RUN mkdir -p /app/sleep_monitor

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV PYTHONPATH=/app

# 启动命令
CMD ["python", "-m", "sleep_monitor.run_api", "5000"]