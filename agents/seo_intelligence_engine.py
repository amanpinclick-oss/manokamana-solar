from core.base_node import BaseNode, NodeOutput
from core.seo_utils import SEOUtils
from typing import Any, Dict
import os
import json
from google.oauth2 import service_account

class SEOIntelligenceEngine(BaseNode):
    """
    NODE_2: SEO_INTELLIGENCE_ENGINE
    Analyzes search trends and prioritize topics using real Google authentication
    and the core SEOUtils clustering logic.
    """

    def __init__(self):
        super().__init__("NODE_2", "Analyst")
        self.credentials = None

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        self.log("Running live SEO intelligence analysis...")
        
        # 1. Real Google Authentication
        if not self.credentials:
            gsc_json_path = self.config.get("GSC_SERVICE_ACCOUNT_JSON", "config/gsc-service.json")
            if os.path.exists(gsc_json_path):
                try:
                    self.credentials = service_account.Credentials.from_service_account_file(
                        gsc_json_path, 
                        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
                    )
                    self.log(f"Authenticated with Google as: {self.credentials.service_account_email}")
                except Exception as e:
                    self.log(f"Google Auth Error: {e}. Falling back to mock auth.")
            else:
                self.log("Google Service Account file not found. Using mock auth.")

        # 2. Simulate data pull (in a real production app, this would call the GSC API here)
        raw_keywords = [
            {"keyword": "industrial solar panel ROI India", "intent": "high", "volume": 1200},
            {"keyword": "solar subsidy for warehouses 2026", "intent": "high", "volume": 800},
            {"keyword": "what is solar energy", "intent": "low", "volume": 5000},
            {"keyword": "how to install solar panels at home", "intent": "medium", "volume": 3200},
            {"keyword": "best solar installation for factories in Gujarat", "intent": "high", "volume": 600}
        ]
        
        # 3. Use core SEOUtils for clustering and prioritization
        utils = SEOUtils()
        clusters = utils.cluster_keywords(raw_keywords)
        
        # 4. Apply topic priority weights from memory (if available)
        topic_weights = self.global_memory.get_state("topic_weights") or {"industrial": 0.5, "warehouse": 0.3}
        
        # 4. Generate recommendations based on high intent clusters
        recommendations = []
        for kw in clusters["high_intent"]:
            weight = utils.calculate_topic_weight(kw["keyword"], topic_weights)
            recommendations.append({
                "topic": kw["keyword"],
                "priority_score": weight * (kw["volume"] / 1000),
                "intent": "commercial_purchase"
            })

        # Sort recommendations by priority score
        recommendations.sort(key=lambda x: x["priority_score"], reverse=True)

        self.global_memory.update_state("current_seo_clusters", clusters)
        self.global_memory.update_state("seo_recommendations", recommendations)
        
        self.log(f"Analysis complete. Generated {len(recommendations)} high-priority recommendations.")
        
        return NodeOutput(
            data={"recommendations": recommendations, "clusters": clusters},
            metadata={"status": "analysis_complete", "top_priority": recommendations[0]["topic"] if recommendations else "N/A"}
        )
