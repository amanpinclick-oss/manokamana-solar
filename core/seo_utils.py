from typing import List, Dict

class SEOUtils:
    """
    Utility for SEO analysis, keyword clustering, and intent classification.
    """

    @staticmethod
    def cluster_keywords(keywords: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Groups keywords into clusters based on intent (High vs Information).
        """
        clusters = {
            "high_intent": [],
            "informational": [],
            "long_tail": []
        }

        for kw in keywords:
            intent = kw.get("intent", "medium")
            if intent == "high":
                clusters["high_intent"].append(kw)
            elif intent == "low":
                clusters["informational"].append(kw)
            
            if len(kw.get("keyword", "").split()) >= 4:
                clusters["long_tail"].append(kw)

        return clusters

    @staticmethod
    def calculate_topic_weight(keyword: str, global_weights: Dict[str, float]) -> float:
        """
        Calculates a priority weight for a keyword based on system topic affinities.
        """
        for topic, weight in global_weights.items():
            if topic.lower() in keyword.lower():
                return weight
        return 0.1 # Baseline
