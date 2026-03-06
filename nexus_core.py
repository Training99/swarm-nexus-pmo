#!/usr/bin/env python3
"""
Swarm Nexus V0.1 - 蜂群项目管理中心
PMO (Project Management Office) for Multi-Swarm Coordination

Core Responsibilities:
1. 24/7 Project Monitoring - Track all tasks across all swarms
2. Task Leak Prevention - Detect and assign orphaned tasks
3. Security Oversight - Continuous security monitoring
4. Cross-Swarm Coordination - Daily standups + ad-hoc sync
5. Innovation Agent - Creative problem solving when swarms are stuck

Author: Atlas_T
Created: 2026-03-07
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
# Project paths
WORKSPACE = Path('/root/.openclaw/workspace')
NEXUS_DIR = WORKSPACE / 'swarm_nexus'
NEXUS_DIR.mkdir(exist_ok=True)

class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    ORPHANED = "orphaned"  # 被遗忘的任务

class RiskLevel(Enum):
    CRITICAL = "critical"    # 立即处理
    HIGH = "high"           # 4小时内处理
    MEDIUM = "medium"       # 24小时内处理
    LOW = "low"             # 记录即可

@dataclass
class Task:
    """任务定义"""
    id: str
    name: str
    description: str
    project_id: str
    source: str  # 来源：用户指令/蜂群生成/系统检测
    required_capabilities: List[str]  # 所需能力
    assigned_swarm: Optional[str] = None
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 3  # 1-5, 1最高
    created_at: str = ""
    deadline: Optional[str] = None
    dependencies: List[str] = None
    progress: int = 0  # 0-100
    block_reason: Optional[str] = None
    last_updated: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.last_updated:
            self.last_updated = self.created_at
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class SwarmStatus:
    """蜂群状态"""
    swarm_id: str
    swarm_type: str  # evomap, investment, content, opportunity, system
    status: str  # active, idle, blocked, error
    current_task: Optional[str] = None
    task_queue_length: int = 0
    last_heartbeat: str = ""
    capabilities: List[str] = None
    performance_score: float = 1.0  # 0-1
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if not self.last_heartbeat:
            self.last_heartbeat = datetime.now().isoformat()

@dataclass
class SecurityAlert:
    """安全告警"""
    id: str
    level: RiskLevel
    category: str  # api_key, unauthorized_access, anomaly, etc.
    description: str
    source: str
    detected_at: str
    status: str = "open"  # open, investigating, resolved
    assigned_to: Optional[str] = None
    
    def __post_init__(self):
        if not self.detected_at:
            self.detected_at = datetime.now().isoformat()

class GlobalMemoryHub:
    """全局记忆中心 - 所有蜂群共享"""
    
    def __init__(self):
        self.memory_file = NEXUS_DIR / 'global_memory.json'
        self._memory = self._load()
    
    def _load(self) -> Dict:
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'projects': {},
            'tasks': {},
            'swarm_states': {},
            'security_alerts': [],
            'meeting_minutes': [],
            'innovation_solutions': []
        }
    
    def save(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self._memory, f, ensure_ascii=False, indent=2)
    
    def get_project(self, project_id: str) -> Dict:
        return self._memory['projects'].get(project_id, {})
    
    def save_project(self, project_id: str, data: Dict):
        self._memory['projects'][project_id] = data
        self.save()
    
    def get_task(self, task_id: str) -> Optional[Task]:
        data = self._memory['tasks'].get(task_id)
        if data:
            # 将字符串状态转换回枚举
            if isinstance(data.get('status'), str):
                data['status'] = TaskStatus(data['status'])
            return Task(**data)
        return None
    
    def save_task(self, task: Task):
        """保存任务到记忆"""
        task_dict = asdict(task)
        # 转换枚举类型为字符串
        task_dict['status'] = task.status.value
        self._memory['tasks'][task.id] = task_dict
        self.save()
    
    def get_all_tasks(self) -> List[Task]:
        tasks = []
        for data in self._memory['tasks'].values():
            # 将字符串状态转换回枚举
            if isinstance(data.get('status'), str):
                data['status'] = TaskStatus(data['status'])
            tasks.append(Task(**data))
        return tasks
    
    def get_orphaned_tasks(self) -> List[Task]:
        """获取被遗忘的任务（超过2小时未更新且无进度）"""
        orphaned = []
        now = datetime.now()
        for task in self.get_all_tasks():
            if task.status in [TaskStatus.PENDING, TaskStatus.ASSIGNED]:
                last_update = datetime.fromisoformat(task.last_updated)
                hours_inactive = (now - last_update).total_seconds() / 3600
                if hours_inactive > 2 and task.progress == 0:
                    orphaned.append(task)
        return orphaned
    
    def save_swarm_state(self, swarm_id: str, state: SwarmStatus):
        self._memory['swarm_states'][swarm_id] = asdict(state)
        self.save()
    
    def get_swarm_states(self) -> Dict[str, SwarmStatus]:
        return {
            k: SwarmStatus(**v) 
            for k, v in self._memory['swarm_states'].items()
        }
    
    def add_security_alert(self, alert: SecurityAlert):
        self._memory['security_alerts'].append(asdict(alert))
        self.save()
    
    def get_open_alerts(self) -> List[SecurityAlert]:
        return [
            SecurityAlert(**data) 
            for data in self._memory['security_alerts']
            if data['status'] == 'open'
        ]

class InnovationAgent:
    """
    创新求解Agent
    当所有蜂群都无法解决问题时，Innovation Agent介入
    使用创意方法、外部资源、非传统思路寻找解决方案
    """
    
    def __init__(self, memory_hub: GlobalMemoryHub):
        self.memory = memory_hub
        self.solution_history = []
    
    def solve(self, problem: Dict) -> Dict:
        """
        创新求解流程
        
        problem格式:
        {
            'type': 'blocked_task' | 'security_threat' | 'resource_shortage' | 'capability_gap',
            'description': '问题描述',
            'attempted_solutions': [],  # 已尝试的方案
            'constraints': [],  # 约束条件
            'context': {}  # 上下文信息
        }
        """
        print(f"🧠 Innovation Agent analyzing: {problem['description'][:50]}...")
        
        solution_strategies = {
            'blocked_task': self._solve_blocked_task,
            'security_threat': self._solve_security_threat,
            'resource_shortage': self._solve_resource_shortage,
            'capability_gap': self._solve_capability_gap
        }
        
        solver = solution_strategies.get(problem['type'], self._solve_generic)
        solution = solver(problem)
        
        # 记录解决方案
        self._record_solution(problem, solution)
        
        return solution
    
    def _solve_blocked_task(self, problem: Dict) -> Dict:
        """解决阻塞任务"""
        task = problem.get('task')
        block_reason = problem.get('block_reason', '')
        
        strategies = []
        
        # 策略1: 任务分解
        if 'too complex' in block_reason.lower():
            strategies.append({
                'action': 'decompose',
                'description': '将任务分解为更小的子任务',
                'implementation': '使用递归分解，将复杂任务拆分为可管理的部分'
            })
        
        # 策略2: 跨蜂群借调
        if 'lack capability' in block_reason.lower():
            strategies.append({
                'action': 'borrow_capability',
                'description': '从其他蜂群借调能力',
                'implementation': '检查其他蜂群的能力列表，临时组建联合工作组'
            })
        
        # 策略3: 外部资源
        strategies.append({
            'action': 'external_resource',
            'description': '搜索外部解决方案',
            'implementation': '搜索GitHub、文档、社区，寻找类似问题的解决方案'
        })
        
        # 策略4: 降低要求
        strategies.append({
            'action': 'reduce_scope',
            'description': '降低任务范围或要求',
            'implementation': '先交付MVP版本，后续迭代完善'
            })
        
        return {
            'problem_type': 'blocked_task',
            'strategies': strategies,
            'recommended': strategies[0] if strategies else None,
            'confidence': 0.8
        }
    
    def _solve_security_threat(self, problem: Dict) -> Dict:
        """解决安全威胁"""
        strategies = [
            {
                'action': 'immediate_isolation',
                'description': '立即隔离受影响的系统/密钥',
                'urgency': 'immediate'
            },
            {
                'action': 'rotate_credentials',
                'description': '轮换所有相关凭证',
                'urgency': 'within_1_hour'
            },
            {
                'action': 'notify_user',
                'description': '立即通知用户',
                'urgency': 'immediate'
            }
        ]
        return {
            'problem_type': 'security_threat',
            'strategies': strategies,
            'recommended': strategies[0],
            'confidence': 0.95
        }
    
    def _solve_resource_shortage(self, problem: Dict) -> Dict:
        """解决资源短缺"""
        strategies = [
            {
                'action': 'priority_queue',
                'description': '暂停低优先级任务，释放资源给高优先级任务',
                'implementation': '重新排序任务队列'
            },
            {
                'action': 'request_external_api',
                'description': '使用外部API服务替代本地计算',
                'implementation': '调用第三方服务完成计算密集型任务'
            },
            {
                'action': 'cache_optimization',
                'description': '优化缓存策略，减少重复计算',
                'implementation': '实施24小时TTL缓存'
            }
        ]
        return {
            'problem_type': 'resource_shortage',
            'strategies': strategies,
            'recommended': strategies[0],
            'confidence': 0.75
        }
    
    def _solve_capability_gap(self, problem: Dict) -> Dict:
        """解决能力缺口"""
        missing_capability = problem.get('missing_capability', '')
        
        strategies = [
            {
                'action': 'quick_learning',
                'description': f'快速学习{missing_capability}',
                'implementation': '搜索最佳实践文档，立即应用',
                'time_estimate': '30分钟-2小时'
            },
            {
                'action': 'skill_augmentation',
                'description': '通过工具增强能力',
                'implementation': '使用现有工具组合模拟所需能力'
            },
            {
                'action': 'swarm_spawning',
                'description': '孵化新蜂群专门处理此类任务',
                'implementation': '基于模板快速创建专用蜂群',
                'time_estimate': '2-4小时'
            }
        ]
        return {
            'problem_type': 'capability_gap',
            'strategies': strategies,
            'recommended': strategies[0],
            'confidence': 0.7
        }
    
    def _solve_generic(self, problem: Dict) -> Dict:
        """通用求解"""
        return {
            'problem_type': 'generic',
            'strategies': [
                {'action': 'escalate', 'description': '升级到用户处理'},
                {'action': 'research', 'description': '深入研究问题'},
                {'action': 'workaround', 'description': '寻找临时解决方案'}
            ],
            'recommended': {'action': 'escalate', 'description': '升级到用户处理'},
            'confidence': 0.5
        }
    
    def _record_solution(self, problem: Dict, solution: Dict):
        """记录解决方案供未来参考"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'problem': problem,
            'solution': solution
        }
        self.solution_history.append(record)
        
        # 保存到全局记忆
        memory = self.memory._memory.get('innovation_solutions', [])
        memory.append(record)
        self.memory._memory['innovation_solutions'] = memory
        self.memory.save()

