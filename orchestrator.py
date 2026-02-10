# orchestrator.py
import json
import datetime
import random
from db import conn

def fetch_market_signal():
    # Placeholder for trend-based logic. In a real scenario, this would read from the DB
    # or call the trend_agent. For now, we simulate a signal.
    print("Fetching market signals...")
    # Simulated signals
    return {
        "industrial solar": random.randint(50, 95),
        "commercial solar": random.randint(50, 95),
        "solar EPC": random.randint(50, 80),
        "rooftop pv": random.randint(50, 90)
    }

def decide_tasks():
    market = fetch_market_signal()
    tasks = []

    # 1. SEO Logic: If interest is high, plan a blog post
    for kw, score in market.items():
        if score > 80:
            tasks.append({
                "agent": "seo",
                "payload": json.dumps({"action": "new_blog", "keyword": kw})
            })

    # 2. Content Logic: If commercial interest is significantly higher, plan social media
    if market.get("commercial solar", 0) > 85:
        tasks.append({
            "agent": "content",
            "payload": json.dumps({"action": "linkedin_carousel", "topic": "Commercial Solar ROI"})
        })

    # 3. Lead Intel Logic: Constant monitoring task
    tasks.append({
        "agent": "lead_intel",
        "payload": json.dumps({"action": "daily_review"})
    })

    return tasks

def enqueue(tasks):
    with conn() as c:
        for t in tasks:
            c.execute(
                "INSERT INTO tasks (agent, payload) VALUES (?, ?)",
                (t["agent"], t["payload"])
            )
    print(f"Queued {len(tasks)} tasks.")

if __name__ == "__main__":
    print(f"[{datetime.datetime.now()}] Starting Orchestrator Daily Loop...")
    new_tasks = decide_tasks()
    enqueue(new_tasks)
    print("Orchestrator run complete.")
