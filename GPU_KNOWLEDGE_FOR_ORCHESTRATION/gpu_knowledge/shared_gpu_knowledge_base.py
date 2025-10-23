"""
Shared GPU Knowledge Base for 102-Agent Team

Centralized knowledge repository that all agents can query for
deep GPU technical expertise from "Inside NVIDIA GPUs"
"""

import json
import pickle
from typing import Dict, List, Any, Optional
from pathlib import Path
import threading


class SharedGPUKnowledgeBase:
    """
    Thread-safe centralized knowledge base accessible by all 102 agents

    Knowledge sources:
    - Inside NVIDIA GPUs PDF
    - CUDA Programming Guides
    - Architecture Whitepapers
    - Optimization Best Practices
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton pattern - all agents share same knowledge base"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.knowledge = self._initialize_knowledge_base()
            self.pdf_extracted_knowledge = {}
            self.agent_queries = []  # Track what agents are asking
            self.initialized = True

    def _initialize_knowledge_base(self) -> Dict:
        """
        Initialize comprehensive GPU knowledge base

        This will be enhanced with PDF content
        """
        return {
            "gpu_architectures": {
                "ampere": {
                    "compute_capability": "8.x",
                    "key_features": [
                        "3rd generation Tensor Cores",
                        "Structural sparsity support",
                        "TF32 precision for AI",
                        "MIG (Multi-Instance GPU)",
                        "PCIe Gen 4 support"
                    ],
                    "sm_count": {
                        "A100": 108,
                        "A10": 72,
                        "RTX 3090": 82
                    },
                    "tensor_core_improvements": "2x FP16 throughput, INT8/INT4 support",
                    "memory_improvements": "Up to 40MB L2 cache, memory compression"
                },
                "hopper": {
                    "compute_capability": "9.x",
                    "key_features": [
                        "4th generation Tensor Cores",
                        "Transformer Engine",
                        "Thread Block Clusters",
                        "Asynchronous execution",
                        "FP8 precision support"
                    ],
                    "sm_count": {
                        "H100": 132
                    },
                    "revolutionary_features": [
                        "DPX instructions for dynamic programming",
                        "Distributed shared memory",
                        "Tensor Memory Accelerator (TMA)",
                        "Thread block clusters (new level in hierarchy)"
                    ]
                },
                "ada_lovelace": {
                    "compute_capability": "8.9",
                    "key_features": [
                        "3rd gen RT Cores",
                        "4th gen Tensor Cores",
                        "DLSS 3",
                        "Shader Execution Reordering",
                        "Opacity Micromap Engine"
                    ],
                    "gaming_optimizations": True
                }
            },

            "deep_technical_details": {
                "warp_scheduler": {
                    "warp_size": 32,
                    "scheduling_policy": "Round-robin with priority",
                    "latency_hiding": {
                        "mechanism": "Switch to ready warp when current stalls",
                        "zero_overhead": "Warp context always resident",
                        "requirement": "Need 4-8 warps per SM for full utilization"
                    },
                    "instruction_issue": {
                        "dual_issue": "Some architectures can issue 2 independent instructions",
                        "throughput": "1 instruction per warp per cycle (typical)",
                        "dependencies": "RAW/WAW/WAR hazards cause stalls"
                    }
                },

                "memory_subsystem": {
                    "registers": {
                        "organization": "Partitioned across thread scheduler blocks",
                        "max_per_thread": 255,
                        "total_per_sm": "65536 (varies by architecture)",
                        "register_file": {
                            "banks": "Multiple banks for parallel access",
                            "width": "32-bit",
                            "allocation": "At kernel launch, granularity = 256 registers"
                        },
                        "spilling": {
                            "trigger": "Exceeds hardware limit or compiler limit",
                            "destination": "Local memory (cached in L1/L2)",
                            "performance_impact": "Severe - 100-200 cycle penalty"
                        }
                    },

                    "shared_memory": {
                        "architecture": "On-chip SRAM",
                        "access_time": "~30 cycles",
                        "banks": 32,
                        "bank_width": "4 bytes",
                        "bank_conflict_details": {
                            "definition": "Multiple threads access different addresses in same bank",
                            "serialization": "N-way conflict = N serial accesses",
                            "broadcast": "All threads same address = no conflict",
                            "detection": "Nsight Compute shows shared_ld/st_bank_conflict",
                            "solution_strategies": [
                                "Padding arrays to avoid conflicts",
                                "Swizzling access patterns",
                                "Using different data layouts"
                            ]
                        },
                        "configuration": {
                            "trade_off": "Shared memory vs L1 cache size",
                            "options": "cudaFuncSetCacheConfig",
                            "sizes": "16/32/48/64/100KB depending on arch"
                        }
                    },

                    "cache_hierarchy": {
                        "l1_cache": {
                            "size": "32-128 KB per SM",
                            "line_size": "128 bytes",
                            "associativity": "Direct-mapped or set-associative",
                            "policy": "Cache most recent access",
                            "cache_control": {
                                "ldg": "Read-only cache (texture cache)",
                                "ldu": "Bypass L1",
                                "default": "Use L1"
                            }
                        },
                        "l2_cache": {
                            "size": "1.5 - 40 MB (architecture dependent)",
                            "line_size": "128 bytes",
                            "shared_across": "All SMs",
                            "persistence": {
                                "access_policy": "Can set persisting vs streaming",
                                "l2_policy_window": "Control what stays in L2",
                                "use_case": "Keep frequently accessed data in L2"
                            }
                        },
                        "texture_cache": {
                            "optimization": "2D spatial locality",
                            "filtering": "Hardware interpolation",
                            "use_cases": "Image processing, read-only random access"
                        }
                    },

                    "global_memory": {
                        "dram_type": "GDDR6/GDDR6X/HBM2/HBM2e",
                        "bus_width": "384-5120 bits",
                        "access_granularity": "32-byte segment per thread",
                        "coalescing": {
                            "definition": "Multiple thread accesses combined into fewer transactions",
                            "requirements": {
                                "alignment": "Access naturally aligned addresses",
                                "contiguity": "Threads N access address[N]",
                                "segment": "All accesses within 32B aligned segment"
                            },
                            "best_case": "32 threads → 1 transaction (128 bytes)",
                            "worst_case": "32 threads → 32 transactions",
                            "detection": "gld/st_efficiency metric in profiler"
                        },
                        "atomic_operations": {
                            "location": "Can execute in L2 cache",
                            "serialization": "Serialize on same address",
                            "performance": "Much faster in L2 than DRAM",
                            "types": "Add, Min, Max, CAS, Exchange, etc."
                        }
                    }
                },

                "execution_model": {
                    "simt": {
                        "definition": "Single Instruction Multiple Thread",
                        "vs_simd": "Each thread has own PC and register state",
                        "reconvergence": "Diverged threads reconverge at immediate post-dominator",
                        "predication": {
                            "mechanism": "All threads execute, results conditionally written",
                            "benefit": "Avoid branch for simple conditionals",
                            "cost": "Execute all paths"
                        }
                    },

                    "divergence": {
                        "causes": [
                            "if/else with different paths in warp",
                            "Loops with thread-dependent iteration count",
                            "Function calls with thread-dependent targets"
                        ],
                        "impact": "Serialize execution of divergent paths",
                        "measurement": "branch_efficiency metric",
                        "mitigation": [
                            "Organize data so threads in warp take same path",
                            "Use warp-level primitives (__ballot, __any, __all)",
                            "Partition work to separate warps"
                        ]
                    },

                    "synchronization": {
                        "block_level": {
                            "__syncthreads()": "Barrier for all threads in block",
                            "__syncwarp()": "Barrier for threads in warp",
                            "memory_fence": "__threadfence() for memory ordering"
                        },
                        "grid_level": {
                            "kernel_boundary": "Implicit synchronization between kernels",
                            "cooperative_groups": "Explicit grid-wide synchronization",
                            "requirements": "Must know max blocks at compile time"
                        },
                        "pitfalls": [
                            "Conditional __syncthreads() = deadlock",
                            "Assuming threads execute in lockstep",
                            "Missing memory fence with atomic operations"
                        ]
                    }
                },

                "performance_characteristics": {
                    "instruction_throughput": {
                        "fp32": "2x CUDA cores/SM operations per cycle",
                        "fp64": "1/2 to 1/32 of FP32 rate (architecture dependent)",
                        "int32": "Same as FP32",
                        "special_functions": "1/4 rate (sin, cos, log, etc.)",
                        "tensor_cores": "8x to 16x FP32 throughput for matrix ops"
                    },

                    "memory_bandwidth": {
                        "theoretical": "Memory clock × bus width ÷ 8",
                        "hbm2": "Up to 2 TB/s (H100)",
                        "gddr6x": "Up to 1 TB/s (RTX 4090)",
                        "achievable": "80-90% of theoretical is excellent",
                        "bottleneck": "Often the limiting factor in kernels"
                    },

                    "occupancy": {
                        "definition": "Active warps / maximum possible warps per SM",
                        "factors": {
                            "registers": "Limited by register file size",
                            "shared_memory": "Limited by shared memory size",
                            "block_size": "Too small = low occupancy",
                            "blocks_per_sm": "Hardware limit (16-32)"
                        },
                        "myth": "100% occupancy not always optimal",
                        "reality": "Trade-off between occupancy and per-thread resources",
                        "tools": "CUDA Occupancy Calculator, Nsight Compute"
                    }
                }
            },

            "optimization_patterns": {
                "memory_bound_kernels": {
                    "characteristics": "Memory time >> Compute time",
                    "strategies": [
                        "Improve coalescing",
                        "Use shared memory for reuse",
                        "Increase arithmetic intensity",
                        "Use vector loads (float4, etc.)",
                        "Compress data if possible"
                    ],
                    "profiling": "Look at memory throughput vs peak"
                },

                "compute_bound_kernels": {
                    "characteristics": "Compute time >> Memory time",
                    "strategies": [
                        "Already well optimized for memory",
                        "Use tensor cores if applicable",
                        "Use fast math",
                        "Algorithmic improvements",
                        "Consider mixed precision"
                    ],
                    "profiling": "Look at achieved_occupancy and instruction mix"
                },

                "latency_bound_kernels": {
                    "characteristics": "Low occupancy, frequent stalls",
                    "strategies": [
                        "Increase occupancy",
                        "Reduce register usage",
                        "Reduce shared memory usage",
                        "Increase block size",
                        "Use asynchronous operations"
                    ],
                    "profiling": "Look at stall reasons in Nsight"
                }
            },

            "cuda_best_practices": {
                "kernel_design": [
                    "Maximize parallel work - expose all parallelism",
                    "Minimize divergence - organize data for uniform control flow",
                    "Coalesce memory access - structure for sequential access",
                    "Optimize for occupancy - balance resources vs parallelism",
                    "Use shared memory - exploit data reuse"
                ],

                "memory_management": [
                    "Minimize transfers - keep data on GPU",
                    "Use pinned memory - 2x faster than pageable",
                    "Overlap transfer and compute - use streams",
                    "Batch operations - amortize overhead",
                    "Consider unified memory - easier development, profile first"
                ],

                "algorithm_selection": [
                    "GPU-friendly algorithms - prefer data parallel",
                    "Tiling - improve data reuse",
                    "Reduce synchronization - expensive operation",
                    "Persistent threads - keep GPU busy",
                    "Use libraries - cuBLAS, cuDNN, etc. are highly optimized"
                ]
            }
        }

    def add_pdf_knowledge(self, category: str, content: Dict):
        """
        Add extracted knowledge from PDF

        Args:
            category: Knowledge category (e.g., 'architecture', 'optimization')
            content: Detailed knowledge extracted from PDF
        """
        with self._lock:
            if category not in self.pdf_extracted_knowledge:
                self.pdf_extracted_knowledge[category] = []
            self.pdf_extracted_knowledge[category].append(content)

    def query(self, query: str, agent_id: Optional[int] = None) -> Any:
        """
        Query knowledge base

        Args:
            query: Query string (e.g., 'memory.shared_memory.bank_conflict_details')
            agent_id: ID of agent making query (for tracking)

        Returns:
            Knowledge matching query
        """
        # Track query for analytics
        if agent_id is not None:
            self.agent_queries.append({"agent_id": agent_id, "query": query})

        # Parse query path
        parts = query.lower().split('.')
        result = self.knowledge

        for part in parts:
            if isinstance(result, dict) and part in result:
                result = result[part]
            else:
                # Search in PDF knowledge if not in base knowledge
                return self._search_pdf_knowledge(query)

        return result

    def _search_pdf_knowledge(self, query: str) -> Any:
        """Search in PDF-extracted knowledge"""
        query_lower = query.lower()
        matches = []

        for category, contents in self.pdf_extracted_knowledge.items():
            for content in contents:
                if self._matches_query(content, query_lower):
                    matches.append({
                        "category": category,
                        "content": content
                    })

        return matches if matches else "No matching knowledge found"

    def _matches_query(self, content: Any, query: str) -> bool:
        """Check if content matches query"""
        content_str = json.dumps(content).lower()
        return query in content_str

    def get_agent_statistics(self) -> Dict:
        """Get statistics about agent knowledge usage"""
        query_count = {}
        for q in self.agent_queries:
            aid = q["agent_id"]
            query_count[aid] = query_count.get(aid, 0) + 1

        return {
            "total_queries": len(self.agent_queries),
            "unique_agents": len(query_count),
            "queries_per_agent": query_count,
            "knowledge_categories": len(self.knowledge),
            "pdf_knowledge_categories": len(self.pdf_extracted_knowledge)
        }

    def save_knowledge_base(self, filepath: str = "gpu_knowledge_base.pkl"):
        """Save knowledge base to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'knowledge': self.knowledge,
                'pdf_knowledge': self.pdf_extracted_knowledge
            }, f)
        print(f"Knowledge base saved to {filepath}")

    def load_knowledge_base(self, filepath: str = "gpu_knowledge_base.pkl"):
        """Load knowledge base from disk"""
        if Path(filepath).exists():
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.knowledge.update(data['knowledge'])
                self.pdf_extracted_knowledge.update(data['pdf_knowledge'])
            print(f"Knowledge base loaded from {filepath}")
        else:
            print(f"No saved knowledge base found at {filepath}")


