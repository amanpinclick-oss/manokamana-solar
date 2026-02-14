from core.base_node import BaseNode, NodeOutput
import os
import json
from typing import Any, Dict

class SocialDistributionSwarm(BaseNode):
    """
    NODE_10: SOCIAL_DISTRIBUTION_SWARM
    Generates multi-platform social media drafts to amplify engine insights and lead wins.
    """

    def __init__(self):
        super().__init__("NODE_10", "Marketing Swarm")

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        self.log("Social Swarm initialized. Reviewing recent wins...")
        
        # 1. Gather context from memory
        leads = self.global_memory.get_state("lead_quality") or []
        assets = self.global_memory.get_state("published_assets") or []
        total_co2 = self.global_memory.get_state("total_co2_offset") or 0.0
        
        drafts = []

        # 2. Strategy A: Amplify Tier A Lead Wins (Anonymous)
        tier_a_leads = [l for l in leads if l.get("score") == "A"]
        for lead in tier_a_leads:
            industry = lead.get("industry", "Manufacturing").replace("-", " ").title()
            drafts.append({
                "platform": "LinkedIn",
                "campaign": "Industrial Growth",
                "content": (
                    f"🚀 Huge Solar Win for the {industry} Sector! 🚀\n\n"
                    f"We just analyzed a new industrial site and found a massive solar ROI potential.\n"
                    f"⚡ Estimated Capacity: {lead.get('co2_offset', 0) * 1.2:.1f} kW peak\n"
                    f"🌿 Annual Carbon Offset: {lead.get('co2_offset', 0):.1f} Tons CO2\n\n"
                    f"Solar isn't just 'green'—it's a competitive advantage for Indian industry. #SolarROI #ManokamanaSolar #GreenEnergy"
                )
            })

        # 3. Strategy B: Global Sustainability Pulse
        if total_co2 > 0:
            drafts.append({
                "platform": "WhatsApp",
                "campaign": "Sustainability Pulse",
                "content": (
                    f"*Manokamana Solar Update*: Engine has now identified a total of *{total_co2:.1f} Tons* of annual CO2 potential across scouted sites! 🌍\n\n"
                    f"That's equivalent to planting over *{int(total_co2 * 45)}* trees. Join the movement. Reply 'ROI' for a free custom audit."
                )
            })

        # 4. Strategy C: Asset Expansion (Blog teaser)
        if assets:
            latest = assets[-1]
            drafts.append({
                "platform": "X (Twitter)",
                "campaign": "Thought Leadership",
                "content": (
                    f"New Market Insight: '{latest['title']}' is now live on the Manokamana Engine dashboard.\n\n"
                    f"Why industrial leaders are moving to solar in 2026. 🧵👇\n"
                    f"#SolarIndia #CleanTech #IndustryInsights"
                )
            })

        # 5. Save drafts to file system
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        social_dir = os.path.join(project_root, "content", "social")
        if not os.path.exists(social_dir):
            os.makedirs(social_dir)

        filepath = os.path.join(social_dir, "social_drafts_current.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(drafts, f, indent=4)

        self.log(f"Social Swarm generated {len(drafts)} drafts. Saved to content/social/")

        return NodeOutput(
            data={"drafts": drafts},
            metadata={"status": "drafting_complete", "count": len(drafts)}
        )
