# trend_agent.py
import json
import datetime
from db import conn
# Note: pytrends is often used for this, but for this blueprint we'll use a mocked version 
# to ensure it runs without external environment dependencies in this sandbox.

def pull_trends():
    print("Pulling Google Trends data...")
    # Simulated data for core EPC topics
    kw = ["industrial solar", "commercial solar", "solar EPC", "rooftop pv", "green energy subsidy"]
    trends = {k: 75 + (datetime.datetime.now().hour % 20) for k in kw}
    return trends

def push_to_orchestrator(trends):
    payload = json.dumps({"action": "trend_update", "data": trends})
    with conn() as c:
        c.execute("INSERT INTO tasks (agent, payload) VALUES (?, ?)",
                  ('market_trend', payload))
    print("Trend data queued in task table.")

def run():
    trends = pull_trends()
    push_to_orchestrator(trends)

if __name__ == "__main__":
    run()
