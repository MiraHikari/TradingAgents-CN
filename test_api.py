#!/usr/bin/env python3
"""
TradingAgents-CN API 测试脚本
测试Flask API的各项功能
"""

import requests
import json
import time
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功: {data}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_get_stocks():
    """测试获取股票列表接口"""
    print("\n🔍 测试获取股票列表接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/stocks")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取股票列表成功: 共{data.get('count', 0)}只股票")
            for stock in data.get('stocks', [])[:3]:  # 只显示前3只
                print(f"   - {stock.get('code')}: {stock.get('name')} ({stock.get('market')})")
            return True
        else:
            print(f"❌ 获取股票列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取股票列表异常: {e}")
        return False

def test_get_config():
    """测试获取配置接口"""
    print("\n🔍 测试获取配置接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/config")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取配置成功:")
            print(f"   - LLM提供商: {data.get('config', {}).get('llm_provider')}")
            print(f"   - 版本: {data.get('config', {}).get('version')}")
            return True
        else:
            print(f"❌ 获取配置失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取配置异常: {e}")
        return False

def test_get_status():
    """测试获取状态接口"""
    print("\n🔍 测试获取状态接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取状态成功:")
            print(f"   - TradingAgents状态: {data.get('status', {}).get('trading_agents_initialized')}")
            print(f"   - 服务名称: {data.get('status', {}).get('service')}")
            return True
        else:
            print(f"❌ 获取状态失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取状态异常: {e}")
        return False

def test_analyze_stock():
    """测试股票分析接口"""
    print("\n🔍 测试股票分析接口...")
    try:
        # 测试数据
        test_data = {
            "stock_code": "AAPL",
            "date": datetime.now().strftime('%Y-%m-%d')
        }
        
        print(f"📊 分析股票: {test_data['stock_code']} ({test_data['date']})")
        
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 股票分析成功:")
            print(f"   - 股票代码: {data.get('stock_code')}")
            print(f"   - 分析日期: {data.get('date')}")
            print(f"   - 分析结果: {data.get('analysis', {})}")
            return True
        else:
            print(f"❌ 股票分析失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 股票分析异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 TradingAgents-CN API 测试开始")
    print("=" * 50)
    
    # 等待API服务启动
    print("⏳ 等待API服务启动...")
    time.sleep(3)
    
    # 执行测试
    tests = [
        test_health_check,
        test_get_stocks,
        test_get_config,
        test_get_status,
        test_analyze_stock,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！API服务运行正常。")
    else:
        print("⚠️ 部分测试失败，请检查API服务状态。")
    
    print("\n💡 提示:")
    print("   - 确保Flask API服务正在运行 (python api/app.py)")
    print("   - 检查端口5000是否被占用")
    print("   - 查看API服务日志获取详细错误信息")

if __name__ == "__main__":
    main()