class SwarmMeetingSystem:
    """蜂群会议系统"""
    
    def __init__(self, memory_hub: GlobalMemoryHub):
        self.memory = memory_hub
        self.meeting_history = []
    
    def daily_standup(self, swarm_states: Dict[str, SwarmStatus]) -> str:
        """生成每日站会报告"""
        now = datetime.now()
        
        report = f"""
📅 蜂群每日站会报告 - {now.strftime('%Y-%m-%d')}
时间: NY {now.strftime('%H:%M')} | 时长: 预计15分钟
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        cross_swarm_needs = []
        blocked_swarms = []
        
        for swarm_id, state in swarm_states.items():
            emoji = "🟢" if state.status == "active" else "🟡" if state.status == "idle" else "🔴"
            
            report += f"""
{emoji} {swarm_id.upper()} 蜂群
├─ 状态: {state.status}
├─ 当前任务: {state.current_task or '无'}
├─ 队列长度: {state.task_queue_length}
├─ 能力覆盖: {', '.join(state.capabilities[:3])}...
└─ 最后心跳: {state.last_heartbeat}
"""
            
            if state.status == "blocked":
                blocked_swarms.append(swarm_id)
            
            # 检测跨蜂群协作需求 (简化逻辑)
            if state.task_queue_length > 5:
                cross_swarm_needs.append({
                    'swarm': swarm_id,
                    'need': '任务分流',
                    'description': f'{swarm_id} 队列积压，需要其他蜂群支援'
                })
        
        # 添加跨蜂群需求汇总
        if cross_swarm_needs:
            report += """
