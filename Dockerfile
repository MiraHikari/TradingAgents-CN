# 多阶段构建Dockerfile
FROM node:18-alpine AS frontend-builder

# 设置工作目录
WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/package*.json ./

# 安装前端依赖
RUN npm ci --only=production

# 复制前端源代码
COPY frontend/src ./src
COPY frontend/public ./public

# 构建前端
RUN npm run build

# Python后端阶段
FROM python:3.10-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=api/app.py
ENV FLASK_ENV=production

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制Python依赖文件
COPY requirements.txt .
COPY pyproject.toml .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask flask-cors

# 复制项目源代码
COPY tradingagents/ ./tradingagents/
COPY api/ ./api/

# 从前端构建阶段复制构建结果
COPY --from=frontend-builder /app/frontend/build ./api/static

# 创建非root用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# 启动命令
CMD ["python", "api/app.py"]
