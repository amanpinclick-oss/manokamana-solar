from typing import Dict

class ContentTemplates:
    """
    Brand guidelines and platform-specific structure templates for Manokamana Solar.
    """

    VOICE_GUIDELINES = "Professional, ROI-focused, educational, and sustainable."

    TEMPLATES = {
        "linkedin": {
            "prefix": "🌟 Industrial Solar: A High-ROI Financial Asset.\n\n",
            "suffix": "\n\n#SolarIndia #IndustrialSolar #ROI #ManokamanaSolar",
            "max_length": 3000
        },
        "instagram": {
            "prefix": "⚡️ Go Solar, Go Green, Save Big! ⚡️\n\n",
            "suffix": "\n\n. \n. \n#SolarEnergy #GoSolar #CleanEnergy #Sustainability",
            "max_length": 2200
        },
        "facebook": {
            "prefix": "📢 Focus on Savings! Manokamana Solar presents: ",
            "suffix": "\n\nContact us for a free solar assessment! 📞",
            "max_length": 5000
        },
        "youtube_script": {
            "structure": [
                "[Hook: 0-10s] Why your factory is losing money every month on electricity.",
                "[Introduction: 10-30s] Introduction to Solar ROI and Manokamana Solar.",
                "[Core Content: 30-120s] {topic_details}",
                "[Call to Action: 120-150s] Click the link below for a free ROI report."
            ]
        },
        "blog": {
            "prefix": "<h1>{title}</h1>\n",
            "suffix": "\n\n<p>Stay tuned for more solar insights from Manokamana Solar.</p>",
            "max_length": 50000
        }
    }

    @staticmethod
    def format_content(platform: str, topic: str, raw_draft: str) -> str:
        """
        Formats raw draft into platform-specific content using templates.
        """
        template = ContentTemplates.TEMPLATES.get(platform, {})
        if platform == "youtube_script":
            script = "\n".join(template["structure"]).replace("{topic_details}", raw_draft)
            return script
        
        prefix = template.get("prefix", "").replace("{title}", topic)
        suffix = template.get("suffix", "")
        
        formatted = f"{prefix}{raw_draft}{suffix}"
        
        # Truncate if necessary
        max_len = template.get("max_length", 10000)
        return formatted[:max_len]