🤝 跨蜂群协作需求:
"""
            for need in cross_swarm_needs:
                report += f"├─ [{need['swarm']}] {need['need']}: {need['description']}\n"
        
        if blocked_swarms:
            report += f"""
🚨 阻塞告警: {', '.join(blocked_swarms)} 蜂群处于阻塞状态
   Innovation Agent已介入分析
"""
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
下次站会: 明天 NY 09:00
"""
        
        # 保存会议记录
        self._save_meeting('daily_standup', report)
        
        return report
    
    def ad_hoc_sync(self, task: Task, involved_swarms: List[str]) -> str:
        """专项协调会"""
        meeting_notes = f"""
🎯 专项协调会记录
任务: {task.name} ({task.id})
时间: {datetime.now().isoformat()}
参与蜂群: {', '.join(involved_swarms)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

议程:
1. 任务分解与分配
2. 依赖关系确认
3. 交付标准对齐
4. 进度同步机制

分配方案:
"""
        
        # 简化分配逻辑
        for i, swarm in enumerate(involved_swarms):
            meeting_notes += f"\n{i+1}. {swarm} 蜂群:\n"
            meeting_notes += f"   ├─ 负责: 任务模块 {i+1}\n"
            meeting_notes += f"   ├─ 依赖: {'无' if i == 0 else involved_swarms[i-1]}\n"
            meeting_notes += f"   └─ 交付: 待定\n"
        
        meeting_notes += """
同步机制:
├─ 每2小时进度汇报
├─ 阻塞立即升级
└─ 完成后通知Nexus
"""
        
        self._save_meeting('ad_hoc_sync', meeting_notes)
        return meeting_notes
    
    def _save_meeting(self, meeting_type: str, content: str):
        """保存会议记录"""
        record = {
            'type': meeting_type,
            'timestamp': datetime.now().isoformat(),
            'content': content
        }
        self.meeting_history.append(record)
        
        memory = self.memory._memory.get('meeting_minutes', [])
        memory.append(record)
        self.memory._memory['meeting_minutes'] = memory[-50:]  # 保留最近50条
        self.memory.save()

