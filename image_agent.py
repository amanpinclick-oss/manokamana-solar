# image_agent.py
import json
import os
import subprocess
from db import conn

def gen_from_prompt_mock(prompt, out_path):
    print(f"Generating image for prompt: {prompt[:50]}...")
    # Mocking image creation: creating a placeholder text file if GPU is missing
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path + ".txt", "w") as f:
        f.write(f"IMAGE_PLACEHOLDER: {prompt}")
    print(f"Mock image placeholder created at {out_path}.txt")

def process_task(task_id, payload):
    if payload["action"] == "carousel_images":
        topic = payload.get("topic", "solar")
        # In a real scenario, captions would be used for multi-slide prompts
        out_path = f"static/images/{topic.replace(' ', '_')}.png"
        gen_from_prompt_mock(f"Industrial solar panels on a factory roof in India, high quality, professional photography.", out_path)
        
        with conn() as c:
            # Notify content agent or just mark as done
            c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
            print(f"Image generation task {task_id} marked as done.")

def main():
    with conn() as c:
        rows = c.execute("SELECT id, payload FROM tasks WHERE agent='image_generator' AND status='pending'").fetchall()
        for r in rows:
            process_task(r[0], json.loads(r[1]))

if __name__ == "__main__":
    main()
