#!/usr/bin/env python3
"""
Example: Full Orchestrator Integration with GPU Knowledge

Shows how to integrate GPU knowledge into a complete orchestration system.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gpu_knowledge import AgentKnowledgeInterface, SharedGPUKnowledgeBase


class GPUExpertAgent:
    """Agent with GPU expertise"""

    def __init__(self, agent_id: int, role: str):
        self.agent_id = agent_id
        self.role = role
        self.gpu_knowledge = AgentKnowledgeInterface(agent_id)
        self.tasks_completed = 0

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using GPU knowledge"""

        if task['type'] == 'kernel_optimization':
            return self._optimize_kernel(task)
        elif task['type'] == 'memory_analysis':
            return self._analyze_memory(task)
        elif task['type'] == 'performance_tuning':
            return self._tune_performance(task)
        else:
            return {'status': 'unknown_task_type'}

    def _optimize_kernel(self, task: Dict) -> Dict:
        """Optimize kernel code"""
        hopper = self.gpu_knowledge.ask("hopper_sota_matmul")
        perf = hopper['performance_progression']

        self.tasks_completed += 1
        return {
            'status': 'optimized',
            'agent_id': self.agent_id,
            'agent_role': self.role,
            'target_performance': perf['stmatrix_optimization'],
            'techniques': ['TMA', 'Tensor Cores', 'Hilbert Curves']
        }

    def _analyze_memory(self, task: Dict) -> Dict:
        """Analyze memory layout"""
        memory = self.gpu_knowledge.ask("memory_subsystem_deep_dive")
        bank_conflicts = memory['smem_sram_model']['bank_conflicts']

        self.tasks_completed += 1
        return {
            'status': 'analyzed',
            'agent_id': self.agent_id,
            'agent_role': self.role,
            'recommendations': bank_conflicts['solutions'],
            'expected_speedup': '32x max from avoiding conflicts'
        }

    def _tune_performance(self, task: Dict) -> Dict:
        """Tune performance"""
        scheduling = self.gpu_knowledge.ask("scheduling_strategies")

        self.tasks_completed += 1
        return {
            'status': 'tuned',
            'agent_id': self.agent_id,
            'agent_role': self.role,
            'strategy': 'hilbert_curve',
            'improvement': scheduling['hilbert_curve_schedule']['performance_gain']
        }