class SwarmNexusPMO:
    """
    蜂群项目管理中心 (PMO)
    核心职责：24/7监控、防遗漏、安全监督、协调、创新求解
    """
    
    def __init__(self):
        self.memory = GlobalMemoryHub()
        self.meeting_system = SwarmMeetingSystem(self.memory)
        self.innovation_agent = InnovationAgent(self.memory)
        self.registered_swarms = {}  # 注册的蜂群
        self.monitoring = False
        self.monitor_thread = None
        
        # 注册现有蜂群
        self._register_existing_swarms()
    
    def _register_existing_swarms(self):
        """注册现有蜂群"""
        existing_swarms = [
            {
                'id': 'evomap_swarm',
                'type': 'monetization',
                'capabilities': ['bounty_execution', 'capsule_validation', 'market_scanning', 'earnings_optimization']
            },
            {
                'id': 'investment_swarm', 
                'type': 'analysis',
                'capabilities': ['gold_analysis', 'usdc_analysis', 'fund_research', 'macro_analysis', 'briefing_generation']
            },
            {
                'id': 'opportunity_swarm',
                'type': 'research', 
                'capabilities': ['tech_scouting', 'pain_point_mining', 'trend_hunting', 'regulatory_scanning']
            },
            {
                'id': 'content_swarm',
                'type': 'production',
                'capabilities': ['trend_research', 'copywriting', 'visual_design', 'multi_platform_publishing']
            },
            {
                'id': 'system_swarm',
                'type': 'operations',
                'capabilities': ['security_monitoring', 'error_fixing', 'performance_optimization', 'daily_review']
            }
        ]
        
        for swarm_data in existing_swarms:
            self.register_swarm(swarm_data['id'], swarm_data['type'], swarm_data['capabilities'])
    
    def register_swarm(self, swarm_id: str, swarm_type: str, capabilities: List[str]):
        """注册蜂群到Nexus"""
        self.registered_swarms[swarm_id] = {
            'type': swarm_type,
            'capabilities': capabilities,
            'registered_at': datetime.now().isoformat()
        }
        
        # 初始化蜂群状态
        state = SwarmStatus(
            swarm_id=swarm_id,
            swarm_type=swarm_type,
            status='idle',
            capabilities=capabilities
        )
        self.memory.save_swarm_state(swarm_id, state)
        
        print(f"✅ 蜂群已注册: {swarm_id} ({swarm_type})")
    
    def create_project(self, name: str, description: str, tasks: List[Dict]) -> str:
        """创建新项目"""
        project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        project = {
            'id': project_id,
            'name': name,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'tasks': [],
            'swarms_involved': []
        }
        
        # 创建任务
        for task_data in tasks:
            task = Task(
                id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(project['tasks'])}",
                name=task_data['name'],
                description=task_data.get('description', ''),
                project_id=project_id,
                source='user',
                required_capabilities=task_data.get('required_capabilities', []),
                priority=task_data.get('priority', 3),
                deadline=task_data.get('deadline')
            )
            
            project['tasks'].append(task.id)
            self.memory.save_task(task)
            
            # 自动分配任务到蜂群
            self._auto_assign_task(task)
        
        self.memory.save_project(project_id, project)
        
        print(f"✅ 项目创建: {name} ({project_id})")
        print(f"   任务数: {len(tasks)}")
        
        return project_id
    
    def _auto_assign_task(self, task: Task):
        """自动分配任务到最合适的蜂群"""
        best_swarm = None
        best_score = 0
        
        for swarm_id, swarm_info in self.registered_swarms.items():
            # 计算匹配分数
            matching_caps = set(task.required_capabilities) & set(swarm_info['capabilities'])
            score = len(matching_caps) / len(task.required_capabilities) if task.required_capabilities else 0
            
            # 检查蜂群当前负载
            state = self.memory.get_swarm_states().get(swarm_id)
            if state and state.task_queue_length > 10:
                score *= 0.5  # 负载高，降低优先级
            
            if score > best_score:
                best_score = score
                best_swarm = swarm_id
        
        if best_swarm and best_score >= 0.5:
            task.assigned_swarm = best_swarm
            task.status = TaskStatus.ASSIGNED
            self.memory.save_task(task)
            print(f"   📋 任务分配: {task.name[:30]}... → {best_swarm} (匹配度: {best_score:.0%})")
        else:
            print(f"   ⚠️  任务未分配: {task.name[:30]}... (无匹配蜂群)")
            # 触发Innovation Agent
            self._trigger_innovation(task)
    
    def _trigger_innovation(self, task: Task):
        """触发创新求解"""
        problem = {
            'type': 'capability_gap',
            'description': f'没有蜂群能处理任务: {task.name}',
            'missing_capability': task.required_capabilities,
            'context': {'task': asdict(task)}
        }
        
        solution = self.innovation_agent.solve(problem)
        print(f"   🧠 Innovation Agent建议: {solution['recommended']['description']}")
    
    def start_monitoring(self):
        """启动24/7监控"""
        if self.monitoring:
            return
        
        self.monitoring = True
        
        print("🟢 Nexus 24/7监控已启动")
        print("   ├─ 每5分钟: 检查遗漏任务")
        print("   ├─ 每10分钟: 检查蜂群健康")
        print("   ├─ 每小时: 安全扫描")
        print("   └─ 每天09:00: 每日站会")
        
        # 启动监控线程
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _monitor_loop(self):
        """监控循环 - 纯Python实现，无外部依赖"""
        last_orphan_check = 0
        last_health_check = 0
        last_security_scan = 0
        last_standup = None
        
        while self.monitoring:
            now = time.time()
            current_hour = datetime.now().hour
            
            # 每5分钟检查遗漏任务
            if now - last_orphan_check >= 300:  # 300秒 = 5分钟
                self._check_orphaned_tasks()
                last_orphan_check = now
            
            # 每10分钟检查蜂群健康
            if now - last_health_check >= 600:  # 600秒 = 10分钟
                self._check_swarm_health()
                last_health_check = now
            
            # 每小时安全扫描
            if now - last_security_scan >= 3600:  # 3600秒 = 1小时
                self._security_scan()
                last_security_scan = now
            
            # 每天09:00站会
            today = datetime.now().strftime('%Y-%m-%d')
            if current_hour == 9 and last_standup != today:
                self._daily_standup()
                last_standup = today
            
            time.sleep(1)
    
    def _check_orphaned_tasks(self):
        """检查被遗忘的任务"""
        orphaned = self.memory.get_orphaned_tasks()
        
        if orphaned:
            print(f"\n⚠️  发现 {len(orphaned)} 个被遗忘的任务:")
            for task in orphaned:
                task.status = TaskStatus.ORPHANED
                self.memory.save_task(task)
                print(f"   - {task.name} (已闲置{(datetime.now() - datetime.fromisoformat(task.last_updated)).total_seconds()/3600:.1f}小时)")
                
                # 重新分配或触发创新
                self._auto_assign_task(task)
    
    def _check_swarm_health(self):
        """检查蜂群健康"""
        states = self.memory.get_swarm_states()
        now = datetime.now()
        
        for swarm_id, state in states.items():
            last_heartbeat = datetime.fromisoformat(state.last_heartbeat)
            minutes_since_heartbeat = (now - last_heartbeat).total_seconds() / 60
            
            if minutes_since_heartbeat > 30:
                print(f"\n🚨 蜂群失联: {swarm_id} (已{minutes_since_heartbeat:.0f}分钟无心跳)")
                # 触发恢复流程
                self._recover_swarm(swarm_id)
    
    def _recover_swarm(self, swarm_id: str):
        """恢复蜂群"""
        print(f"   🔄 尝试恢复 {swarm_id}...")
        # 简化的恢复逻辑
        state = self.memory.get_swarm_states().get(swarm_id)
        if state:
            state.status = 'recovering'
            self.memory.save_swarm_state(swarm_id, state)
    
    def _security_scan(self):
        """安全扫描"""
        # 简化的安全扫描
        alerts = self.memory.get_open_alerts()
        critical_alerts = [a for a in alerts if a.level == RiskLevel.CRITICAL]
        
        if critical_alerts:
            print(f"\n🔴 关键安全告警: {len(critical_alerts)} 个")
            for alert in critical_alerts:
                print(f"   - [{alert.category}] {alert.description}")
    
    def _daily_standup(self):
        """执行每日站会"""
        states = self.memory.get_swarm_states()
        report = self.meeting_system.daily_standup(states)
        print(report)
        
        # 保存到文件
        report_file = NEXUS_DIR / f"standup_{datetime.now().strftime('%Y%m%d')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def get_sync_board(self) -> str:
        """获取同步看板"""
        states = self.memory.get_swarm_states()
        tasks = self.memory.get_all_tasks()
        
        board = """
┌─────────────────────────────────────────────────────────────────┐
│                    SWARM NEXUS SYNC BOARD                        │
│                    实时同步看板 - {time:<20}      │
├─────────────────────────────────────────────────────────────────┤
""".format(time=datetime.now().strftime('%Y-%m-%d %H:%M NY'))
        
        # 蜂群状态
        for swarm_id, state in states.items():
            emoji = "🟢" if state.status == "active" else "🟡" if state.status == "idle" else "🔴" if state.status == "blocked" else "⚪"
            progress_int = int(state.performance_score * 10)
            progress_bar = "█" * progress_int + "░" * (10 - progress_int)
            
            board += f"""
│ {emoji} {swarm_id:<15} 
│    状态: {state.status:<10} | 任务队列: {state.task_queue_length:<3} | 性能: {progress_bar}
│    当前: {state.current_task or '空闲':<30}
"""
        
        # 任务统计
        pending = len([t for t in tasks if t.status == TaskStatus.PENDING])
        in_progress = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
        blocked = len([t for t in tasks if t.status == TaskStatus.BLOCKED])
        orphaned = len([t for t in tasks if t.status == TaskStatus.ORPHANED])
        
        board += f"""
├─────────────────────────────────────────────────────────────────┤
│ 📊 任务统计: 待分配 {pending} | 进行中 {in_progress} | 阻塞 {blocked} | 遗忘 {orphaned}
"""
        
        # 告警
        if orphaned > 0:
            board += f"│ 🚨 告警: {orphaned} 个任务被遗忘，已触发重新分配\n"
        
        alerts = self.memory.get_open_alerts()
        if alerts:
            critical = len([a for a in alerts if a.level == RiskLevel.CRITICAL])
            if critical > 0:
                board += f"│ 🔴 安全: {critical} 个关键告警待处理\n"
        
        board += """└─────────────────────────────────────────────────────────────────┘
"""
        return board
    
    def request_ad_hoc_sync(self, task_id: str) -> str:
        """请求专项协调会"""
        task = self.memory.get_task(task_id)
        if not task:
            return f"❌ 任务不存在: {task_id}"
        
        # 识别相关蜂群
        involved = [task.assigned_swarm] if task.assigned_swarm else []
        
        # 如果有依赖，也加入
        for dep_id in task.dependencies:
            dep_task = self.memory.get_task(dep_id)
            if dep_task and dep_task.assigned_swarm:
                if dep_task.assigned_swarm not in involved:
                    involved.append(dep_task.assigned_swarm)
        
        if len(involved) > 1:
            meeting_notes = self.meeting_system.ad_hoc_sync(task, involved)
            return meeting_notes
        else:
            return f"⚠️  任务 {task_id} 只需要单蜂群处理，无需协调会"

