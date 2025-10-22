"""
GPU Expert AI Agent - Deep Technical Knowledge System

This agent has comprehensive knowledge of NVIDIA GPU architecture,
CUDA programming, and optimization techniques.

Built for: GPU Optimization Startup AI Agent Team
"""

class GPUExpertAgent:
    """
    AI Agent with deep NVIDIA GPU technical expertise

    Knowledge Areas:
    - GPU Architecture (Streaming Multiprocessors, Warps, Threads)
    - Memory Hierarchy (Registers, Shared, L1/L2, Global, Texture)
    - CUDA Programming Model
    - Performance Optimization Techniques
    - Compute Capabilities
    - Tensor Cores, RT Cores
    """

    def __init__(self):
        self.knowledge_base = self._initialize_gpu_knowledge()
        self.optimization_strategies = self._load_optimization_strategies()

    def _initialize_gpu_knowledge(self):
        """
        Comprehensive GPU architecture knowledge base
        """
        return {
            "architecture": {
                "streaming_multiprocessor": {
                    "description": "Core processing unit in NVIDIA GPUs",
                    "components": [
                        "CUDA cores (FP32/FP64 units)",
                        "Tensor cores (mixed precision matrix ops)",
                        "RT cores (ray tracing acceleration)",
                        "Load/Store units",
                        "Special Function Units (SFU)",
                        "Warp schedulers",
                        "Dispatch units"
                    ],
                    "execution_model": {
                        "warp_size": 32,
                        "max_threads_per_sm": "varies by architecture (1024-2048)",
                        "max_blocks_per_sm": "16-32 depending on generation",
                        "warp_scheduling": "Zero-overhead context switching"
                    }
                },
                "memory_hierarchy": {
                    "registers": {
                        "scope": "per-thread",
                        "speed": "fastest",
                        "size": "limited (255 per thread max)",
                        "latency": "~1 cycle",
                        "optimization": "Register spilling to local memory reduces performance"
                    },
                    "shared_memory": {
                        "scope": "per-block",
                        "speed": "very fast",
                        "size": "48-164 KB per SM (configurable with L1)",
                        "latency": "~30 cycles",
                        "access_pattern": "Bank conflicts can reduce performance",
                        "num_banks": 32,
                        "optimization": "Avoid bank conflicts, use padding if necessary"
                    },
                    "l1_cache": {
                        "scope": "per-SM",
                        "size": "configurable with shared memory",
                        "latency": "~30 cycles",
                        "type": "hardware managed"
                    },
                    "l2_cache": {
                        "scope": "global (all SMs)",
                        "size": "3-40 MB depending on GPU",
                        "latency": "~200 cycles",
                        "optimization": "Locality and coalescing critical"
                    },
                    "global_memory": {
                        "scope": "device-wide",
                        "size": "GB range (8-80 GB typical)",
                        "latency": "400-800 cycles",
                        "bandwidth": "100-2000 GB/s depending on GPU",
                        "optimization": {
                            "coalescing": "Adjacent threads should access adjacent memory",
                            "alignment": "128-byte cache line alignment preferred",
                            "patterns": "Sequential access patterns maximize bandwidth"
                        }
                    },
                    "constant_memory": {
                        "size": "64 KB",
                        "cached": True,
                        "optimization": "Fast for broadcast reads, slow for scattered access"
                    },
                    "texture_memory": {
                        "cached": True,
                        "optimization": "Spatial locality benefits, supports filtering"
                    }
                },
                "compute_hierarchy": {
                    "grid": "Collection of thread blocks",
                    "block": "Collection of threads (max 1024 threads)",
                    "warp": "32 threads executing in lockstep",
                    "thread": "Single execution unit",
                    "synchronization": {
                        "within_block": "__syncthreads(), __syncwarp()",
                        "across_blocks": "Requires kernel termination or cooperative groups"
                    }
                }
            },
            "performance_characteristics": {
                "warp_divergence": {
                    "cause": "Conditional branches with different paths in warp",
                    "impact": "Serializes execution, reduces throughput",
                    "solution": "Minimize divergent branches, use warp-level primitives"
                },
                "memory_coalescing": {
                    "requirement": "Threads in warp access consecutive memory locations",
                    "impact_if_poor": "Multiple memory transactions instead of one",
                    "optimal_pattern": "Thread N accesses address BaseAddr + N * ElementSize"
                },
                "occupancy": {
                    "definition": "Ratio of active warps to max possible warps per SM",
                    "factors": [
                        "Register usage per thread",
                        "Shared memory per block",
                        "Block size",
                        "Hardware limits"
                    ],
                    "goal": "High occupancy for latency hiding, but not always optimal"
                },
                "bank_conflicts": {
                    "cause": "Multiple threads in warp access same shared memory bank",
                    "banks": 32,
                    "serialization": "N-way conflict = N serialized accesses",
                    "broadcast_exception": "All threads reading same address = no conflict"
                }
            },
            "cuda_programming": {
                "kernel_launch": {
                    "syntax": "kernel<<<gridDim, blockDim, sharedMem, stream>>>(args)",
                    "gridDim": "Number of blocks in grid (dim3)",
                    "blockDim": "Number of threads per block (dim3)",
                    "sharedMem": "Dynamic shared memory size (bytes)",
                    "stream": "CUDA stream for async execution"
                },
                "built_in_variables": {
                    "threadIdx": "(x,y,z) thread index within block",
                    "blockIdx": "(x,y,z) block index within grid",
                    "blockDim": "(x,y,z) block dimensions",
                    "gridDim": "(x,y,z) grid dimensions",
                    "warpSize": "32 on all current NVIDIA GPUs"
                },
                "memory_qualifiers": {
                    "__device__": "Global memory variable",
                    "__shared__": "Shared memory variable",
                    "__constant__": "Constant memory variable",
                    "__managed__": "Unified memory (accessible from CPU/GPU)"
                },
                "function_qualifiers": {
                    "__global__": "Kernel function (called from host)",
                    "__device__": "Device function (called from device)",
                    "__host__": "Host function (default)",
                    "__host__ __device__": "Compiled for both"
                }
            },
            "optimization_techniques": {
                "memory_optimization": [
                    "Use shared memory for frequently accessed data",
                    "Ensure coalesced global memory access",
                    "Minimize register usage to increase occupancy",
                    "Use texture memory for read-only spatial data",
                    "Align data structures to cache line boundaries"
                ],
                "execution_optimization": [
                    "Minimize warp divergence",
                    "Maximize occupancy (but balance with resource usage)",
                    "Use asynchronous operations (streams, events)",
                    "Overlap computation with data transfer",
                    "Use warp-level primitives for synchronization"
                ],
                "algorithmic_optimization": [
                    "Tiling for data reuse",
                    "Thread coarsening for reduced synchronization",
                    "Persistent threads for GPU-side scheduling",
                    "Dynamic parallelism for irregular workloads",
                    "Cooperative groups for flexible synchronization"
                ]
            }
        }

    def _load_optimization_strategies(self):
        """
        Advanced optimization strategies for different scenarios
        """
        return {
            "matrix_multiplication": {
                "naive": "Each thread computes one output element",
                "tiled": "Use shared memory for tile-based computation",
                "tensor_cores": "Use wmma API for mixed-precision acceleration",
                "optimizations": [
                    "2D thread blocks for better memory access",
                    "Shared memory tiling to reduce global memory access",
                    "Register blocking for data reuse",
                    "Prefetching to hide latency"
                ]
            },
            "reduction": {
                "sequential_addressing": "Avoid warp divergence in early iterations",
                "warp_primitives": "Use __shfl_down_sync for warp-level reduction",
                "atomic_operations": "Final reduction with atomics",
                "multiple_kernels": "Hierarchical reduction for large arrays"
            },
            "scan_prefix_sum": {
                "work_efficient": "Up-sweep and down-sweep phases",
                "bank_conflict_free": "Add padding to avoid conflicts",
                "large_arrays": "Block-level scan + global scan of block sums"
            },
            "memory_bandwidth": {
                "measurement": "Transfer large arrays and measure time",
                "theoretical_peak": "Memory clock × bus width / 8",
                "achieved_bandwidth": "Bytes transferred / time",
                "optimization_target": "80-90% of theoretical peak is excellent"
            }
        }

    def get_architecture_detail(self, component):
        """Query specific GPU architecture component details"""
        return self.knowledge_base.get("architecture", {}).get(component, "Component not found")

    def get_optimization_strategy(self, algorithm):
        """Get optimization strategy for specific algorithm"""
        return self.optimization_strategies.get(algorithm, "Strategy not found")

    def analyze_performance_issue(self, issue_type):
        """Analyze common GPU performance issues"""
        return self.knowledge_base.get("performance_characteristics", {}).get(issue_type, "Issue type not found")

    def generate_cuda_template(self, pattern="basic_kernel"):
        """Generate CUDA code templates"""
        templates = {
            "basic_kernel": """
__global__ void myKernel(float* input, float* output, int N) {
    // Calculate global thread ID
    int tid = blockIdx.x * blockDim.x + threadIdx.x;

    // Boundary check
    if (tid < N) {
        // Perform computation
        output[tid] = input[tid] * 2.0f;
    }
}

// Host code
int main() {
    int N = 1024;
    int blockSize = 256;
    int gridSize = (N + blockSize - 1) / blockSize;

    // Launch kernel
    myKernel<<<gridSize, blockSize>>>(d_input, d_output, N);
}
""",
            "shared_memory_kernel": """
__global__ void sharedMemKernel(float* input, float* output, int N) {
    // Shared memory declaration
    __shared__ float sharedData[256];

    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int localIdx = threadIdx.x;

    // Load data to shared memory
    if (tid < N) {
        sharedData[localIdx] = input[tid];
    }

    // Synchronize threads in block
    __syncthreads();

    // Use shared memory for computation
    if (tid < N) {
        float result = 0.0f;
        // Example: simple neighbor averaging
        if (localIdx > 0) result += sharedData[localIdx - 1];
        result += sharedData[localIdx];
        if (localIdx < blockDim.x - 1) result += sharedData[localIdx + 1];

        output[tid] = result / 3.0f;
    }
}
""",
            "reduction_kernel": """
__global__ void reductionKernel(float* input, float* output, int N) {
    __shared__ float sdata[256];

    int tid = threadIdx.x;
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    // Load and perform first level of reduction
    sdata[tid] = (i < N) ? input[i] : 0.0f;
    __syncthreads();

    // Reduction in shared memory
    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            sdata[tid] += sdata[tid + s];
        }
        __syncthreads();
    }

    // Write result for this block
    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}
"""
        }
        return templates.get(pattern, "Template not found")


# Example usage and knowledge queries
if __name__ == "__main__":
    agent = GPUExpertAgent()

    # Query architecture details
    print("=== GPU Memory Hierarchy ===")
    memory_info = agent.get_architecture_detail("memory_hierarchy")
    for mem_type, details in memory_info.items():
        print(f"\n{mem_type.upper()}:")
        for key, value in details.items():
            print(f"  {key}: {value}")

    # Get optimization strategy
    print("\n=== Matrix Multiplication Optimization ===")
    matmul_strategy = agent.get_optimization_strategy("matrix_multiplication")
    print(matmul_strategy)

    # Analyze performance issue
    print("\n=== Warp Divergence Analysis ===")
    divergence_info = agent.analyze_performance_issue("warp_divergence")
    print(divergence_info)

    # Generate code template
    print("\n=== CUDA Kernel Template ===")
    template = agent.generate_cuda_template("shared_memory_kernel")
    print(template)
