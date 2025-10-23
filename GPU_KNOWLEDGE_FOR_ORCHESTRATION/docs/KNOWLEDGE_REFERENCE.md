# 📖 GPU Knowledge Reference

Complete reference of available GPU knowledge for your agents.

---

## 📊 Knowledge Categories

### 24 PDF-Derived Categories

1. **gpu_architecture_fundamentals**
2. **memory_subsystem_deep_dive**
3. **compute_architecture_details**
4. **performance_characteristics_detailed**
5. **cuda_programming_model_detailed**
6. **gpu_assembly_languages**
7. **ptx_sass_analysis_insights**
8. **matmul_fundamentals**
9. **naive_matmul_analysis**
10. **roofline_model**
11. **warp_tiling_method**
12. **hopper_sota_matmul**
13. **tma_tensor_memory_accelerator**
14. **swizzling_deep_dive**
15. **tensor_cores_wgmma**
16. **pipelining_optimizations**
17. **multiple_consumers_and_scaling**
18. **persistent_kernels**
19. **scheduling_strategies**
20. **thread_block_clusters**
21. **final_optimizations**
22. **architectural_progression**
23. **practical_development_insights**
24. **key_takeaways_and_philosophy**

---

## 🔍 Quick Reference

### Agent Interface

```python
from gpu_knowledge import AgentKnowledgeInterface

agent = AgentKnowledgeInterface(agent_id=1)
```

#### Methods

**ask(query: str) -> Any**
```python
result = agent.ask("hopper_sota_matmul")
```

**get_optimization_for(algorithm: str) -> List[str]**
```python
strategies = agent.get_optimization_for("memory_bound_kernels")
```

**get_architecture_detail(arch: str, detail: str) -> Any**
```python
features = agent.get_architecture_detail("ampere", "key_features")
```

**get_best_practice(category: str) -> List[str]**
```python
practices = agent.get_best_practice("kernel_design")
```

---

## 📚 Detailed Categories

### 1. GPU Architecture Fundamentals

**Query**: `"gpu_architecture_fundamentals"`

**Contains**:
- Hopper H100 specifications
- Memory hierarchy overview
- Compute unit organization
- SM structure and capabilities

**Example**:
```python
arch = agent.ask("gpu_architecture_fundamentals")
h100 = arch['h100_specifics']
print(f"Total SMs: {h100['total_sms']}")  # 132
```

---

### 2. Memory Subsystem Deep Dive

**Query**: `"memory_subsystem_deep_dive"`

**Contains**:
- GMEM (DRAM) model
- SMEM (SRAM) model
- Bank conflicts
- Coalescing patterns
- L1 cache model

**Example**:
```python
memory = agent.ask("memory_subsystem_deep_dive")
bank_conflicts = memory['smem_sram_model']['bank_conflicts']
print(f"Impact: {bank_conflicts['impact']}")  # N-way conflict = N serialized accesses
```

---

### 3. Hopper SOTA Matmul

**Query**: `"hopper_sota_matmul"`

**Contains**:
- Performance progression (32 → 771 TFLOP/s)
- Optimization techniques
- Feature usage (TMA, Tensor Cores, etc.)

**Example**:
```python
hopper = agent.ask("hopper_sota_matmul")
final = hopper['performance_progression']['stmatrix_optimization']
print(f"Final performance: {final}")  # 771 TFLOP/s (~107% of cuBLAS)
```

---

### 4. TMA (Tensor Memory Accelerator)

**Query**: `"tma_tensor_memory_accelerator"`

**Contains**:
- Purpose and capabilities
- Setup requirements
- Async copy patterns
- Barrier synchronization
- Memory consistency

**Example**:
```python
tma = agent.ask("tma_tensor_memory_accelerator")
print(f"Purpose: {tma['purpose']}")
# Asynchronous data transfers between GMEM ↔ SMEM and SMEM ↔ SMEM
```

---

### 5. Swizzling Deep Dive

**Query**: `"swizzling_deep_dive"`

**Contains**:
- Motivation and benefits
- Swizzle modes (128B, 64B, 32B)
- XOR-based patterns
- Mechanism details
- Transpose benefits

**Example**:
```python
swizzle = agent.ask("swizzling_deep_dive")
modes = swizzle['swizzle_modes']
print(f"Available modes: {list(modes.keys())}")  # ['128B', '64B', '32B']
```

---

### 6. Tensor Cores & WGMMA

**Query**: `"tensor_cores_wgmma"`

**Contains**:
- MMA instruction evolution
- WGMMA shapes (m64nNk16)
- Operand placement
- Accumulator distribution
- Instruction patterns

**Example**:
```python
tc = agent.ask("tensor_cores_wgmma")
shapes = tc['wgmma_shapes']
print(f"Format: {shapes['format']}")  # m64nNk16 where N ∈ {8, 16, 24, ..., 256}
```

