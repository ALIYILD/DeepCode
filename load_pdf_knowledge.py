"""
PDF Content Processor: Inside NVIDIA GPUs

This script extracts and structures the knowledge from the
"Inside NVIDIA GPUs: Anatomy of high performance matmul kernels" document
into the shared knowledge base for the 102-agent team.
"""

from shared_gpu_knowledge_base import SharedGPUKnowledgeBase


def load_nvidia_gpu_internals_knowledge():
    """
    Load comprehensive GPU knowledge from the PDF content
    """
    kb = SharedGPUKnowledgeBase()

    # ============================================================================
    # PART 1: FUNDAMENTALS OF NVIDIA GPU ARCHITECTURE
    # ============================================================================

    kb.add_pdf_knowledge("gpu_architecture_fundamentals", {
        "source": "Inside NVIDIA GPUs (September 2025)",
        "overview": {
            "two_essential_tasks": [
                "Move and store data (memory system)",
                "Do useful work with data (compute pipelines)"
            ],
            "focus_architecture": "Hopper H100",
            "key_insight": "Understanding Hopper enables adaptation to future (Blackwell, Rubin) and past (Ampere, Volta) architectures"
        },
        "memory_hierarchy": {
            "device_memory_vram": {
                "type": "HBM (High Bandwidth Memory)",
                "location": "Off-chip DRAM, packaged with GPU",
                "contains": ["global memory (GMEM)", "local memory (register spill space)"],
                "technology": "Stacked HBM layers with logic layer at bottom"
            },
            "l2_cache": {
                "type": "k-way set-associative SRAM",
                "size": "3-40 MB depending on GPU",
                "organization": "Physically partitioned into two parts",
                "access": "Each SM connects directly to one partition, indirectly to other via crossbar",
                "latency_cycles": 200
            },
            "distributed_shared_memory": {
                "description": "Pooled shared memories (SMEM) of physically close SMs (a GPC)",
                "introduced": "Hopper architecture",
                "feature": "Direct SM-to-SM communication for loads, stores, atomics"
            },
            "l1_and_shared_memory": {
                "l1_cache": {
                    "type": "k-way set-associative SRAM",
                    "scope": "private to each SM",
                    "size": "32-128 KB per SM",
                    "line_size": "128 bytes",
                    "latency_cycles": 30
                },
                "shared_memory": {
                    "type": "Programmer-managed on-chip SRAM",
                    "scope": "per-block",
                    "size": "48-164 KB per SM (configurable)",
                    "sharing": "L1 and SMEM share same physical storage",
                    "configuration": "Software-configurable split",
                    "access_time": "~30 cycles",
                    "banks": 32,
                    "bank_width": "4 bytes (32 bits)"
                }
            },
            "register_file": {
                "type": "Fastest storage next to compute units",
                "scope": "Private to individual threads",
                "size_per_sm": "65,536 registers (Hopper)",
                "max_per_thread": 255,
                "latency_cycles": 1,
                "comparison": "Total RMEM capacity ~ same as combined L1/SMEM"
            },
            "memory_trend": "GMEM → Registers: bandwidth increases, latency/capacity decrease by orders of magnitude",
            "key_implications": [
                "Keep frequently accessed data close to compute units",
                "Minimize accesses to lower hierarchy levels, especially GMEM"
            ]
        },
        "h100_specifics": {
            "total_sms": 132,
            "gpcs": 8,
            "sms_per_gpc": 18,
            "l2_partitions": 2,
            "gpc_to_l2": "4 GPCs per L2 partition",
            "actual_products": {
                "note": "SXM/PCIe expose 132 or 114 SMs (some fused off)",
                "cluster_implication": "Can't use all SMs with clusters > 2 SMs"
            }
        }
    })

    # Memory subsystem details
    kb.add_pdf_knowledge("memory_subsystem_deep_dive", {
        "gmem_dram_model": {
            "cell_structure": {
                "components": ["transistor", "capacitor"],
                "operation": "Capacitor stores charge (1 or 0), transistor controls access",
                "signals": ["wordline (row select)", "bitline (data read/write)"]
            },
            "access_pattern_impact": {
                "row_activation": "Opening a row is expensive",
                "sequential_access": "Elements in same row are fast to access",
                "strided_access": "Touching multiple rows is slow",
                "coalescing": "Threads should access contiguous memory to minimize DRAM row activations",
                "performance_impact": "Bad patterns can cause 13x slowdown"
            },
            "hbm_organization": {
                "structure": "Stack of DRAM layers with logic layer at bottom",
                "reference": "Demystifying the Characteristics of High Bandwidth Memory for Real-Time Systems paper"
            }
        },
        "smem_sram_model": {
            "cell_technology": "SRAM (many more transistors per bit than DRAM)",
            "speed_vs_capacity": "Faster but larger/less dense than DRAM",
            "organization": {
                "banks": 32,
                "bank_width": "4 bytes (32 bits)",
                "total_bandwidth": "128 bytes per cycle (all 32 banks)"
            },
            "bank_conflicts": {
                "definition": "Multiple threads access different addresses in same bank",
                "impact": "N-way conflict = N serialized accesses",
                "worst_case": "32 threads, same bank, different addresses = 32x slower",
                "broadcast_exception": "All threads accessing same address = no conflict (multicast)",
                "detection": "Nsight Compute: shared_ld/st_bank_conflict metric",
                "solutions": [
                    "Padding arrays to avoid conflicts",
                    "Swizzling access patterns",
                    "Using different data layouts"
                ]
            }
        },
        "l1_cache_model": {
            "pipeline": [
                "Memory request issued by warp",
                "Enters MIO pipeline, dispatched to LSUIN router",
                "SMEM requests served immediately from data array",
                "GMEM requests proceed to tag-comparison stage",
                "Hit: served from data array",
                "Miss: propagates to L2 (and beyond if needed)"
            ],
            "set_associative_logic": {
                "set_id_extraction": "From GMEM address",
                "tag_comparison": "Check all tags in set",
                "validity_check": "Invalid = miss even if tag matches",
                "replacement_policy": "Pseudo-LRU"
            },
            "cache_control": {
                "ldg": "Use read-only cache (texture cache)",
                "ldu": "Bypass L1",
                "default": "Use L1"
            }
        }
    })

    # Compute architecture
    kb.add_pdf_knowledge("compute_architecture_details", {
        "streaming_multiprocessor": {
            "quadrants": 4,
            "threads_per_sm": {
                "maximum": 2048,
                "concurrent_warps": 64,
                "warp_size": 32
            },
            "parallelism_vs_concurrency": {
                "parallel_execution": "128 threads (4 warps) can execute simultaneously per SM",
                "concurrent_threads": "2048 threads (64 warps) can be resident and scheduled",
                "key_insight": "Concurrency enables latency hiding through context switching"
            },
            "components": {
                "tensor_cores": {
                    "purpose": "Specialized matrix multiplication units",
                    "tile_sizes": "e.g., 64x16 @ 16x256",
                    "usage": "Large matmuls decomposed into many tile operations"
                },
                "cuda_cores": {
                    "operations": "Standard FP operations (FMA: fused multiply-add)",
                    "marketing_note": "CUDA cores is marketing terminology"
                },
                "special_function_units": {
                    "transcendental": ["sin", "cos", "exp", "log"],
                    "algebraic": ["sqrt", "rsqrt"],
                    "throughput": "Typically 1/4 rate of standard FP"
                },
                "load_store_units": {
                    "purpose": "Service load/store instructions",
                    "complement": "Works alongside TMA engine"
                },
                "warp_schedulers": {
                    "count_per_sm": 4,
                    "issue_rate": "1 warp instruction per cycle per scheduler",
                    "scheduling_policy": "Round-robin with priority"
                }
            }
        },
        "tensor_memory_accelerator": {
            "introduced": "Hopper architecture",
            "capabilities": [
                "Asynchronous GMEM ↔ SMEM transfers",
                "SMEM ↔ SMEM transfers within cluster",
                "Automatic swizzling to reduce bank conflicts"
            ],
            "significance": "Major architectural advancement for async data movement"
        }
    })

    # Speed of light and power throttling
    kb.add_pdf_knowledge("performance_characteristics_detailed", {
        "speed_of_light": {
            "definition": "Maximum compute throughput dictated by physical chip characteristics",
            "formula": "perf = freq_clk_max * num_tc * flop_per_tc_per_clk",
            "h100_bf16_example": {
                "clock_max": "1.98 GHz",
                "tensor_cores": 528,
                "flops_per_tc_per_clk": 512,
                "peak_performance": "~989 TFLOP/s"
            },
            "important_note": "Speed of light is NOT constant"
        },
        "power_throttling": {
            "mechanism": "GPU clock frequency drops under power/thermal constraints",
            "impact": "Effective speed of light decreases with clock frequency",
            "practical_implication": "Peak performance varies based on thermal/power conditions",
            "reference": "Horace He's blog on predictable data performance"
        },
        "instruction_throughput": {
            "fp32": "2x CUDA cores/SM operations per cycle",
            "fp64": "1/2 to 1/32 of FP32 rate (architecture dependent)",
            "int32": "Same as FP32",
            "special_functions": "1/4 rate (sin, cos, log, etc.)",
            "tensor_cores": "8x to 16x FP32 throughput for matrix ops",
            "tf32": "Tensor Core precision for AI (Ampere+)",
            "bf16": "BFloat16 support in Tensor Cores (Ampere+)",
            "fp8": "FP8 precision (Hopper+)"
        },
        "memory_bandwidth": {
            "theoretical_calculation": "memory_clock × bus_width ÷ 8",
            "hbm2": "Up to 2 TB/s (H100)",
            "gddr6x": "Up to 1 TB/s (RTX 4090)",
            "achievable_target": "80-90% of theoretical is excellent",
            "common_bottleneck": "Often the limiting factor in kernels"
        },
        "occupancy": {
            "definition": "Active warps / maximum possible warps per SM",
            "limiting_factors": {
                "registers": "Limited by register file size (65,536 per SM)",
                "shared_memory": "Limited by SMEM size (up to 228 KB)",
                "block_size": "Too small = low occupancy",
                "blocks_per_sm": "Hardware limit (16-32)"
            },
            "myth": "100% occupancy not always optimal",
            "reality": "Trade-off between occupancy and per-thread resources",
            "tools": ["CUDA Occupancy Calculator", "Nsight Compute"]
        }
    })

    # ============================================================================
    # PART 2: CUDA PROGRAMMING MODEL
    # ============================================================================

    kb.add_pdf_knowledge("cuda_programming_model_detailed", {
        "key_abstractions": {
            "thread": "Smallest unit of execution",
            "warp": "32 threads executing in lockstep (SIMT model)",
            "thread_block": "Group of threads (up to 1024) on single SM",
            "thread_block_cluster": "Group of blocks across multiple SMs (Hopper+)",
            "grid": "Collection of thread blocks or clusters"
        },
        "built_in_variables": {
            "gridDim": "Dimensions of grid (blocks in grid)",
            "blockIdx": "Block index within grid",
            "blockDim": "Dimensions of block (threads in block)",
            "threadIdx": "Thread index within block",
            "warpSize": "32 (constant on all NVIDIA GPUs)",
            "storage": "Stored in special registers, initialized at kernel launch"
        },
        "coordinate_calculation": {
            "global_x": "blockIdx.x * blockDim.x + threadIdx.x",
            "global_y": "blockIdx.y * blockDim.y + threadIdx.y",
            "reshaping_trick": "1D → 2D: x = idx % 32, y = idx / 32"
        },
        "execution_requirements": {
            "minimum_block_size": "128 threads (4 warps)",
            "reasoning": [
                "Each SM has 4 warp schedulers",
                "Want to keep all schedulers busy",
                "Warp-group (4 warps) is execution unit for WGMMA on Hopper"
            ]
        },
        "gpc_and_clusters": {
            "gpc": "Graphics Processing Cluster (legacy name, now compute-only)",
            "cluster_abstraction": "Thread block clusters map to GPC hardware",
            "dsmem": "Distributed Shared Memory - direct SM-to-SM communication within GPC"
        }
    })

    # ============================================================================
    # PART 3: PTX AND SASS
    # ============================================================================

    kb.add_pdf_knowledge("gpu_assembly_languages", {
        "isa_definition": "Instruction Set Architecture - set of instructions processor can execute",
        "sass": {
            "name": "Native ISA for NVIDIA GPUs",
            "documentation": "Poorly documented, especially for recent generations",
            "reverse_engineering": "Some older generations partially reverse-engineered",
            "reality": "What actually executes on hardware"
        },
        "ptx": {
            "name": "Parallel Thread Execution - NVIDIA's virtual ISA",
            "nature": "Abstract GPU ISA, not executed directly",
            "compilation": "PTX → SASS via ptxas compiler",
            "forward_compatibility": {
                "key_advantage": "PTX from decade ago runs on modern GPUs",
                "mechanism": "JIT-compiled to SASS when needed",
                "trade_off": "May not exploit latest hardware features optimally"
            }
        },
        "compilation_flow": {
            "stages": "CUDA C++ → PTX → SASS",
            "embedding": "Both PTX and SASS embedded in CUDA binary",
            "runtime_selection": "Matching SASS used if available, else JIT PTX"
        },
        "why_care_about_assembly": {
            "performance_gains": "Last few percent of performance (critical at scale)",
            "scale_impact": "1% improvement across 30,000 GPUs = millions saved",
            "o_nr_complexity": "O(NR) not O(N) - Nuclear Reactor complexity class",
            "compiler_verification": "Check that hints produce expected instructions",
            "example_instructions": {
                "ldg_128": "Vectorized 128-bit load from global memory",
                "pragma_unroll": "Verify loop unrolling actually happened"
            }
        },
        "inline_ptx": {
            "necessity": "Some instructions have no CUDA C++ equivalent",
            "usage": "Write inline PTX in CUDA kernels",
            "examples_coming": "Will see in async matmul section"
        },
        "famous_example": {
            "paper": "Dissecting the NVIDIA Volta GPU Architecture via Microbenchmarking",
            "technique": "Tweaked SASS to avoid bank conflicts",
            "result": "132 → 152 GFLOP/s (15.4% improvement)"
        }
    })

    kb.add_pdf_knowledge("ptx_sass_analysis_insights", {
        "compiler_optimizations": [
            "Early exits for out-of-bounds threads",
            "Loop unrolling (×4 in PTX, ×16 in SASS)",
            "Splitting into main and tail loops",
            "Pipeline load-balancing (bfi instead of add)",
            "Interleaving loads with FMAs",
            "Moving loads to top of loop"
        ],
        "compiler_inefficiencies_observed": [
            "Unnecessary initialization to zero",
            "Overly complex address calculations",
            "Redundant partial-offset calculations",
            "Unused program counter loads",
            "Noop predicates",
            "Superfluous branch instructions",
            "Infinite loop after EXIT (padding?)",
            "NOP padding for alignment"
        ],
        "ilp_importance": {
            "definition": "Instruction-Level Parallelism - work kept in flight per warp",
            "benefit": "Hide latency by issuing independent instructions back-to-back",
            "low_ilp_example": "y = a*b+1; z = y*c+1; w = z*c+1; → 12 cycles (serialized)",
            "high_ilp_example": "c0 = a0*b0+1; c1 = a1*b1+1; c2 = a2*b2+1; → 6 cycles (parallel)",
            "unrolling_benefit": "Exposes ILP, reduces branch instructions"
        },
        "debugging_tip": "Use #pragma unroll 1 to disable unrolling for easier PTX/SASS analysis"
    })

    # ============================================================================
    # PART 4: MATMUL KERNEL DESIGN
    # ============================================================================

    kb.add_pdf_knowledge("matmul_fundamentals", {
        "definition": "C[m,n] = sum over k of A[m,k] * B[k,n]",
        "work_calculation": {
            "dot_products": "M × N",
            "operations_per_dot": "K multiply-adds",
            "total_flops": "2 × M × N × K (factor of 2: FMA counts as 2 ops)"
        },
        "parallelism": "All M×N dot products are independent → embarrassingly parallel",
        "gemm_generalization": "C = alpha * A @ B + beta * C",
        "loop_order_equivalences": {
            "traditional": "for m: for n: for k: C[m,n] += A[m,k] * B[k,n]",
            "outer_product_view": "for k: for m: for n: C[m,n] += A[m,k] * B[k,n]",
            "key_insight": "Matmul = sum of partial outer products",
            "bandwidth_optimization": "K-outermost reduces A loads from N³ to N²"
        },
        "partial_accumulation": {
            "dot_product": "Sum of partial dot products",
            "enables_blocking": "Break into block matmuls fitting in SMEM",
            "bandwidth_reduction": "Move blocks to SMEM, compute there, reduce GMEM traffic"
        }
    })

    kb.add_pdf_knowledge("naive_matmul_analysis", {
        "naive_kernel_characteristics": {
            "thread_organization": "Each thread computes one output element",
            "block_size": "32×32 = 1024 threads",
            "launch_config": "CEIL_DIV(M,32) × CEIL_DIV(N,32) blocks",
            "register_usage": "32 registers per thread",
            "performance": "3171 GFLOP/s (coalesced) vs 243 GFLOP/s (uncoalesced) on H100"
        },
        "coalescing_impact": {
            "good_pattern": "row = blockIdx.x*32 + threadIdx.x/32, col = blockIdx.y*32 + threadIdx.x%32",
            "bad_pattern": "Swapping % and / operators → 13x slowdown",
            "hardware_optimizations": [
                "Matrix A: 32 per-thread LDG.32 → single warp-level LDG.32 (broadcast)",
                "Matrix B: 32 consecutive LDG.32 → single 128B warp-level load"
            ]
        },
        "occupancy_analysis": {
            "registers_limit": "32 reg/thread × 1024 threads = 32K per block → max 2 blocks/SM",
            "threads_limit": "2048 threads/SM, 1024 threads/block → max 2 blocks/SM",
            "smem_limit": "1024B overhead → max 8 blocks/SM (not binding)",
            "actual": "min(2, 2, 8) = 2 blocks per SM",
            "resident_blocks": "114 SMs × 2 = 228 blocks",
            "waves": "16,384 total blocks / 228 resident = ~72 waves"
        },
        "tile_quantization": {
            "issue": "When matrix dims not divisible by tile size, threads do no work",
            "example": "33×33 matrix with 32×32 tiles → ~75% threads idle",
            "severity": "Pronounced when tiles large relative to matrix"
        },
        "wave_quantization": {
            "issue": "Similar to tile quantization but for SM utilization",
            "example": "114 blocks (1 wave) vs 115 blocks (2 waves) → nearly 2x time",
            "impact": "Especially noticeable for small wave counts"
        }
    })

    kb.add_pdf_knowledge("roofline_model", {
        "definition": "Plot of performance (FLOP/s) vs arithmetic intensity (AI)",
        "arithmetic_intensity": "FLOPs performed per byte loaded from GMEM",
        "ridge_point": "peak_perf / GMEM_bandwidth",
        "h100_ridge": "~410 (for H100 PCIe)",
        "regions": {
            "memory_bound": "Left of ridge point, limited by memory bandwidth",
            "compute_bound": "Right of ridge point, limited by compute throughput"
        },
        "goal": "Move kernels from memory-bound to compute-bound region",
        "strategies_to_increase_ai": [
            "Compute multiple output elements per thread",
            "Make output tiles as square as possible",
            "Reuse data in faster memory (SMEM, registers)"
        ]
    })

    # ============================================================================
    # PART 5: WARP-TILING METHOD
    # ============================================================================

    kb.add_pdf_knowledge("warp_tiling_method", {
        "constraints": "Near-SOTA under pre-Volta conditions (no TMA, no async, no tensor cores, fp32 only)",
        "key_principles": [
            "Output tiles should be square (maximize arithmetic intensity)",
            "Break computation into substeps fitting in SMEM",
            "Load chunks from GMEM to SMEM",
            "Compute on SMEM data",
            "Accumulate results in registers"
        ],
        "tile_sizes": {
            "block_m": 128,
            "block_n": 128,
            "block_k": 16,
            "thread_m": 8,
            "thread_n": 8,
            "warp_m": 64,
            "warp_n": 64
        },
        "algorithm_structure": {
            "outer_loop": "Iterate over K dimension in chunks of Bk",
            "load_phase": [
                "Load A[Bm × Bk] chunk to As (transposed)",
                "Load B[Bk × Bn] chunk to Bs (not transposed)",
                "Use vectorized loads (LDG.128)"
            ],
            "sync_after_load": "__syncthreads() ensures all data in SMEM",
            "compute_phase": [
                "Each thread computes Tm × Tn output elements",
                "Warp-tiling: warps process Wm × Wn sub-tiles",
                "Thread-tiling: threads process Tm × Tn sub-sub-tiles",
                "Matmul as series of outer products: regM × regN"
            ],
            "sync_after_compute": "__syncthreads() prevents next chunk overwriting current",
            "advance_pointers": "A += Bk, B += Bk*N",
            "epilogue": "Flush threadResults registers to output matrix C"
        },
        "loading_details": {
            "matrix_b_to_bs": {
                "straightforward": "Bs not transposed",
                "pattern": "Each of 4 warps fetches row of B",
                "vectorization": "LDG.128 → STS.128 per thread",
                "iterations": "4 loops with stride of 4 rows"
            },
            "matrix_a_to_as": {
                "tricky": "As is transposed",
                "reason": "Enable vectorized loads (LDS.128) during compute",
                "trade_off": "Stores cannot be vectorized (scatter to column = same bank)",
                "acceptable": "Loads happen multiple times, stores only once"
            }
        },
        "bank_conflict_handling": {
            "issue": "Transposed As causes bank conflicts on stores",
            "mitigation": "Accepted because compute-phase loads are vectorized",
            "priority": "Fast loads > fast stores (loads happen more often)"
        },
        "performance": {
            "baseline_warp_tiling": "~32 TFLOP/s",
            "improvement_over_naive": "Significant due to better arithmetic intensity",
            "limitation": "Not SOTA - modern GPUs have tensor cores and async features"
        },
        "auto_tuning": "In practice, tile sizes should be auto-tuned for specific GPU",
        "code_reference": "Simon Boehm's blog post kernel 10"
    })

    # ============================================================================
    # PART 6: HOPPER SOTA ASYNCHRONOUS MATMUL
    # ============================================================================

    kb.add_pdf_knowledge("hopper_sota_matmul", {
        "new_features_used": [
            "TMA (Tensor Memory Accelerator)",
            "Tensor Cores",
            "bf16 precision",
            "Asynchronous operations",
            "Thread block clusters",
            "wgmma.mma_async instructions"
        ],
        "performance_progression": {
            "warp_tiling_baseline": "32 TFLOP/s",
            "tensor_cores_tma": "317 TFLOP/s (10x improvement)",
            "increased_tile_size": "423 TFLOP/s",
            "pipelined_tma_tc": "498 TFLOP/s",
            "two_consumer_wgs": "610 TFLOP/s",
            "persistent_kernels": "660 TFLOP/s",
            "faster_ptx_barriers": "704 TFLOP/s",
            "clusters_tma_multicast": "734 TFLOP/s",
            "micro_optimizations": "747 TFLOP/s",
            "tma_async_stores": "758 TFLOP/s",
            "hilbert_curve_scheduling": "764 TFLOP/s",
            "stmatrix_optimization": "771 TFLOP/s (~107% of cuBLAS)"
        },
        "simplifications_vs_warp_tiling": [
            "Only 128 threads (4 warps) needed per block",
            "TMA handles data movement (vs manual warp-level loads)",
            "Automatic swizzling (vs manual bank conflict management)",
            "Tensor cores handle matmul (vs manual FMA loops)"
        ]
    })

    kb.add_pdf_knowledge("tma_tensor_memory_accelerator", {
        "purpose": "Asynchronous data transfers between GMEM ↔ SMEM and SMEM ↔ SMEM",
        "setup": {
            "tensor_map_creation": "cuTensorMapEncodeTiled API",
            "metadata": [
                "Data type (e.g., bf16)",
                "Rank (e.g., 2 for matrix)",
                "Pointer to source",
                "Shape (fastest stride dimension first)",
                "Stride information",
                "Target SMEM shape",
                "Swizzle mode (e.g., 128B pattern)"
            ]
        },
        "barriers": {
            "type": "Shared memory barriers (mbarrier)",
            "initialization": "init(&bar, num_threads)",
            "fence": "cde::fence_proxy_async_shared_cta() - proxy memory model ordering"
        },
        "async_copy_pattern": {
            "single_thread_launch": "Only thread 0 launches TMA",
            "copy_instruction": "cde::cp_async_bulk_tensor_2d_global_to_shared(dst, tensorMap, offset_k, offset_mn, barrier)",
            "barrier_arrive_tx": "cuda::device::barrier_arrive_tx(bar, 1, sizeof(data)) - arms barrier with byte count",
            "other_threads_arrive": "bar.arrive() - threads contribute arrivals without bytes",
            "wait": "bar.wait(token) - blocks until all threads arrived AND all bytes transferred",
            "completion_condition": "Both thread count and byte count satisfied"
        },
        "memory_consistency": {
            "async_proxy": "TMA engine",
            "generic_proxy": "Normal thread ld/st",
            "fence_role": "Order visibility between proxies",
            "complexity_note": "Memory consistency deserves dedicated post"
        }
    })

    kb.add_pdf_knowledge("swizzling_deep_dive", {
        "motivation": {
            "problem": "Naive SMEM layout causes bank conflicts for column access",
            "example": "Loading first column → all elements in same bank → 8-way conflict",
            "solution": "Rearrange data in SMEM to distribute column elements across banks"
        },
        "swizzle_result": {
            "rows": "Still can be loaded in single cycle (no change)",
            "columns": "Now lie along diagonal → different banks → single cycle",
            "generalization": "ANY row or column can be loaded conflict-free after swizzling"
        },
        "swizzle_modes": {
            "128B": "Swizzle<3,4,3>",
            "64B": "Swizzle<2,4,3>",
            "32B": "Swizzle<1,4,3>"
        },
        "swizzle_function_decode": {
            "swizzle_3_4_3": {
                "b_bits": 3,
                "m_base": 4,
                "s_shift": 3,
                "bit_mask": "(1 << 3) - 1 = 0b111",
                "yyy_mask": "0b111 << 7 = 0b11110000000",
                "operation": "Extract bits GHI, XOR with JKL to get WYZ",
                "result_pattern": "0bxxxxxxGH_IWYZxxxx where WYZ = GHI ^ JKL"
            },
            "mechanism": "XOR with specific mask pattern",
            "xor_property": "When control bit is 1, XOR flips corresponding lower bit"
        },
        "swizzle_application": {
            "input": "Linear SMEM address",
            "process": "Apply XOR mask to flip specific bits",
            "output": "Swizzled SMEM address",
            "automatic": "TMA applies swizzling on load, unswizzles on store"
        },
        "transpose_benefit": {
            "naive": "Load row, write as column → 8-way bank conflict",
            "swizzled": "No bank conflicts on reads or writes",
            "caution": "Must be careful with indexing"
        },
        "reference": "CUTLASS, Simon (not Boehm) explanation"
    })

    kb.add_pdf_knowledge("tensor_cores_wgmma", {
        "mma_instruction_evolution": {
            "wmma": "Warp-cooperative, synchronous (older generations)",
            "mma_sync": "Warp-cooperative, synchronous (Ampere)",
            "wgmma_mma_async": "Warp-group cooperative, asynchronous (Hopper)"
        },
        "warp_group": "4 warps = 128 threads",
        "wgmma_shapes": {
            "format": "m64nNk16 where N ∈ {8, 16, 24, ..., 256}",
            "example": "m64n64k16 = 64×16 @ 16×64 matmul",
            "performance": "Larger N values more performant (if enough registers/SMEM)"
        },
        "operand_placement": {
            "matrix_a": "Registers or SMEM",
            "matrix_b": "Must be in SMEM",
            "accumulator": "Always in registers (fp32)"
        },
        "accumulator_distribution": {
            "size_example": "64×64 output",
            "threads": "128 threads in warp group",
            "per_thread": "(64/16) × 8 = 32 fp32 registers",
            "total": "128 × 32 = 4096 registers = 64×64 elements",
            "declaration": "float d[WGMMA_N/16][8]"
        },
        "wgmma_instruction_pattern": {
            "fence": "wgmma.fence.sync.aligned - establish ordering",
            "mma_calls": "Multiple wgmma.mma_async calls (e.g., 4x for 64×64)",
            "commit_group": "wgmma.commit_group.sync.aligned - close batch",
            "wait": "wgmma.wait_group.sync.aligned %0 - block until done"
        },
        "fence_details": {
            "purpose": "Order accesses to warpgroup registers",
            "required": "Before first wgmma.mma_async",
            "exception": "Not needed between back-to-back MMAs of same shape",
            "compiler": "Will insert automatically if missing"
        },
        "mma_semantics": {
            "default": "D = A @ B + D (GEMM accumulation)",
            "alternative_flag": "D = A @ B (no accumulation)",
            "data_types": "bf16 @ bf16 → fp32 (example)"
        },
        "smem_descriptors": {
            "contents": [
                "SMEM base address",
                "Swizzle mode",
                "LBO (leading dim byte offset)",
                "SBO (stride dim byte offset)"
            ],
            "purpose": "Tell tensor core how to navigate SMEM layout",
            "complexity_note": "Descriptor construction details omitted (deserve own post)"
        },
        "chunk_decomposition": {
            "why_4_calls": "64×64 @ 64×64 = 4× (64×16 @ 16×64)",
            "accumulation": "Each call adds partial result to accumulator",
            "column_major_b": "Slightly mind-bending but mathematically correct"
        },
        "asm_volatile_notes": {
            "inline_ptx": "Some Hopper instructions not in CUDA C++",
            "memory_clobber": ":::memory prevents compiler memory optimizations",
            "volatile": "Prevents deletion or hoisting of asm block"
        }
    })

    kb.add_pdf_knowledge("pipelining_optimizations", {
        "problem": "Wasted TMA and TC cycles due to serialization",
        "solution": "Pipeline compute and data movement",
        "producer_consumer_model": {
            "producer_warpgroup": "Keeps TMA busy, streams chunks into queue",
            "consumer_warpgroup": "Drains queue, keeps tensor cores saturated",
            "queue_size": "e.g., 5 slots (configurable)",
            "synchronization": "full[i]/empty[i] barrier pairs per queue slot"
        },
        "queue_barriers": {
            "full": "Signals data ready to consume",
            "empty": "Signals buffer ready to fill",
            "initialization": "init with num_consumers * 128 + 1 threads"
        },
        "producer_logic": {
            "thread": "Only thread 0 orchestrates TMA",
            "wait_empty": "empty[qidx].wait() - block until slot free",
            "issue_tma": "cp_async_bulk_tensor for A and B",
            "signal_full": "barrier_arrive_tx with byte count"
        },
        "consumer_logic": {
            "initialization": "Mark all slots as empty (ready to fill)",
            "wait_full": "full[qidx].wait() - block until data ready",
            "compute": "Run tensor core MMAs on buffer",
            "signal_empty": "Barrier arrive to mark slot consumed"
        },
        "tile_size_upgrade": {
            "reason": "Larger tensor core shapes maximize throughput",
            "example": "m64n64k16 → m64nBNk16 (e.g., m64n128k16)"
        }
    })

    kb.add_pdf_knowledge("multiple_consumers_and_scaling", {
        "register_pressure_issue": {
            "problem": "128×256 tile needs 256 fp32 registers per thread for accumulator",
            "limit": "Exceeds per-thread register budget",
            "consequence": "Register spilling to device memory (very bad)"
        },
        "solution": "Two consumer warp-groups",
        "consumer_distribution": {
            "wg1": "Computes upper 64×256 half-tile",
            "wg2": "Computes lower 64×256 half-tile",
            "per_thread_registers": "Halved, avoids spills"
        },
        "block_configuration": {
            "producer": "1 warp-group (128 threads) - TMA",
            "consumer_a": "1 warp-group (128 threads) - upper half",
            "consumer_b": "1 warp-group (128 threads) - lower half",
            "total": "384 threads per block"
        },
        "matmul_decomposition": "Each consumer handles subset of output tile rows"
    })

    kb.add_pdf_knowledge("persistent_kernels", {
        "concept": "Launch small fixed number of blocks (often 1 per SM), keep alive for entire workload",
        "vs_traditional": "Traditional: 1 block per tile, many waves",
        "advantages": [
            "Overlap output store with incoming loads",
            "Reduce kernel launch overhead",
            "Better cache locality",
            "More control over scheduling"
        ],
        "implementation": {
            "launch": "1 block per SM (e.g., 114 blocks on H100 PCIe)",
            "work_loop": "Each block processes multiple tiles internally",
            "tile_queue": "Blocks pull tiles from global queue until done"
        },
        "latency_hiding": "While flushing results to GMEM, load next tile's data"
    })

    kb.add_pdf_knowledge("scheduling_strategies", {
        "naive_schedule": {
            "approach": "Each SM processes consecutive tiles",
            "problem": "Poor cache locality across SMs"
        },
        "block_wise_cache_aware": {
            "approach": "Group tiles into blocks, SM processes entire block before moving",
            "benefit": "Better L2 cache reuse within block",
            "improvement": "Over naive"
        },
        "hilbert_curve_schedule": {
            "approach": "Traverse output tiles following Hilbert space-filling curve",
            "key_property": "Points close on curve are close in 2D space",
            "benefit": "Maximizes spatial locality for cache reuse",
            "improvement": "Best locality, +6-8 TFLOP/s over cache-aware",
            "performance_gain": "758 → 764 TFLOP/s"
        },
        "space_filling_curves": {
            "definition": "Continuous curve passing through every point in space",
            "locality": "1D distance on curve ≈ 2D distance in space",
            "application": "Determines which tile to process next"
        }
    })

    kb.add_pdf_knowledge("thread_block_clusters", {
        "motivation": "Reduce L2/GMEM traffic by sharing data across SMs",
        "dsmem": "Distributed Shared Memory - SMs in cluster share SMEM directly",
        "super_sm_concept": "Treat cluster as 'super-SM' with pooled SMEM",
        "implementation": {
            "cluster_collaboration": "Multiple SMs work on larger 'super-tile'",
            "data_sharing": "Direct SM-to-SM loads via DSMEM",
            "reduced_loads": "Each chunk loaded once per cluster, not once per SM"
        },
        "scheduling": "Hilbert curve at cluster granularity (super-tiles)",
        "tma_multicast": {
            "feature": "TMA can broadcast data to multiple SMs in cluster",
            "benefit": "Further reduces redundant loads",
            "performance": "704 → 734 TFLOP/s"
        },
        "cluster_size_constraints": {
            "h100_reality": "Not all SMs usable due to fusing",
            "example": "Can't use clusters > 2 SMs to cover all 114 SMs"
        }
    })

    kb.add_pdf_knowledge("final_optimizations", {
        "barrier_optimization": {
            "redundant_arrivals": "Consumer threads don't need to arrive on full[qidx]",
            "important_condition": "Only 'all bytes arrived' matters",
            "savings": "256 tokens per iteration (only tid==0 needs to arrive)"
        },
        "register_rebalancing": {
            "instruction": "asm volatile(\"setmaxnreg.{inc,dec}.sync.aligned.u32 %0;\\n\" : : \"n\"(RegCount));",
            "purpose": "Shift register budget from producer (lightweight) to consumers (heavy)",
            "benefit": "Better resource utilization"
        },
        "cache_bypass_on_output": {
            "problem": "Output writes pollute L1/L2 caches",
            "solution_1": "__stwt (write-through) - bypass L1/L2",
            "solution_2": "Async store via SMEM then TMA to GMEM",
            "benefit": "Overlap write-back with compute, don't evict useful data"
        },
        "accumulator_initialization": {
            "naive": "Zero-initialize accumulator registers",
            "optimized": "First MMA does C = A @ B, subsequent do C = A @ B + C",
            "savings": "Skip redundant zeroing"
        },
        "stmatrix_method": {
            "contribution": "Aroun's PR",
            "technique": "Optimized async store using stmatrix",
            "gain": "+1% (additional SMRs spared)"
        },
        "micro_optimization_impact": {
            "individual": "Small gains (1-2%)",
            "cumulative": "747 → 771 TFLOP/s",
            "scale": "At 30k GPUs, every 1% = massive savings"
        }
    })

    # ============================================================================
    # ADDITIONAL DEEP INSIGHTS
    # ============================================================================

    kb.add_pdf_knowledge("architectural_progression", {
        "ampere_to_hopper": "Biggest generational jump",
        "hopper_new_features": [
            "DSMEM (distributed shared memory)",
            "TMA (tensor memory accelerator)",
            "Thread block clusters",
            "Asynchronous transaction barriers",
            "Split barriers counting transactions (bytes) not just threads"
        ],
        "ampere_features": [
            "tf32 and bf16 Tensor Core support",
            "Asynchronous copy (GMEM → SMEM) with two modes",
            "Asynchronous barriers (hardware-accelerated in SMEM)",
            "CUDA task graphs",
            "Warp-level reduction instructions"
        ],
        "future_architectures": {
            "blackwell": "Next after Hopper",
            "rubin": "Future architecture",
            "forward_portability": "Understanding Hopper enables adaptation"
        }
    })

    kb.add_pdf_knowledge("practical_development_insights", {
        "profiling_tools": [
            "Nsight Compute (ncu)",
            "Occupancy calculator",
            "nvdisasm for assembly inspection",
            "ptxas with -v flag"
        ],
        "compilation_flags": {
            "o3": "Most aggressive optimization",
            "ndebug": "Turn assertions into noop",
            "arch": "Specify compute capability (e.g., sm_90a for H100)",
            "use_fast_math": "Trade accuracy for speed (fp32 focused)",
            "ptxas_options_v": "Print resource usage"
        },
        "debugging_techniques": [
            "Verify PTX/SASS matches expectations",
            "Use #pragma unroll 1 to simplify analysis",
            "Check for bank conflicts via profiler",
            "Measure arithmetic intensity",
            "Profile on actual hardware (not simulation)"
        ],
        "performance_philosophy": {
            "o_nr_not_o_n": "Nuclear reactor complexity, not algorithmic",
            "percent_matters": "1% at scale = millions saved",
            "understand_hardware": "Mental model essential",
            "local_to_global": "Focus on single block correctness"
        }
    })

    kb.add_pdf_knowledge("key_takeaways_and_philosophy", {
        "fundamental_belief": "Computers can be understood",
        "mental_model_importance": "Hardware understanding enables performance",
        "coalescing_critical": "Memory access patterns have dramatic impact",
        "hierarchy_awareness": "Keep data close to compute",
        "tile_shapes_matter": "Square tiles maximize arithmetic intensity",
        "async_is_powerful": "Overlap compute with data movement",
        "hardware_abstractions": "Tensor cores and TMA simplify and accelerate",
        "scheduling_sophistication": "Hilbert curves beat naive traversal",
        "clusters_enable_sharing": "DSMEM reduces redundant loads",
        "micro_optimizations_add_up": "Last few percent matter at scale",
        "matmul_as_training": "Understanding matmul gives toolkit for any GPU kernel",
        "transformers_bottleneck": "Most FLOPs in matmuls (MLP, attention)",
        "embarrassingly_parallel": "Natural fit for GPUs",
        "future_work": [
            "Blackwell GPU kernels",
            "Microbenchmarking experiments",
            "Multi-GPU kernels",
            "Memory consistency models"
        ]
    })

    # Save the enriched knowledge base
    print("\n" + "="*80)
    print("KNOWLEDGE BASE POPULATED FROM PDF")
    print("="*80)

    stats = kb.get_agent_statistics()
    print(f"\n📊 Knowledge Base Statistics:")
    print(f"   Total categories: {len(kb.knowledge) + len(kb.pdf_extracted_knowledge)}")
    print(f"   PDF knowledge categories: {len(kb.pdf_extracted_knowledge)}")

    print("\n📚 PDF Knowledge Categories Added:")
    for i, category in enumerate(kb.pdf_extracted_knowledge.keys(), 1):
        print(f"   {i}. {category}")

    kb.save_knowledge_base("gpu_knowledge_from_pdf.pkl")
    print(f"\n💾 Knowledge base saved: gpu_knowledge_from_pdf.pkl")

    print("\n✅ Your 102-agent team now has expert-level knowledge from the PDF!")
    print("   - GPU architecture fundamentals")
    print("   - Memory hierarchy deep dives")
    print("   - CUDA programming model")
    print("   - PTX/SASS assembly")
    print("   - Matmul kernel design (naive → SOTA)")
    print("   - Hopper async features (TMA, tensor cores, swizzling)")
    print("   - Advanced optimizations (pipelining, clusters, Hilbert curves)")

    return kb


if __name__ == "__main__":
    kb = load_nvidia_gpu_internals_knowledge()

    # Demo: Query the new knowledge
    print("\n" + "="*80)
    print("DEMO: ACCESSING PDF KNOWLEDGE")
    print("="*80)

    # Example queries
    print("\n🔍 Query: Swizzling deep dive")
    swizzle = kb.query("swizzling_deep_dive")
    if swizzle and isinstance(swizzle, dict):
        print(f"   Motivation: {swizzle.get('motivation', {}).get('problem', 'N/A')}")
        print(f"   Swizzle modes: {list(swizzle.get('swizzle_modes', {}).keys())}")

    print("\n🔍 Query: Hopper SOTA performance progression")
    sota = kb.query("hopper_sota_matmul")
    if sota and isinstance(sota, dict):
        perf = sota.get('performance_progression', {})
        print(f"   Baseline: {perf.get('warp_tiling_baseline', 'N/A')}")
        print(f"   Final: {perf.get('stmatrix_optimization', 'N/A')}")

    print("\n🔍 Query: TMA (Tensor Memory Accelerator)")
    tma = kb.query("tma_tensor_memory_accelerator")
    if tma and isinstance(tma, dict):
        print(f"   Purpose: {tma.get('purpose', 'N/A')}")
