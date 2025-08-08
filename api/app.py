#!/usr/bin/env python3
"""
TradingAgents-CN Flask API
提供股票分析的核心API接口
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from pathlib import Path
import json
import logging
from datetime import datetime
import traceback

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入TradingAgents核心模块
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.utils.logging_manager import get_logger

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 配置日志
logger = get_logger('api')

# 全局变量存储TradingAgents实例
trading_agents = None

def initialize_trading_agents():
    """初始化TradingAgents实例"""
    global trading_agents
    try:
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = "google"
        config["backend_url"] = "https://generativelanguage.googleapis.com/v1"
        config["deep_think_llm"] = "gemini-2.0-flash"
        config["quick_think_llm"] = "gemini-2.0-flash"
        config["max_debate_rounds"] = 1
        config["online_tools"] = True
        
        trading_agents = TradingAgentsGraph(debug=True, config=config)
        logger.info("TradingAgents初始化成功")
        return True
    except Exception as e:
        logger.error(f"TradingAgents初始化失败: {e}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'TradingAgents-CN API'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_stock():
    """股票分析接口"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        stock_code = data.get('stock_code')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        if not stock_code:
            return jsonify({'error': '股票代码不能为空'}), 400
        
        if not trading_agents:
            return jsonify({'error': 'TradingAgents未初始化'}), 500
        
        logger.info(f"开始分析股票: {stock_code}, 日期: {date}")
        
        # 执行分析
        _, decision = trading_agents.propagate(stock_code, date)
        
        return jsonify({
            'success': True,
            'stock_code': stock_code,
            'date': date,
            'analysis': decision,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"分析失败: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': f'分析失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """获取股票列表接口"""
    try:
        # 这里可以集成现有的股票数据API
        # 暂时返回示例数据
        stocks = [
            {'code': '000001', 'name': '平安银行', 'market': 'A股'},
            {'code': '000002', 'name': '万科A', 'market': 'A股'},
            {'code': 'AAPL', 'name': 'Apple Inc.', 'market': '美股'},
            {'code': 'NVDA', 'name': 'NVIDIA Corporation', 'market': '美股'},
        ]
        
        return jsonify({
            'success': True,
            'stocks': stocks,
            'count': len(stocks)
        })
        
    except Exception as e:
        logger.error(f"获取股票列表失败: {e}")
        return jsonify({'error': f'获取股票列表失败: {str(e)}'}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取配置信息"""
    try:
        config_info = {
            'llm_provider': DEFAULT_CONFIG.get('llm_provider', 'unknown'),
            'available_providers': ['google', 'openai', 'dashscope', 'deepseek'],
            'version': 'cn-0.1.12'
        }
        
        return jsonify({
            'success': True,
            'config': config_info
        })
        
    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        return jsonify({'error': f'获取配置失败: {str(e)}'}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取服务状态"""
    try:
        status = {
            'trading_agents_initialized': trading_agents is not None,
            'timestamp': datetime.now().isoformat(),
            'service': 'TradingAgents-CN API'
        }
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"获取状态失败: {e}")
        return jsonify({'error': f'获取状态失败: {str(e)}'}), 500

if __name__ == '__main__':
    # 初始化TradingAgents
    if initialize_trading_agents():
        logger.info("API服务启动成功")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.error("API服务启动失败")
        sys.exit(1)