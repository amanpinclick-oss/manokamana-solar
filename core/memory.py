from typing import Any, Dict, List
import datetime

class GlobalMemory:
    """
    Manages global state and logs for the entire agentic system.
    """

    def __init__(self):
        self.memory: Dict[str, Any] = {
            "keyword_performance": [],
            "lead_quality": [],
            "conversion_feedback": [],
            "content_performance": [],
            "risk_scores": [],
            "budget_phase": "STATE_1",
            "published_assets": []
        }
        self.event_log: List[Dict[str, Any]] = []

    def update_state(self, key: str, value: Any):
        if key in self.memory:
            self.memory[key] = value
        else:
            self.memory[key] = value

    def append_to_list(self, key: str, value: Any):
        if key in self.memory and isinstance(self.memory[key], list):
            self.memory[key].append(value)

    def log_event(self, node_id: str, event_type: str, details: Dict[str, Any]):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "node_id": node_id,
            "event_type": event_type,
            "details": details
        }
        self.event_log.append(entry)

    def get_state(self, key: str) -> Any:
        return self.memory.get(key)

    def get_list(self, key: str) -> List[Any]:
        """
        Safely retrieve a list from memory.
        """
        val = self.get_state(key)
        return val if isinstance(val, list) else []
