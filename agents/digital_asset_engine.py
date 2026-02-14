import os
import json
import datetime
from core.base_node import BaseNode, NodeOutput
from core.site_builder import SiteBuilder

class DigitalAssetEngine(BaseNode):
    """
    NODE_1: DIGITAL_ASSET_ENGINE
    Handles website deployment, blog publishing, and structured data.
    Now integrated with SiteBuilder for real file output.
    """

    def __init__(self):
        super().__init__("NODE_1", "Builder / Publisher")
        self.builder = None

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        if not self.builder:
            # Initialize builder with project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.builder = SiteBuilder(project_root)

        action = inputs.get("action", "publish_blog")
        
        if action == "publish_blog":
            return await self.publish_blog(inputs.get("content_draft", {}))
        elif action == "deploy_site":
            return await self.deploy_site()
        
        return NodeOutput(data=None, metadata={"error": "Unknown action"})

    async def publish_blog(self, draft: Dict[str, Any]) -> NodeOutput:
        title = draft.get("title", "Untitled Post")
        content = draft.get("draft", "No content provided.")
        slug = title.lower().replace(' ', '-')
        
        self.log(f"Publishing blog: {title}")
        
        # 1. Generate Schema Markup (JSON-LD)
        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "datePublished": datetime.datetime.now().isoformat(),
            "author": {"@type": "Organization", "name": "Manokamana Solar"}
        }

        # 2. Write Markdown File
        file_content = f"""---
title: {title}
date: {datetime.datetime.now().strftime('%Y-%m-%d')}
schema: {json.dumps(schema)}
---

{content}
"""
        filepath = self.builder.get_blog_path(slug)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(file_content)

        # 3. Log to Global Memory
        asset_url = f"/blog/{slug}"
        published_asset = {
            "title": title,
            "url": asset_url,
            "file_path": filepath,
            "published_at": datetime.datetime.now().isoformat()
        }
        self.global_memory.append_to_list("published_assets", published_asset)
        
        return NodeOutput(
            data=published_asset,
            metadata={"status": "published", "slug": slug}
        )

    async def deploy_site(self) -> NodeOutput:
        self.log("Triggering site rebuild and deployment...")
        webhook_url = self.config.get("DEPLOYMENT_WEBHOOK_URL", "http://localhost:8000/deploy")
        self.log(f"Notifying deployment webhook: {webhook_url}")
        result = self.builder.rebuild_site()
        return NodeOutput(data=result, metadata={"deployment": "success", "webhook": webhook_url})
