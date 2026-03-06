#!/bin/bash
# Swarm Nexus PMO 启动脚本
# 蜂群项目管理中心

cd /root/.openclaw/workspace/swarm_nexus

echo "🐝 Swarm Nexus PMO - 蜂群项目管理中心"
echo "========================================"
echo ""

# 检查参数
if [ "$1" == "start" ]; then
    echo "启动 24/7 监控模式..."
    python3 nexus_core.py start
    
elif [ "$1" == "board" ]; then
    echo "显示同步看板..."
    python3 nexus_core.py board
    
elif [ "$1" == "project" ]; then
    echo "创建示例项目..."
    python3 nexus_core.py project
    
elif [ "$1" == "standup" ]; then
    echo "手动触发站会..."
    python3 nexus_core.py standup
    
elif [ "$1" == "status" ]; then
    echo "查看系统状态..."
    python3 nexus_core.py status
    
elif [ "$1" == "monitor" ]; then
    echo "启动后台监控 (持续运行)..."
    nohup python3 nexus_core.py start > nexus_monitor.log 2>&1 &
    echo "PID: $!"
    echo "日志: swarm_nexus/nexus_monitor.log"
    
else
    echo "用法: ./nexus.sh [命令]"
    echo ""
    echo "命令:"
    echo "  start    - 启动24/7监控 (前台)"
    echo "  monitor  - 启动24/7监控 (后台)"
    echo "  board    - 显示同步看板"
    echo "  project  - 创建示例项目"
    echo "  standup  - 手动触发站会"
    echo "  status   - 查看系统状态"
    echo ""
    echo "示例:"
    echo "  ./nexus.sh board      # 快速查看看板"
    echo "  ./nexus.sh monitor    # 后台启动监控"
fi
