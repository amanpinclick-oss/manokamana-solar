import json
import csv
import os
from typing import Dict, List, Any

class ReportGenerator:
    """
    Utility for generating structured JSON and CSV performance reports.
    """

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_json(self, data: Dict[str, Any], filename: str) -> str:
        """
        Exports data as a JSON file.
        """
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return filepath

    def generate_csv(self, list_data: List[Dict[str, Any]], filename: str) -> str:
        """
        Exports a list of dictionaries as a CSV file.
        """
        if not list_data:
            return ""
        
        filepath = os.path.join(self.output_dir, f"{filename}.csv")
        keys = list_data[0].keys()
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(list_data)
        
        return filepath
