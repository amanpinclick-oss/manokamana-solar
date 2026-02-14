import asyncio
import sys
from core.orchestrator import MasterOrchestrator
from agents.digital_asset_engine import DigitalAssetEngine
from agents.seo_intelligence_engine import SEOIntelligenceEngine
from agents.authority_content_engine import AuthorityContentEngine
from agents.lead_intelligence_engine import LeadIntelligenceEngine
from agents.governance_risk_engine import GovernanceRiskEngine
from agents.analytics_dashboard_engine import AnalyticsDashboardEngine
from core.optimization_engine import StrategicReallocationEngine
from core.phase_manager import BudgetPhaseManager

async def production_launch():
    print("\n🚀 --- Manokamana Solar Agentic Engine: PRODUCTION LAUNCH --- 🚀\n")
    
    orchestrator = MasterOrchestrator()
    
    # Register all performance nodes
    orchestrator.register_node(DigitalAssetEngine())
    orchestrator.register_node(SEOIntelligenceEngine())
    orchestrator.register_node(AuthorityContentEngine())
    orchestrator.register_node(LeadIntelligenceEngine())
    orchestrator.register_node(GovernanceRiskEngine())
    orchestrator.register_node(AnalyticsDashboardEngine())
    orchestrator.register_node(StrategicReallocationEngine())
    orchestrator.register_node(BudgetPhaseManager())

    # 1. Initial High-Priority Cycle (SEO -> Content -> Publish)
    print("\n[Launch] Running initial high-priority SEO and Content cycle...")
    
    # Analyze SEO Trends
    await orchestrator.run_node("NODE_2")
    
    # Pick a high-priority topic and generate content
    topic = "Industrial Solar Subsidy 2026 India"
    content_output = await orchestrator.run_node("NODE_3", {"topic": topic, "platform": "blog"})
    
    # Governance Gate
    risk_output = await orchestrator.run_node("NODE_5", {"content": content_output.data["draft"], "type": "blog"})
    
    if risk_output.metadata.get("status") == "cleared":
        await orchestrator.run_node("NODE_1", {
            "action": "publish_blog", 
            "content_draft": {"title": topic, "draft": content_output.data["draft"]}
        })
        await orchestrator.run_node("NODE_1", {"action": "deploy_site"})
    
    print("\n[Launch] Initial cycle complete. Entering scheduled background loop.")
    print("Press Ctrl+C to stop the engine.\n")

    # 2. Enter Continuous Intelligence Loop
    try:
        await orchestrator.start_scheduled_loop()
    except KeyboardInterrupt:
        orchestrator.stop()
        print("\n[Launch] Engine stopped by user.")
    except Exception as e:
        print(f"\n[Launch] Critical Error: {e}")
        orchestrator.stop()

if __name__ == "__main__":
    try:
        asyncio.run(production_launch())
    except KeyboardInterrupt:
        pass
