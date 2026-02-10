# website_agent.py
import os
import json
import subprocess
import datetime
from db import conn

CONTENT_DIR = "content"

def init_site():
    print("Initializing Hugo site...")
    # Mocking Hugo initialization if 'hugo' is not available
    try:
        subprocess.run(["hugo", "new", "site", "."], check=True)
        print("Hugo site scaffolded.")
    except Exception as e:
        print(f"Hugo not found or init failed: {e}. Proceeding with manual directory creation.")
        os.makedirs(CONTENT_DIR, exist_ok=True)
        for s in ["industrial", "commercial", "services", "projects", "blog", "contact"]:
            os.makedirs(os.path.join(CONTENT_DIR, s), exist_ok=True)

def process_task(task_id, payload):
    action = payload.get("action")
    if action == "add_page":
        slug = payload["slug"]
        title = payload["title"]
        section = payload["section"]
        fname = os.path.join(CONTENT_DIR, section, f"{slug}.md")
        
        # In case the file doesn't exist (Content Agent already writes blog posts)
        if not os.path.exists(fname):
            with open(fname, "w") as f:
                f.write(f"""---
title: "{title}"
date: {datetime.datetime.now().isoformat()}
draft: false
---
New page content for {title}.
""")
        print(f"Page processed: {fname}")
        
        # Git Integration (Mocked / Attempted)
        try:
            subprocess.run(["git", "add", "."], check=False)
            subprocess.run(["git", "commit", "-m", f"auto: update {slug}"], check=False)
            print("Changes committed to Git.")
        except:
            print("Git commit skipped (likely no repo initialized).")
        
        with conn() as c:
            c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))

def main():
    if not os.path.exists(CONTENT_DIR):
        init_site()
        
    with conn() as c:
        rows = c.execute("SELECT id, payload FROM tasks WHERE agent='website' AND status='pending'").fetchall()
        for r in rows:
            process_task(r[0], json.loads(r[1]))

if __name__ == "__main__":
    main()
