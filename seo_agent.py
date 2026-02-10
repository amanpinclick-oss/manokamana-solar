# seo_agent.py
import json
import datetime
from db import conn

# Placeholder for Google API client
# In a real environment, you'd use:
# from googleapiclient.discovery import build
# from google.oauth2 import service_account

def fetch_queries_mock():
    print("Fetching Google Search Console queries (Mocked)...")
    # Simulated GSC data
    return [
        {'keys': ['industrial solar ROI'], 'clicks': 120, 'impressions': 1000, 'ctr': 0.12, 'position': 4.5},
        {'keys': ['commercial solar EPC india'], 'clicks': 45, 'impressions': 800, 'ctr': 0.05, 'position': 8.2},
        {'keys': ['solar subsidy for factories'], 'clicks': 80, 'impressions': 600, 'ctr': 0.13, 'position': 3.1}
    ]

def update_seo_metrics(rows):
    now = datetime.datetime.now()
    with conn() as c:
        for r in rows:
            q = r['keys'][0]
            c.execute("""INSERT OR REPLACE INTO seo_metrics
                         (query, clicks, impressions, ctr, position, last_updated)
                         VALUES (?, ?, ?, ?, ?, ?)""",
                      (q, r['clicks'], r['impressions'], r['ctr'], r['position'], now))
    print(f"Updated SEO metrics for {len(rows)} queries.")

def low_competition_keywords(rows, ctr_thr=0.02, pos_thr=15):
    # Intent identification: high CTR and top 15 position
    return [r['keys'][0] for r in rows if r['ctr'] > ctr_thr and r['position'] < pos_thr]

def queue_blog(keyword):
    with conn() as c:
        c.execute("""INSERT INTO tasks (agent, payload) VALUES
                     ('content', ?)""",
                  (json.dumps({"action": "new_blog", "keyword": keyword}),))
    print(f"Queued blog creation task for: {keyword}")

def run():
    rows = fetch_queries_mock()
    update_seo_metrics(rows)
    candidates = low_competition_keywords(rows)
    # Queue top 2 high-intent topics
    for kw in candidates[:2]:
        queue_blog(kw)

if __name__ == "__main__":
    run()
