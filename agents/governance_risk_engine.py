from core.base_node import BaseNode, NodeOutput
from typing import Any, Dict

class GovernanceRiskEngine(BaseNode):
    """
    NODE_5: GOVERNANCE_RISK_ENGINE
    Monitors all content and activities for policy compliance and legal misrepresentation.
    """

    def __init__(self):
        super().__init__("NODE_5", "Monitor / Gatekeeper")

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        content = inputs.get("content", "")
        content_type = inputs.get("type", "unknown")
        
        self.log(f"Analyzing {content_type} risk...")
        
        risk_score = 0
        flags = []

        # Simple simulation of risk detection logic
        if "guaranteed ROI" in content.lower():
            risk_score += 40
            flags.append("Financial Claim Risk: Excessive ROI guarantee")
        
        if "free government subsidy" in content.lower():
            risk_score += 30
            flags.append("Policy Risk: Unverified subsidy mention")

        if len(content) < 50 and content_type == "blog":
            risk_score += 20
            flags.append("SEO Risk: Thin content")

        # Sustainability Alignment Check
        co2_limit = inputs.get("co2_offset_limit", 1500) # Default limit for standard industrial
        actual_co2 = inputs.get("actual_co2_offset", 0)
        
        if actual_co2 > co2_limit:
            risk_score += 50
            flags.append("Sustainability Risk: CO2 offset claim exceeds industrial baseline. Requires manual audit.")

        self.global_memory.update_state("current_risk_score", risk_score)
        self.log(f"Risk Score: {risk_score} | Flags: {flags}")

        block_threshold = self.config.get_int("RISK_THRESHOLD_BLOCK", 70)
        return NodeOutput(
            data={"risk_score": risk_score, "flags": flags},
            metadata={"status": "cleared" if risk_score < block_threshold else "flagged"}
        )
