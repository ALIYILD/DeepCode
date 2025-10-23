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
