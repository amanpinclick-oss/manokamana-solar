from core.base_node import BaseNode, NodeOutput
from typing import Any, Dict

class StrategicReallocationEngine(BaseNode):
    """
    NODE_7: STRATEGIC_REALLOCATION_ENGINE
    Triggered monthly to update topic weights based on lead conversion performance.
    """

    def __init__(self):
        super().__init__("NODE_7", "Optimization Engine")

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        self.log("Running strategic reallocation based on lead performance...")
        
        # 1. Get current state
        current_weights = self.global_memory.get_state("topic_weights") or {"industrial": 0.4, "commercial": 0.3, "warehouse": 0.3}
        leads = self.global_memory.get_list("lead_quality")
        
        # 2. Count lead occurrences by topic (simulated by looking for keywords in lead metadata/projections)
        # In a real system, we'd have a 'topic' field on the lead. 
        # Here we simulate by looking at CAPEX potential or just frequency.
        topic_performance = {"industrial": 0, "commercial": 0, "warehouse": 0}
        
        for lead in leads:
            # Simple heuristic: If capex is high, it's likely industrial. 
            # If medium, likely warehouse. If low, commercial.
            capex = lead.get("capex", 0)
            if capex > 2000000:
                topic_performance["industrial"] += 1
            elif capex > 800000:
                topic_performance["warehouse"] += 1
            else:
                topic_performance["commercial"] += 1
        
        # 3. Calculate new weights (Normalize)
        total_leads = len(leads) if leads else 1
        new_weights = {}
        for topic, count in topic_performance.items():
            # Blend 50% current weight with 50% performance weight for stability
            perf_weight = count / total_leads
            new_weights[topic] = round((current_weights.get(topic, 0.33) * 0.5) + (perf_weight * 0.5), 2)
        
        # Ensure they sum closer to 1 (normalization check)
        total = sum(new_weights.values())
        if total > 0:
            new_weights = {k: round(v/total, 2) for k, v in new_weights.items()}

        self.global_memory.update_state("topic_weights", new_weights)
        self.log(f"Optimization complete. New topic weights: {new_weights}")
        
        return NodeOutput(
            data={"new_weights": new_weights, "performance_stats": topic_performance},
            metadata={"status": "reallocation_complete"}
        )
