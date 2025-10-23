#!/bin/bash
# create_gpu_knowledge_package.sh
# Run this in the DeepCode directory

echo "Creating GPU Knowledge Python Package..."

# Create package structure
mkdir -p gpu_knowledge_package/gpu_knowledge
cd gpu_knowledge_package

# Copy core files
cp ../shared_gpu_knowledge_base.py gpu_knowledge/
cp ../gpu_expert_agent.py gpu_knowledge/
cp ../gpu_agent_team.py gpu_knowledge/
cp ../gpu_knowledge_from_pdf.pkl gpu_knowledge/
cp ../load_pdf_knowledge.py gpu_knowledge/

# Create __init__.py
cat > gpu_knowledge/__init__.py << 'EOF'
"""
GPU Expert Knowledge System for AI Agents
"""

from .shared_gpu_knowledge_base import (
    SharedGPUKnowledgeBase,
    AgentKnowledgeInterface
)
from .gpu_expert_agent import GPUExpertAgent
from .gpu_agent_team import (
    CUDAOptimizationAgent,
    MemoryOptimizationAgent,
    PerformanceProfilingAgent,
    GPUAgentTeam
)

__version__ = '1.0.0'

__all__ = [
    'SharedGPUKnowledgeBase',
    'AgentKnowledgeInterface',
    'GPUExpertAgent',
    'CUDAOptimizationAgent',
    'MemoryOptimizationAgent',
    'PerformanceProfilingAgent',
    'GPUAgentTeam'
]
EOF

# Create setup.py
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name='gpu-knowledge',
    version='1.0.0',
    description='GPU Expert Knowledge System for Multi-Agent AI Teams',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    package_data={
        'gpu_knowledge': ['*.pkl'],
    },
    install_requires=[
        # Add any dependencies here
    ],
    python_requires='>=3.8',
)
EOF

# Create README
cat > README.md << 'EOF'
# GPU Knowledge Package

GPU Expert Knowledge System extracted from "Inside NVIDIA GPUs" for AI agent teams.

## Installation

```bash
pip install -e .
```

## Usage

```python
from gpu_knowledge import AgentKnowledgeInterface

agent = AgentKnowledgeInterface(agent_id=1)
knowledge = agent.ask("hopper_sota_matmul")
```
EOF

echo ""
echo "✅ Package created in gpu_knowledge_package/"
echo ""
echo "To install in your orchestration repo:"
echo "  cd gpu_knowledge_package"
echo "  pip install -e ."
echo ""
echo "Or create a wheel:"
echo "  python setup.py bdist_wheel"
echo "  # Then install the .whl file in your main repo"
