import asyncio
from typing import Dict, List, Any
from core.base_node import BaseNode, NodeOutput
from core.memory import GlobalMemory
from core.config_loader import ConfigLoader

class MasterOrchestrator:
    """
    NODE_0: MASTER_ORCHESTRATOR
    Responsible for maintaining global state, triggering nodes, and managing phase transitions.
    """

    def __init__(self):
        self.memory = GlobalMemory()
        self.config = ConfigLoader()
        self.nodes: Dict[str, BaseNode] = {}
        self.is_running = False

    def register_node(self, node: BaseNode):
        node.set_memory(self.memory)
        node.set_config(self.config)
        self.nodes[node.node_id] = node
        print(f"[Orchestrator] Registered node: {node.node_id} ({node.node_type})")

    async def run_node(self, node_id: str, inputs: Dict[str, Any] = None) -> NodeOutput:
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not registered.")
        
        node = self.nodes[node_id]
        print(f"[Orchestrator] Triggering node: {node_id}")
        
        # Risk Gate Check (NODE_5)
        if node_id != "NODE_5" and "NODE_5" in self.nodes:
            risk_score = self.memory.get_state("current_risk_score") or 0
            if risk_score > 70:
                print(f"[Orchestrator] BLOCKED: Node {node_id} execution halted due to high risk score ({risk_score}).")
                return NodeOutput(data=None, metadata={"status": "blocked", "risk_score": risk_score})

        output = await node.run(inputs or {})
        self.memory.log_event(node_id, "execution_success", {"output_metadata": output.metadata})
        return output

    async def start_scheduled_loop(self):
        """
        Main execution loop for scheduled tasks.
        """
        self.is_running = True
        print("[Orchestrator] Starting MASTER_ORCHESTRATOR loop...")
        
        while self.is_running:
            # Example: Daily system check
            await self.run_node("NODE_6") # Analytics Layer
            
            # Weekly Publishing Cycle (Simulated)
            # This would be triggered by actual time checks
            
            # Risk Threshold Breach Check
            risk_score = self.memory.get_state("current_risk_score") or 0
            if risk_score > 50:
                self.memory.log_event("NODE_0", "high_risk_alert", {"risk_score": risk_score})
            
            await asyncio.sleep(60) # Wait for next tick

    def stop(self):
        self.is_running = False
        print("[Orchestrator] Stopping MASTER_ORCHESTRATOR.")
