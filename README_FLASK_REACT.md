# TradingAgents-CN Flask + React 版本

基于Flask API和React前端的现代化股票分析平台，提供更好的用户体验和扩展性。

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 16+
- npm 8+

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd tradingagents-cn
```

2. **安装Python依赖**
```bash
# 创建虚拟环境
python -m venv env

# 激活虚拟环境
# Windows
env\Scripts\activate
# Linux/macOS
source env/bin/activate

# 安装依赖
pip install -e .
```

3. **安装前端依赖**
```bash
cd frontend
npm install
cd ..
```

### 启动应用

使用一键启动脚本：
```bash
python start_flask_react.py
```

或者分别启动：

**启动Flask API后端：**
```bash
cd api
python app.py
```

**启动React前端：**
```bash
cd frontend
npm start
```

访问地址：
- 前端：http://localhost:3000
- API：http://localhost:5000

## 📁 项目结构

```
├── api/                    # Flask API后端
│   ├── app.py             # 主应用文件
│   └── requirements.txt   # Python依赖
├── frontend/              # React前端
│   ├── src/
│   │   ├── components/    # React组件
│   │   │   ├── StockAnalysis.js
│   │   │   ├── StockList.js
│   │   │   └── Settings.js
│   │   ├── App.js         # 主应用组件
│   │   └── App.css        # 样式文件
│   └── package.json       # Node.js依赖
├── tradingagents/         # 核心TradingAgents模块
├── start_flask_react.py   # 一键启动脚本
└── README_FLASK_REACT.md  # 本文档
```

## 🔧 API接口

### 健康检查
```
GET /api/health
```

### 股票分析
```
POST /api/analyze
Content-Type: application/json

{
  "stock_code": "AAPL",
  "date": "2024-01-15"
}
```

### 获取股票列表
```
GET /api/stocks
```

### 获取配置信息
```
GET /api/config
```

### 获取服务状态
```
GET /api/status
```

## 🎨 前端功能

### 股票分析页面
- 股票代码输入
- 分析日期选择
- 实时分析结果显示
- 投资建议和风险评估

### 股票列表页面
- 可分析股票列表
- 搜索和筛选功能
- 分页显示

### 设置页面
- 系统状态监控
- 配置信息显示
- API连接状态

## 🛠️ 技术栈

### 后端
- **Flask**: Web框架
- **Flask-CORS**: 跨域支持
- **TradingAgents**: 核心分析引擎

### 前端
- **React 18**: 前端框架
- **Ant Design**: UI组件库
- **Axios**: HTTP客户端
- **Day.js**: 日期处理

## 🔄 开发模式

### 后端开发
```bash
cd api
python app.py
```

### 前端开发
```bash
cd frontend
npm start
```

### 热重载
- 前端代码修改会自动重载
- 后端代码修改需要重启Flask服务

## 📦 部署

### 生产环境构建

1. **构建前端**
```bash
cd frontend
npm run build
```

2. **配置Flask生产环境**
```bash
export FLASK_ENV=production
cd api
python app.py
```

### Docker部署
```bash
# 构建镜像
docker build -t tradingagents-flask-react .

# 运行容器
docker run -p 5000:5000 -p 3000:3000 tradingagents-flask-react
```

## 🔍 故障排除

### 常见问题

1. **API连接失败**
   - 检查Flask服务是否启动
   - 确认端口5000未被占用
   - 检查防火墙设置

2. **前端无法启动**
   - 确认Node.js版本 >= 16
   - 删除node_modules重新安装
   - 检查端口3000是否被占用

3. **模块导入错误**
   - 确认虚拟环境已激活
   - 检查PYTHONPATH设置
   - 重新安装项目依赖

### 日志查看

**Flask日志：**
```bash
cd api
python app.py 2>&1 | tee flask.log
```

**React日志：**
```bash
cd frontend
npm start 2>&1 | tee react.log
```

## 🤝 贡献

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目基于Apache 2.0许可证开源。

## 🙏 致谢

感谢原项目 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 提供的核心分析引擎。