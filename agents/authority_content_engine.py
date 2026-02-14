from core.base_node import BaseNode, NodeOutput
from core.content_templates import ContentTemplates
from typing import Any, Dict
from openai import OpenAI

class AuthorityContentEngine(BaseNode):
    """
    NODE_3: AUTHORITY_CONTENT_ENGINE
    Generates multi-platform content drafts using real OpenAI API calls.
    Integrated with ContentTemplates for platform-specific formatting.
    """

    def __init__(self):
        super().__init__("NODE_3", "Generator")
        self.client = None

    async def run(self, inputs: Dict[str, Any]) -> NodeOutput:
        topic = inputs.get("topic", "Solar ROI for Industrial Clients")
        platform = inputs.get("platform", "linkedin")
        
        self.log(f"Generating live {platform} content for topic: {topic}")
        
        if not self.client:
            api_key = self.config.get("OPENAI_API_KEY")
            if not api_key or "sk-" not in api_key:
                self.log("Warning: Invalid or missing OpenAI API Key. Falling back to mock logic.")
                return await self._run_mock(topic, platform)
            self.client = OpenAI(api_key=api_key)

        try:
            # 1. Real OpenAI API Call
            response = self.client.chat.completions.create(
                model="gpt-4o", # Scalable model for authority content
                messages=[
                    {"role": "system", "content": f"You are an expert solar consultant for the Indian industrial sector. {ContentTemplates.VOICE_GUIDELINES}"},
                    {"role": "user", "content": f"Write a professional {platform} post about: {topic}. Include ROI metrics and industrial benefits."}
                ],
                max_tokens=500
            )
            raw_draft = response.choices[0].message.content
        except Exception as e:
            self.log(f"OpenAI Error: {e}. Falling back to mock logic.")
            return await self._run_mock(topic, platform)

        # 2. Use ContentTemplates to format (adds branding/hashtags if needed)
        formatted_content = ContentTemplates.format_content(platform, topic, raw_draft)
        
        result = {
            "draft": formatted_content,
            "platform": platform,
            "topic": topic,
            "brand_voice": ContentTemplates.VOICE_GUIDELINES
        }
        
        self.log(f"Live content generation complete for {platform}.")
        
        return NodeOutput(
            data=result,
            metadata={"status": "draft_generated", "mode": "live", "platform": platform}
        )

    async def _run_mock(self, topic: str, platform: str) -> NodeOutput:
        # Fallback simulation
        raw_draft = f"Self-generated draft about {topic} for {platform}. (Mock Mode)"
        formatted_content = ContentTemplates.format_content(platform, topic, raw_draft)
        return NodeOutput(
            data={"draft": formatted_content, "platform": platform, "topic": topic},
            metadata={"status": "draft_generated", "mode": "mock"}
        )
