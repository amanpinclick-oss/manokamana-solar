# lead_intel_agent.py
import json
import re
import datetime
from db import conn

HIGH_INTENT_PATTERNS = [
    r"\bkw\b", r"\bmw\b", r"\broi\b", r"\bsubsidy\b", r"\bindustrial\b", r"\bcommercial\b"
]

def score_lead(message):
    score = 0
    msg = message.lower()
    for pat in HIGH_INTENT_PATTERNS:
        if re.search(pat, msg):
            score += 1
    return min(score / 3.0, 1.0) # Normalized score

def ingest_lead(name, email, phone, interest, message):
    intent = score_lead(message)
    lead_type = "Industrial" if "industrial" in interest.lower() or "industrial" in message.lower() else "Commercial"
    
    with conn() as c:
        c.execute("""INSERT INTO leads (name, email, phone, type, intent_score, source)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (name, email, phone, lead_type, intent, "website"))
    print(f"Lead ingested: {name} (Score: {intent:.2f})")
    
    # Mock Notification
    if intent > 0.6:
        print(f"ALERT: High-intent lead detected! Sending WhatsApp to BPO...")

def daily_review():
    print("Running daily lead review...")
    # Clear out extremely low-intent old leads if necessary
    with conn() as c:
        c.execute("UPDATE leads SET status='archived' WHERE intent_score < 0.1 AND status='new'")
    print("Daily lead review complete.")

def process_task(task_id, payload):
    action = payload.get("action")
    if action == "daily_review":
        daily_review()
        with conn() as c:
            c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))

def main():
    with conn() as c:
        rows = c.execute("SELECT id, payload FROM tasks WHERE agent='lead_intel' AND status='pending'").fetchall()
        for r in rows:
            process_task(r[0], json.loads(r[1]))

if __name__ == "__main__":
    # For testing: Ingest a sample lead
    # ingest_lead("Test User", "test@example.com", "9876543210", "Industrial Solar", "Need 100kW rooftop installation ROI.")
    main()
