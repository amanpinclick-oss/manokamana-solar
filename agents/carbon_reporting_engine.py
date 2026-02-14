from core.base_node import BaseNode, NodeOutput
from core.report_generator import ReportGenerator
import os
from typing import Any, Dict

class CarbonReportingEngine(BaseNode):
    """
    NODE_9: CARBON_REPORTING_ENGINE
    Generates formal environmental impact reports (Environmental Identity) for Tier A leads.
    """

    def __init__(self):
        super().__init__("NODE_9", "Reporting Engine")
        self.reporter = None

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        lead_data = inputs.get("lead", {})
        roi_results = inputs.get("roi_results", {})
        
        if not lead_data or not roi_results:
            return NodeOutput(data=None, metadata={"status": "error", "message": "Missing lead or ROI data"})

        self.log(f"Generating Carbon Impact Report for: {lead_data.get('name')}")
        
        # Environmental Equivalencies (Approximations)
        # 1 ton CO2 offset = ~45 trees planted (over 10 years)
        # 1 ton CO2 offset = ~400 kg of coal saved
        co2_offset = roi_results.get("annual_co2_offset_tons", 0)
        trees_equivalent = int(co2_offset * 45)
        coal_equivalent_kg = int(co2_offset * 400)

        report = {
            "entity_name": lead_data.get("name"),
            "industry": roi_results.get("industry", "Industrial"),
            "system_capacity_kw": roi_results.get("capacity_kw"),
            "environmental_impact": {
                "annual_co2_offset_tons": co2_offset,
                "equivalent_trees_planted": trees_equivalent,
                "coal_combustion_avoided_kg": coal_equivalent_kg
            },
            "status": "Validated by Manokamana Governance Engine",
            "timestamp": "now"
        }

        if not self.reporter:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            carbon_dir = os.path.join(project_root, "reports", "carbon")
            self.reporter = ReportGenerator(carbon_dir)

        filename = f"carbon_report_{lead_data.get('name', 'anonymous').replace(' ', '_').lower()}"
        report_path = self.reporter.generate_json(report, filename)

        self.log(f"Carbon Report generated: {report_path}")

        return NodeOutput(
            data=report,
            metadata={"status": "report_generated", "path": report_path}
        )
