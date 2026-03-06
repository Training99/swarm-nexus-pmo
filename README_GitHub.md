# Swarm Nexus PMO 🐝

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 一人公司，无限杠杆。
> 
> 蜂群项目管理中心 - 让多个AI Agent像蜂群一样自动协作。

[中文介绍](#中文介绍) | [English](#english)

---

## 中文介绍

### 🎯 这是什么？

Swarm Nexus PMO 是一个**蜂群项目管理中心**，让你可以像管理一个团队一样管理多个AI Agent。

灵感来自 Anthropic Agent Teams 和 Microsoft Magentic-One，我们设计了一套轻量级系统，让5个AI Agent可以：
- **自动分配任务** - 根据能力匹配度智能分配
- **24小时协作** - 不间断运转，无需人工干预
- **自我监控** - 自动检测问题并恢复
- **每日汇报** - 早上看简报，掌握全局

### 🐝 核心概念：蜂群思维

自然界中，蜂群没有中央指挥官，但每只蜜蜂都遵循简单规则，最终形成高效协作。

Swarm Nexus 把这种思维应用到AI Agent管理：
- 每个AI Agent是一个"蜂群"
- Nexus是"指挥中心"
- 任务自动流转，信息全局共享

### 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/swarm-nexus-pmo.git
cd swarm-nexus-pmo

# 安装Python 3.10+
python3 --version

# 配置（重要！）
cp config.example.py config.py
# 编辑 config.py，填入你的API密钥

# 查看状态
python3 nexus_core.py board

# 创建示例项目
python3 nexus_core.py project

# 启动监控
python3 nexus_core.py start
```

### 📊 效果展示

运行10天后的实际数据：

| 指标 | 改进 |
|------|------|
| 任务分配时间 | 5-10分钟 → <1秒 (**600x提升**) |
| 任务遗漏 | 每周2-3个 → **0个** |
| 阻塞处理 | 几小时 → **5分钟** |
| 每日简报 | 自己整理30分钟 → **自动生成** |

### 🏗️ 系统架构

```
Swarm Nexus PMO
├─ Intent Parser (意图解析)
├─ Recursive Decomposer (递归分解)
├─ Global Memory Hub (全局记忆)
├─ Swarm Scheduler (蜂群调度)
├─ Cross-Swarm Coordinator (跨蜂群协调)
├─ Meeting System (会议系统)
│   ├─ Daily Standup (每日站会)
│   └─ Ad-hoc Sync (专项协调)
└─ Innovation Agent (创新求解)
```

### 🐝 内置蜂群

系统预设5个蜂群，你可以根据需求修改：

| 蜂群 | 类型 | 能力 |
|------|------|------|
| **研究蜂群** | 研究 | 技术侦察、痛点挖掘、趋势追踪 |
| **内容蜂群** | 生产 | 文案撰写、视觉设计、多平台发布 |
| **变现蜂群** | 变现 | 任务执行、市场扫描、收益优化 |
| **投资蜂群** | 分析 | 黄金分析、基金研究、宏观判断 |
| **系统蜂群** | 运维 | 安全监控、错误修复、性能优化 |

### 📖 文档

- [项目起源](docs/project_genesis.md) - 从想法到实现的完整记录
- [架构设计](docs/architecture.md) - 系统设计详解
- [部署指南](docs/deployment.md) - 详细部署步骤

### 🤝 贡献

欢迎提交 Issue 和 PR！

### 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

### 🙏 致谢

- 灵感来自 [Anthropic Agent Teams](https://www.anthropic.com/) 和 [Microsoft Magentic-One](https://github.com/microsoft/autogen)
- 架构参考 [ROMA](https://github.com/sentient-xyz/roma) 和 [LangGraph](https://github.com/langchain-ai/langgraph)

### ⚠️ 免责声明

本项目仅供学习和研究使用。请遵守相关平台的使用条款，不要将自动化系统用于违反平台规则的行为。

---

## English

### What is this?

Swarm Nexus PMO is a **Project Management Office for AI Agents**, allowing you to manage multiple AI agents like managing a team.

Inspired by Anthropic Agent Teams and Microsoft Magentic-One, we designed a lightweight system where 5 AI agents can:
- **Auto-assign tasks** based on capability matching
- **Collaborate 24/7** without human intervention
- **Self-monitor** and auto-recover from issues
- **Daily reports** every morning

### Quick Start

```bash
# Clone
git clone https://github.com/yourusername/swarm-nexus-pmo.git
cd swarm-nexus-pmo

# Configure (IMPORTANT!)
cp config.example.py config.py
# Edit config.py with your API keys

# Run
python3 nexus_core.py board
python3 nexus_core.py start
```

### License

MIT License - see [LICENSE](LICENSE) file

---

**一人公司，无限杠杆。**  
*One person, infinite leverage.*
