# compliance_agent.py
import json
import re
import datetime
from db import conn

# Platform policy safety checks
PROHIBITED_PHRASES = [
    r"\bguarantee(s)?\b",
    r"\bfree\s+installation\b",
    r"\bsubsid(y|ies)?\b.*\b(100%|full)\b",
    r"\broi\s+of\s+100%?\b",
    r"\bget\s+rich\b"
]

def passes_policy(text):
    low = text.lower()
    for pat in PROHIBITED_PHRASES:
        if re.search(pat, low):
            print(f"POLICY VIOLATION: Found prohibited pattern '{pat}'")
            return False
    return True

def review_task(task_id, agent, payload_str):
    payload = json.loads(payload_str)
    print(f"Reviewing task {task_id} for agent {agent}...")
    
    # Logic to check content based on task type
    # For this prototype, we check the metadata in the payload
    if "keyword" in payload:
        if not passes_policy(payload["keyword"]):
             return False
    if "topic" in payload:
        if not passes_policy(payload["topic"]):
            return False
            
    return True

def main():
    with conn() as c:
        # Compliance agent reviews 'pending' tasks and moves them to 'approved'
        # Other agents should ideally only consume 'approved' tasks.
        # For simplicity in this demo, agents consume 'pending', 
        # but a robust system would have this gatekeeper.
        rows = c.execute("SELECT id, agent, payload FROM tasks WHERE status='pending'").fetchall()
        for r in rows:
            if review_task(r[0], r[1], r[2]):
                # In a strict system, we'd change status to 'approved'
                # For this blueprint flow, we'll just log the approval.
                print(f"Task {r[0]} approved.")
            else:
                c.execute("UPDATE tasks SET status='blocked' WHERE id=?", (r[0],))
                print(f"Task {r[0]} BLOCKED due to compliance failure.")

if __name__ == "__main__":
    main()
