#!/usr/bin/env python3
"""
TradingAgents-CN Flask + React 启动脚本
同时启动Flask API后端和React前端
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def main():
    """主函数"""
    print("🚀 TradingAgents-CN Flask + React 应用启动器")
    print("=" * 60)
    
    # 获取项目根目录
    project_root = Path(__file__).parent
    api_dir = project_root / "api"
    frontend_dir = project_root / "frontend"
    
    # 检查目录是否存在
    if not api_dir.exists():
        print(f"❌ API目录不存在: {api_dir}")
        return
    
    if not frontend_dir.exists():
        print(f"❌ 前端目录不存在: {frontend_dir}")
        return
    
    # 检查虚拟环境
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if not in_venv:
        print("⚠️ 建议在虚拟环境中运行:")
        print("   Windows: .\\env\\Scripts\\activate")
        print("   Linux/macOS: source env/bin/activate")
        print()
    
    # 检查依赖
    print("🔍 检查依赖...")
    
    # 检查Flask依赖
    try:
        import flask
        print("✅ Flask已安装")
    except ImportError:
        print("❌ Flask未安装，正在安装...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(api_dir / "requirements.txt")], check=True)
            print("✅ Flask依赖安装成功")
        except subprocess.CalledProcessError:
            print("❌ Flask依赖安装失败")
            return
    
    # 检查Node.js和npm
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("✅ Node.js和npm已安装")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js或npm未安装，请先安装Node.js")
        return
    
    # 检查前端依赖
    if not (frontend_dir / "node_modules").exists():
        print("📦 安装前端依赖...")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            print("✅ 前端依赖安装成功")
        except subprocess.CalledProcessError:
            print("❌ 前端依赖安装失败")
            return
    else:
        print("✅ 前端依赖已安装")
    
    # 设置环境变量
    env = os.environ.copy()
    current_path = env.get('PYTHONPATH', '')
    if current_path:
        env['PYTHONPATH'] = f"{project_root}{os.pathsep}{current_path}"
    else:
        env['PYTHONPATH'] = str(project_root)
    
    # 启动Flask API
    print("\n🌐 启动Flask API服务...")
    flask_cmd = [
        sys.executable, str(api_dir / "app.py")
    ]
    
    flask_process = subprocess.Popen(
        flask_cmd,
        cwd=project_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待Flask启动
    print("⏳ 等待Flask API启动...")
    time.sleep(5)
    
    # 检查Flask是否启动成功
    if flask_process.poll() is not None:
        print("❌ Flask API启动失败")
        return
    
    print("✅ Flask API启动成功 (http://localhost:5000)")
    
    # 启动React前端
    print("\n⚛️ 启动React前端...")
    react_cmd = ["npm", "start"]
    
    react_process = subprocess.Popen(
        react_cmd,
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("✅ React前端启动成功 (http://localhost:3000)")
    print("\n🎉 应用启动完成！")
    print("📱 前端地址: http://localhost:3000")
    print("🔧 API地址: http://localhost:5000")
    print("⏹️  按 Ctrl+C 停止所有服务")
    print("=" * 60)
    
    # 信号处理
    def signal_handler(signum, frame):
        print("\n⏹️ 正在停止服务...")
        flask_process.terminate()
        react_process.terminate()
        
        # 等待进程结束
        flask_process.wait()
        react_process.wait()
        
        print("✅ 所有服务已停止")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 监控进程
    try:
        while True:
            if flask_process.poll() is not None:
                print("❌ Flask API进程意外退出")
                break
            
            if react_process.poll() is not None:
                print("❌ React前端进程意外退出")
                break
            
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()