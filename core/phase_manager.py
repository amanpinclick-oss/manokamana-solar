from core.base_node import BaseNode, NodeOutput
from typing import Any, Dict

class BudgetPhaseManager(BaseNode):
    """
    NODE_8: BUDGET_PHASE_MANAGER
    Manages budget scaling (STATE_1 to STATE_4) based on verified lead counts and conversion potential.
    """

    def __init__(self):
        super().__init__("NODE_8", "State Machine")

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        current_phase = self.global_memory.get_state("budget_phase") or "STATE_1"
        leads = self.global_memory.get_list("lead_quality")
        lead_count = len(leads)
        
        # Calculate 'qualified' lead count (Tier A and B)
        qualified_leads = len([l for l in leads if l.get("score") in ["A", "B"]])
        
        self.log(f"Phase Manager: Current Phase {current_phase}, Qualified Leads {qualified_leads}")
        
        new_phase = current_phase
        
        # Configurable thresholds
        p2_threshold = self.config.get_int("MIN_LEADS_FOR_PHASE_2", 5)
        p3_threshold = self.config.get_int("MIN_LEADS_FOR_PHASE_3", 15)
        p4_threshold = self.config.get_int("MIN_LEADS_FOR_PHASE_4", 50)

        if current_phase == "STATE_1" and qualified_leads >= p2_threshold:
            new_phase = "STATE_2"
            self.log("Scaling: Transitioning to Phase 2 (INR 10k budget enabled)")
        elif current_phase == "STATE_2" and qualified_leads >= p3_threshold:
            new_phase = "STATE_3"
            self.log("Scaling: Transitioning to Phase 3 (INR 50k budget enabled)")
        elif current_phase == "STATE_3" and qualified_leads >= p4_threshold:
            new_phase = "STATE_4"
            self.log("Scaling: Transitioning to Phase 4 (INR 1L+ budget enabled)")
            
        if new_phase != current_phase:
            self.global_memory.update_state("budget_phase", new_phase)
            self.global_memory.log_event("NODE_8", "phase_transition", {"from": current_phase, "to": new_phase})
            
        return NodeOutput(
            data={"current_phase": new_phase, "qualified_count": qualified_leads},
            metadata={"status": "phase_checked", "transition": new_phase != current_phase}
        )
