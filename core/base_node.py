import abc
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class NodeOutput:
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""

class BaseNode(abc.ABC):
    """
    Abstract base class for all nodes in the Manokamana Solar Agentic Engine.
    """

    def __init__(self, node_id: str, node_type: str):
        self.node_id = node_id
        self.node_type = node_type
        self.global_memory = None  # Will be set by Orchestrator
        self.config = None         # Will be set by Orchestrator

    @abc.abstractmethod
    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        """
        Execute the node logic.
        """
        pass

    def log(self, message: str):
        print(f"[{self.node_id}] {message}")

    def set_memory(self, memory: Any):
        self.global_memory = memory

    def set_config(self, config: Any):
        self.config = config