class MultiAgentOrchestrator:
    """
    Orchestrator managing multiple GPU-expert agents
    """

    def __init__(self, num_agents: int = 10):
        print(f"\n{'='*70}")
        print(f"INITIALIZING ORCHESTRATOR WITH {num_agents} GPU-EXPERT AGENTS")
        print(f"{'='*70}\n")

        # Initialize shared knowledge base
        self.kb = SharedGPUKnowledgeBase()
        self.kb.load_knowledge_base(
            str(Path(__file__).parent.parent / "gpu_knowledge" / "gpu_knowledge_from_pdf.pkl")
        )
        print("✅ GPU knowledge base loaded")

        # Create specialized agent team
        self.agents = self._create_agent_team(num_agents)
        print(f"✅ Created {len(self.agents)} specialized agents")

        # Task queue
        self.task_queue = []
        self.completed_tasks = []

        self._print_team_composition()

    def _create_agent_team(self, num_agents: int) -> List[GPUExpertAgent]:
        """Create team of specialized agents"""
        agents = []

        # Define specializations
        roles = ['kernel_optimizer', 'memory_specialist', 'performance_tuner']

        for i in range(num_agents):
            role = roles[i % len(roles)]
            agent = GPUExpertAgent(agent_id=i, role=role)
            agents.append(agent)

        return agents

    def _print_team_composition(self):
        """Print team composition"""
        role_counts = {}
        for agent in self.agents:
            role_counts[agent.role] = role_counts.get(agent.role, 0) + 1

        print("\n📊 Team Composition:")
        for role, count in role_counts.items():
            print(f"   {role}: {count} agents")

    def add_task(self, task: Dict[str, Any]):
        """Add task to queue"""
        self.task_queue.append(task)

    def execute_tasks(self):
        """Execute all queued tasks"""
        print(f"\n{'='*70}")
        print(f"EXECUTING {len(self.task_queue)} TASKS")
        print(f"{'='*70}\n")

        while self.task_queue:
            task = self.task_queue.pop(0)
            agent = self._select_agent(task)

            print(f"Task {len(self.completed_tasks)+1}: {task['type']}")
            print(f"  Assigned to: Agent {agent.agent_id} ({agent.role})")

            result = agent.execute_task(task)

            print(f"  Status: {result['status']}")
            if 'target_performance' in result:
                print(f"  Target: {result['target_performance']}")

            self.completed_tasks.append({
                'task': task,
                'result': result,
                'agent_id': agent.agent_id
            })

            print()

    def _select_agent(self, task: Dict) -> GPUExpertAgent:
        """Select best agent for task"""
        # Simple role-based selection
        preferred_roles = {
            'kernel_optimization': 'kernel_optimizer',
            'memory_analysis': 'memory_specialist',
            'performance_tuning': 'performance_tuner'
        }

        preferred_role = preferred_roles.get(task['type'])

        # Find agent with matching role and lowest workload
        matching_agents = [a for a in self.agents if a.role == preferred_role]
        if matching_agents:
            return min(matching_agents, key=lambda a: a.tasks_completed)

        # Fallback to least busy agent
        return min(self.agents, key=lambda a: a.tasks_completed)

    def get_statistics(self) -> Dict:
        """Get orchestration statistics"""
        stats = self.kb.get_agent_statistics()

        return {
            'total_agents': len(self.agents),
            'tasks_completed': len(self.completed_tasks),
            'knowledge_queries': stats['total_queries'],
            'active_agents': stats['unique_agents'],
            'agent_workload': {
                agent.agent_id: agent.tasks_completed
                for agent in self.agents
                if agent.tasks_completed > 0
            }
        }

    def print_summary(self):
        """Print execution summary"""
        stats = self.get_statistics()

        print(f"\n{'='*70}")
        print("ORCHESTRATION SUMMARY")
        print(f"{'='*70}")
        print(f"\n📊 Statistics:")
        print(f"   Total agents: {stats['total_agents']}")
        print(f"   Tasks completed: {stats['tasks_completed']}")
        print(f"   GPU knowledge queries: {stats['knowledge_queries']}")
        print(f"   Active agents: {stats['active_agents']}")

        print(f"\n💼 Agent Workload:")
        for agent_id, count in sorted(stats['agent_workload'].items())[:5]:
            agent = self.agents[agent_id]
            print(f"   Agent {agent_id} ({agent.role}): {count} tasks")

        print(f"\n{'='*70}")


def main():
    """Demo the orchestrator"""

    # Create orchestrator with 10 agents
    orchestrator = MultiAgentOrchestrator(num_agents=10)

    # Add various tasks
    tasks = [
        {'type': 'kernel_optimization', 'code': 'matmul.cu'},
        {'type': 'memory_analysis', 'structure': 'shared_memory'},
        {'type': 'performance_tuning', 'metric': 'throughput'},
        {'type': 'kernel_optimization', 'code': 'convolution.cu'},
        {'type': 'memory_analysis', 'structure': 'global_memory'},
        {'type': 'performance_tuning', 'metric': 'latency'},
    ]

    print(f"\n📋 Adding {len(tasks)} tasks to queue...")
    for task in tasks:
        orchestrator.add_task(task)

    # Execute all tasks
    orchestrator.execute_tasks()

    # Print summary
    orchestrator.print_summary()

    print("\n✅ Orchestrator successfully managed all tasks using GPU expertise!")


if __name__ == "__main__":
    main()
