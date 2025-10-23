#!/usr/bin/env python3
"""
Example: Basic Agent Integration with GPU Knowledge

Shows the simplest way to add GPU expertise to a single agent.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gpu_knowledge import AgentKnowledgeInterface


class BasicGPUAgent:
    """
    Simple agent with GPU knowledge integration
    """

    def __init__(self, agent_id: int):
        self.agent_id = agent_id

        # ✨ Add GPU knowledge - just one line!
        self.gpu_knowledge = AgentKnowledgeInterface(agent_id)

    def optimize_kernel(self, kernel_code: str) -> dict:
        """
        Optimize GPU kernel using expert knowledge
        """
        print(f"\n[Agent {self.agent_id}] Optimizing kernel...")

        # Query TMA knowledge
        tma = self.gpu_knowledge.ask("tma_tensor_memory_accelerator")
        print(f"  Using TMA: {tma['purpose']}")

        # Query swizzling patterns
        swizzle = self.gpu_knowledge.ask("swizzling_deep_dive")
        print(f"  Swizzle modes available: {list(swizzle['swizzle_modes'].keys())}")

        # Query optimization strategies
        hopper = self.gpu_knowledge.ask("hopper_sota_matmul")
        final_perf = hopper['performance_progression']['stmatrix_optimization']
        print(f"  Target performance: {final_perf}")

        return {
            'status': 'optimized',
            'techniques_applied': ['TMA', 'Swizzling', 'Tensor Cores'],
            'expected_performance': final_perf
        }

    def analyze_memory_layout(self, data_structure: str) -> dict:
        """
        Analyze and recommend memory layout
        """
        print(f"\n[Agent {self.agent_id}] Analyzing memory layout...")

        # Get bank conflict information
        bank_conflicts = self.gpu_knowledge.ask(
            "memory_subsystem_deep_dive.smem_sram_model.bank_conflicts"
        )
        print(f"  Bank conflict impact: {bank_conflicts['impact']}")

        # Get coalescing information
        coalescing = self.gpu_knowledge.ask(
            "memory_subsystem_deep_dive.gmem_dram_model.access_pattern_impact"
        )
        print(f"  Coalescing performance impact: {coalescing['performance_impact']}")

        return {
            'recommended_swizzle': '128B',
            'bank_conflicts_avoided': True,
            'coalesced_access': True,
            'expected_speedup': '13x from coalescing'
        }

    def get_architecture_recommendations(self, gpu_type: str = "hopper") -> dict:
        """
        Get architecture-specific recommendations
        """
        print(f"\n[Agent {self.agent_id}] Getting {gpu_type} recommendations...")

        # Query architecture details
        if gpu_type.lower() == "hopper":
            arch = self.gpu_knowledge.ask("gpu_architecture_fundamentals")
            h100 = arch['h100_specifics']

            print(f"  GPU: H100 with {h100['total_sms']} SMs")
            print(f"  GPCs: {h100['gpcs']}")

            return {
                'architecture': 'Hopper H100',
                'sms': h100['total_sms'],
                'gpcs': h100['gpcs'],
                'features': ['TMA', 'Tensor Cores', 'DSMEM', 'Clusters']
            }

        return {'architecture': 'Unknown'}


def main():
    """Demo the basic agent"""

    print("="*70)
    print("BASIC AGENT INTEGRATION DEMO")
    print("="*70)

    # Create agent
    agent = BasicGPUAgent(agent_id=1)

    # Demo 1: Optimize kernel
    result = agent.optimize_kernel("matmul_kernel.cu")
    print(f"\nOptimization Result:")
    for key, value in result.items():
        print(f"  {key}: {value}")

    # Demo 2: Analyze memory layout
    layout = agent.analyze_memory_layout("shared_memory_tile")
    print(f"\nMemory Layout Analysis:")
    for key, value in layout.items():
        print(f"  {key}: {value}")

    # Demo 3: Get architecture recommendations
    recs = agent.get_architecture_recommendations("hopper")
    print(f"\nArchitecture Recommendations:")
    for key, value in recs.items():
        print(f"  {key}: {value}")

    print("\n" + "="*70)
    print("✅ Agent successfully used GPU knowledge for all tasks!")
    print("="*70)


if __name__ == "__main__":
    main()
