# content_agent.py
import json
import os
import datetime
from db import conn

# Mocking LLM generation for the environment
def llm_mock(prompt):
    print(f"Generating content for prompt: {prompt[:50]}...")
    if "outline" in prompt.lower():
        return "## Introduction\n## Benefits of Solar\n## ROI Analysis\n## Conclusion"
    else:
        return "This is a comprehensive guide to solar energy for industrial sectors. It covers energy savings, sustainability, and the long-term ROI of solar EPC projects in India."

def build_blog(keyword):
    outline = llm_mock(f"Write an outline for {keyword}")
    body = llm_mock(f"Write a full SEO-optimized blog post for {keyword} using this outline: {outline}")
    meta_desc = "Expert guide on industrial solar ROI and benefits for Indian businesses."
    
    slug = keyword.lower().replace(' ', '-')
    fm = f"""---
title: "{keyword.title()}"
date: {datetime.datetime.now().isoformat()}
slug: "{slug}"
description: "{meta_desc}"
draft: false
tags: ["solar", "india", "industrial"]
---
"""
    
    os.makedirs("content/blog", exist_ok=True)
    path = os.path.join("content", "blog", f"{slug}.md")
    with open(path, "w") as f:
        f.write(fm + "\n" + body)
    
    print(f"Blog content written to {path}")
    return slug, keyword.title()

def process_task(task_id, payload):
    act = payload.get("action")
    if act == "new_blog":
        slug, title = build_blog(payload["keyword"])
        with conn() as c:
            # Notify Website Agent to update the site
            c.execute("""INSERT INTO tasks (agent, payload) VALUES (?, ?)""",
                      ('website', json.dumps({"action": "add_page", "section": "blog", "slug": slug, "title": title})))
            # Mark this task as done
            c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
    elif act == "linkedin_carousel":
        print(f"Queueing social media visual generation for: {payload.get('topic')}")
        with conn() as c:
            c.execute("""INSERT INTO tasks (agent, payload) VALUES (?, ?)""",
                      ('image_generator', json.dumps({"action": "carousel_images", "topic": payload.get("topic")})))
            c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))

def main():
    with conn() as c:
        rows = c.execute("SELECT id, payload FROM tasks WHERE agent='content' AND status='pending'").fetchall()
        for r in rows:
            process_task(r[0], json.loads(r[1]))

if __name__ == "__main__":
    main()
