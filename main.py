import asyncio
from core.orchestrator import MasterOrchestrator
from agents.digital_asset_engine import DigitalAssetEngine
from agents.seo_intelligence_engine import SEOIntelligenceEngine
from agents.authority_content_engine import AuthorityContentEngine
from agents.lead_intelligence_engine import LeadIntelligenceEngine
from agents.governance_risk_engine import GovernanceRiskEngine
from agents.analytics_dashboard_engine import AnalyticsDashboardEngine
from agents.carbon_reporting_engine import CarbonReportingEngine
from agents.social_distribution_swarm import SocialDistributionSwarm
from core.optimization_engine import StrategicReallocationEngine
from core.phase_manager import BudgetPhaseManager

async def main():
    orchestrator = MasterOrchestrator()
    
    # Register all nodes
    orchestrator.register_node(DigitalAssetEngine())
    orchestrator.register_node(SEOIntelligenceEngine())
    orchestrator.register_node(AuthorityContentEngine())
    orchestrator.register_node(LeadIntelligenceEngine())
    orchestrator.register_node(GovernanceRiskEngine())
    orchestrator.register_node(AnalyticsDashboardEngine())
    orchestrator.register_node(CarbonReportingEngine())
    orchestrator.register_node(SocialDistributionSwarm())
    orchestrator.register_node(StrategicReallocationEngine())
    orchestrator.register_node(BudgetPhaseManager())

    print("\n--- Starting Manokamana Solar Agentic Engine Simulation ---\n")

    # 1. SEO Intelligence
    print("\nStep 1: SEO Analysis")
    await orchestrator.run_node("NODE_2")

    # 2. Content Generation with Risk Check
    print("\nStep 2: Content Generation and Publishing")
    topic = "Solar ROI for Industrial Clients"
    # Execute Content Engine (NODE_3)
    content_output = await orchestrator.run_node("NODE_3", {"topic": topic, "platform": "blog"})
    draft_data = content_output.data # {draft, platform, topic}
    
    # Execute Risk Check (NODE_5)
    risk_output = await orchestrator.run_node("NODE_5", {"content": draft_data["draft"], "type": "blog"})
    
    # If safe, publish via Digital Asset Engine (NODE_1)
    if risk_output.metadata["status"] == "cleared":
        print("[Simulation] Content cleared by Governance. Publishing...")
        publish_input = {
            "action": "publish_blog",
            "content_draft": {
                "title": topic,
                "draft": draft_data["draft"]
            }
        }
        await orchestrator.run_node("NODE_1", publish_input)
    else:
        print("[Simulation] Content blocked by Governance.")

    print("\nStep 3: Site Deployment")
    await orchestrator.run_node("NODE_1", {"action": "deploy_site"})
    
    # 3. Lead Processing and Phase Transition
    print("\nStep 4: Lead Processing and Phase Transition Simulation")
    # Simulate 6 leads to trigger Phase 2
    for i in range(6):
        # NODE_4 Processes lead and puts it in memory
        lead_result = await orchestrator.run_node("NODE_4", {
            "lead": {
                "name": f"Industrial Client {i}",
                "roof_size": 25000,
                "electricity_bill": 150000,
                "operation_type": "manufacturing"
            }
        })

        # Step 4.2: If Tier A, Generate Carbon Environmental Report (NODE_9)
        if lead_result.metadata.get("score") == "A":
            await orchestrator.run_node("NODE_9", {
                "lead": {"name": f"Industrial Client {i}"},
                "roi_results": lead_result.data
            })
    
    await orchestrator.run_node("NODE_8") # Check phase

    # 4. Analytics and Optimization
    print("\nStep 5: Final Analytics and Optimization")
    await orchestrator.run_node("NODE_6")
    await orchestrator.run_node("NODE_7")

    # 5. Marketing Swarm
    print("\nStep 6: Social Distribution Swarm")
    await orchestrator.run_node("NODE_10")

    print("\n--- Simulation Complete ---\n")

if __name__ == "__main__":
    asyncio.run(main())