---

### 7. Scheduling Strategies

**Query**: `"scheduling_strategies"`

**Contains**:
- Naive schedule
- Block-wise cache-aware
- Hilbert curve scheduling
- Space-filling curves

**Example**:
```python
sched = agent.ask("scheduling_strategies")
hilbert = sched['hilbert_curve_schedule']
print(f"Performance: {hilbert['performance_gain']}")  # 758 → 764 TFLOP/s
```

---

### 8. Roofline Model

**Query**: `"roofline_model"`

**Contains**:
- Definition
- Arithmetic intensity
- Ridge point calculation
- Memory-bound vs compute-bound regions

**Example**:
```python
roofline = agent.ask("roofline_model")
print(f"Ridge point (H100): {roofline['h100_ridge']}")  # ~410
```

---

## 🎯 Common Query Patterns

### Pattern 1: Architecture Queries

```python
# Get full architecture
arch = agent.ask("gpu_architecture_fundamentals")

# Get specific component
memory_hierarchy = arch['memory_hierarchy']
l2 = memory_hierarchy['l2_cache']

# Access nested data
latency = l2['latency_cycles']  # 200
```

### Pattern 2: Performance Queries

```python
# Get performance progression
hopper = agent.ask("hopper_sota_matmul")
progression = hopper['performance_progression']

# Iterate through stages
for stage, perf in progression.items():
    print(f"{stage}: {perf}")
```

### Pattern 3: Optimization Queries

```python
# Get optimization strategies
memory_bound = agent.ask("optimization_patterns.memory_bound_kernels")
strategies = memory_bound['strategies']

# Apply each strategy
for strategy in strategies:
    apply_optimization(strategy)
```

---

## 💡 Best Practices

### 1. Cache Frequently Used Knowledge

```python
class SmartAgent:
    def __init__(self, agent_id):
        self.gpu_knowledge = AgentKnowledgeInterface(agent_id)

        # Cache at initialization
        self.hopper_knowledge = self.gpu_knowledge.ask("hopper_sota_matmul")
        self.tma_knowledge = self.gpu_knowledge.ask("tma_tensor_memory_accelerator")
```

### 2. Use Specific Queries

```python
# Less efficient - returns entire category
all_memory = agent.ask("memory_subsystem_deep_dive")

# More efficient - returns specific sub-topic
bank_conflicts = agent.ask("memory_subsystem_deep_dive.smem_sram_model.bank_conflicts")
```

### 3. Validate Knowledge Exists

```python
result = agent.ask("some_topic")
if result:
    process(result)
else:
    print("Knowledge not found")
```

---

## 🔍 Advanced Queries

### Nested Field Access

```python
# Deep nested query
swizzle_function = agent.ask(
    "swizzling_deep_dive.swizzle_function_decode.swizzle_3_4_3.operation"
)
```

### Bulk Loading

```python
# Load multiple topics at once
topics = [
    "tma_tensor_memory_accelerator",
    "swizzling_deep_dive",
    "tensor_cores_wgmma",
    "hopper_sota_matmul"
]

knowledge_bundle = {
    topic: agent.ask(topic)
    for topic in topics
}
```

---

## 📊 Knowledge Statistics

### Get Usage Stats

```python
from gpu_knowledge import SharedGPUKnowledgeBase

kb = SharedGPUKnowledgeBase()
stats = kb.get_agent_statistics()

print(f"Total queries: {stats['total_queries']}")
print(f"Active agents: {stats['unique_agents']}")
print(f"Queries per agent: {stats['queries_per_agent']}")
```

---

## 🚀 Quick Examples

### Example 1: Optimize Kernel

```python
agent = AgentKnowledgeInterface(1)

# Get optimization techniques
hopper = agent.ask("hopper_sota_matmul")
techniques = hopper['new_features_used']

# Apply each technique
for technique in techniques:
    apply(technique)
```

### Example 2: Design Memory Layout

```python
agent = AgentKnowledgeInterface(2)

# Get swizzling info
swizzle = agent.ask("swizzling_deep_dive")
mode = swizzle['swizzle_modes']['128B']

# Get bank conflict info
conflicts = agent.ask("memory_subsystem_deep_dive.smem_sram_model.bank_conflicts")

# Design layout
layout = design_with_knowledge(mode, conflicts)
```

### Example 3: Analyze Performance

```python
agent = AgentKnowledgeInterface(3)

# Get roofline model
roofline = agent.ask("roofline_model")

# Get performance characteristics
perf = agent.ask("performance_characteristics_detailed")

# Analyze
analysis = analyze_with_knowledge(roofline, perf)
```

---

**Complete API reference for GPU knowledge system! Use this as your query guide! 📚**