# CLI入口
def main():
    """命令行入口"""
    import sys
    
    nexus = SwarmNexusPMO()
    
    if len(sys.argv) < 2:
        print("Swarm Nexus PMO - 蜂群项目管理中心")
        print("\n用法:")
        print("  python3 nexus_core.py start       # 启动24/7监控")
        print("  python3 nexus_core.py board       # 显示同步看板")
        print("  python3 nexus_core.py project     # 创建示例项目")
        print("  python3 nexus_core.py standup     # 手动触发站会")
        print("  python3 nexus_core.py status      # 查看所有状态")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "start":
        nexus.start_monitoring()
        print("\n按 Ctrl+C 停止监控")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            nexus.monitoring = False
            print("\n🛑 监控已停止")
    
    elif cmd == "board":
        print(nexus.get_sync_board())
    
    elif cmd == "project":
        # 创建示例项目
        tasks = [
            {
                'name': '研究Anthropic Agent Teams',
                'description': '深度分析最新多智能体框架',
                'required_capabilities': ['tech_scouting', 'research'],
                'priority': 2
            },
            {
                'name': '撰写分析文章',
                'description': '基于研究结果撰写发布内容',
                'required_capabilities': ['copywriting', 'multi_platform_publishing'],
                'priority': 2
            }
        ]
        project_id = nexus.create_project(
            name="Anthropic Agent Teams研究",
            description="研究并发布关于Anthropic Agent Teams的深度分析",
            tasks=tasks
        )
        print(f"\n项目已创建: {project_id}")
    
    elif cmd == "standup":
        nexus._daily_standup()
    
    elif cmd == "status":
        print(nexus.get_sync_board())
        print("\n📋 最近任务:")
        for task in nexus.memory.get_all_tasks()[-5:]:
            print(f"   [{task.status.value}] {task.name[:40]}...")
    
    else:
        print(f"❌ 未知命令: {cmd}")

if __name__ == "__main__":
    main()
