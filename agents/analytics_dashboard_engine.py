from core.base_node import BaseNode, NodeOutput
from core.report_generator import ReportGenerator
import os
from typing import Any, Dict

class AnalyticsDashboardEngine(BaseNode):
    """
    NODE_6: ANALYTICS_DASHBOARD_ENGINE
    Aggregates data from global memory and generates performance reports using ReportGenerator.
    """

    def __init__(self):
        super().__init__("NODE_6", "Aggregator")
        self.reporter = None

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        self.log("Aggregating system analytics...")
        
        ga4_property_id = self.config.get("GA4_PROPERTY_ID", "123456789")
        self.log(f"Consuming GA4 Property ID: {ga4_property_id}")
        
        if not self.reporter:
            # Initialize reporter with project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(project_root, "reports")
            self.reporter = ReportGenerator(reports_dir)
        
        # 1. Gather metrics from memory
        # Note: Lead data and asset data are stored as lists
        leads = self.global_memory.get_state("lead_quality") or []
        assets = self.global_memory.get_state("published_assets") or []
        risk_score = self.global_memory.get_state("current_risk_score") or 0
        
        summary = {
            "total_leads": len(leads),
            "tier_counts": {
                "A": len([l for l in leads if l.get("score") == "A"]),
                "B": len([l for l in leads if l.get("score") == "B"]),
                "C": len([l for l in leads if l.get("score") == "C"])
            },
            "published_assets_count": len(assets),
            "current_risk_health": "Healthy" if risk_score < 50 else "High Risk",
            "total_capex_potential": sum([l.get("capex", 0) for l in leads]),
            "timestamp": inputs.get("timestamp", "now")
        }
        
        # 2. Generate structured reports
        json_path = self.reporter.generate_json(summary, "system_summary")
        csv_path = self.reporter.generate_csv(leads, "leads_detailed")
        
        self.log(f"Analytics Summary: {len(leads)} leads, {len(assets)} assets.")
        self.log(f"Reports saved to: {json_path} and {csv_path}")
        
        return NodeOutput(
            data={"summary": summary, "files": {"json": json_path, "csv": csv_path}},
            metadata={"status": "reports_generated", "lead_count": len(leads)}
        )