class AgentKnowledgeInterface:
    """
    Interface for agents to access shared knowledge base
    """

    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        self.kb = SharedGPUKnowledgeBase()

    def ask(self, question: str) -> Any:
        """
        Ask the knowledge base a question

        Example:
            answer = agent.ask("deep_technical_details.warp_scheduler")
        """
        return self.kb.query(question, self.agent_id)

    def get_optimization_for(self, algorithm: str) -> List[str]:
        """Get optimization strategies for specific algorithm"""
        return self.kb.query(f"optimization_patterns.{algorithm}")

    def get_architecture_detail(self, arch: str, detail: str) -> Any:
        """Get specific architecture details"""
        return self.kb.query(f"gpu_architectures.{arch}.{detail}")

    def get_best_practice(self, category: str) -> List[str]:
        """Get CUDA best practices"""
        return self.kb.query(f"cuda_best_practices.{category}")


# Example usage for 102-agent team
if __name__ == "__main__":
    print("="*70)
    print("SHARED GPU KNOWLEDGE BASE FOR 102-AGENT TEAM")
    print("="*70)

    # Simulate multiple agents accessing knowledge
    agents = [AgentKnowledgeInterface(agent_id=i) for i in range(1, 11)]  # First 10 of 102

    # Agent 1 queries warp scheduler details
    print("\n[Agent 1] Querying warp scheduler details...")
    warp_info = agents[0].ask("deep_technical_details.warp_scheduler.latency_hiding")
    print(json.dumps(warp_info, indent=2))

    # Agent 5 queries bank conflict information
    print("\n[Agent 5] Querying shared memory bank conflicts...")
    bank_info = agents[4].ask("deep_technical_details.memory_subsystem.shared_memory.bank_conflict_details")
    print(json.dumps(bank_info, indent=2))

    # Agent 7 gets optimization strategies
    print("\n[Agent 7] Getting memory-bound kernel optimizations...")
    optimizations = agents[6].ask("optimization_patterns.memory_bound_kernels.strategies")
    for i, opt in enumerate(optimizations, 1):
        print(f"  {i}. {opt}")

    # Check knowledge base statistics
    print("\n" + "="*70)
    print("KNOWLEDGE BASE STATISTICS")
    print("="*70)
    kb = SharedGPUKnowledgeBase()
    stats = kb.get_agent_statistics()
    print(json.dumps(stats, indent=2))

    print("\n✅ All 102 agents can now access this shared GPU knowledge base!")
    print("📚 Knowledge will be enhanced with PDF content from 'Inside NVIDIA GPUs'")
