from core.base_node import BaseNode, NodeOutput
from core.roi_calculator import ROICalculator
from typing import Any, Dict
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class LeadIntelligenceEngine(BaseNode):
    """
    NODE_4: LEAD_INTELLIGENCE_ENGINE
    Processes incoming leads, calculates ROI, scores lead quality,
    and sends real-time Slack alerts for high-priority leads.
    """

    def __init__(self):
        super().__init__("NODE_4", "Event-driven Processor")
        self.slack_client = None

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        lead_data = inputs.get("lead", {})
        self.log(f"Processing lead: {lead_data.get('name', 'Anonymous')}")
        
        # Financial processing using our core ROICalculator
        roof_size = lead_data.get("roof_size", 0)
        monthly_bill = lead_data.get("electricity_bill", 0)
        
        calculator = ROICalculator()
        roi_results = calculator.calculate(roof_size, monthly_bill)
        
        # Scoring Logic (A: Industrial, B: Commercial, C: Small Commercial/Residential)
        industry_type = lead_data.get("operation_type", "other")
        multipliers = {
            "manufacturing": 1.2,
            "cold-storage": 1.5,
            "warehousing": 1.1,
            "other": 1.0
        }
        
        effective_monthly_bill = monthly_bill * multipliers.get(industry_type, 1.0)
        
        score = "C"
        if effective_monthly_bill > 50000 and roi_results["payback_years"] < 4.5:
            score = "A"
        elif effective_monthly_bill > 15000:
            score = "B"
            
        roi_results["lead_score"] = score
        roi_results["industry"] = industry_type
        roi_results["routing"] = "Sales Dashboard" if score in ["A", "B"] else "Nurture Sequence"
        
        # Send Slack Alert for Tier A Leads
        if score == "A":
            await self._send_slack_alert(lead_data, roi_results)

        # Update global CO2 stats
        current_co2 = self.global_memory.get_state("total_co2_offset") or 0.0
        self.global_memory.update_state("total_co2_offset", current_co2 + roi_results["annual_co2_offset_tons"])

        self.global_memory.append_to_list("lead_quality", {
            "timestamp": "now", 
            "score": score, 
            "capex": roi_results["capex_estimate"],
            "industry": industry_type,
            "co2_offset": roi_results["annual_co2_offset_tons"]
        })
        
        self.log(f"Lead Scored: {score} | Payback: {roi_results['payback_years']} years | Capacity: {roi_results['capacity_kw']}kW")
        
        return NodeOutput(
            data=roi_results,
            metadata={"status": "lead_processed", "score": score, "routing": roi_results["routing"]}
        )

    async def _send_slack_alert(self, lead: Dict[str, Any], results: Dict[str, Any]):
        token = self.config.get("SLACK_TOKEN")
        if not token or "xox" not in token:
            self.log("Slack Token missing. Mocking alert to webhook...")
            return

        if not self.slack_client:
            self.slack_client = WebClient(token=token)

        try:
            message = (
                f"🚨 *New Tier A Solar Lead Found!* 🚨\n"
                f"*Name*: {lead.get('name', 'N/A')}\n"
                f"*Capacity*: {results['capacity_kw']} kW\n"
                f"*Payback*: {results['payback_years']} years\n"
                f"*Estimated CAPEX*: INR {results['capex_estimate']:,}"
            )
            self.slack_client.chat_postMessage(channel="#leads", text=message)
            self.log("Slack alert sent successfully.")
        except SlackApiError as e:
            self.log(f"Slack Error: {e.response['error']}")
