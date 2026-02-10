# app.py
from flask import Flask, jsonify, send_from_directory, make_response
from db import conn
import os
import csv
import io

app = Flask(__name__, static_folder="static")

@app.route("/api/seo")
def seo():
    with conn() as c:
        rows = c.execute("SELECT query, clicks, impressions, ctr, position FROM seo_metrics ORDER BY last_updated DESC LIMIT 100").fetchall()
    return jsonify([dict(zip(["query", "clicks", "impressions", "ctr", "position"], r)) for r in rows])

@app.route("/api/leads")
def leads():
    with conn() as c:
        rows = c.execute("""SELECT id, name, email, phone, type, intent_score, status, created_at 
                            FROM leads ORDER BY created_at DESC LIMIT 200""").fetchall()
    return jsonify([dict(zip(["id", "name", "email", "phone", "type", "score", "status", "created"], r)) for r in rows])

@app.route("/api/alerts")
def alerts():
    with conn() as c:
        rows = c.execute("""SELECT id, agent, payload, created_at FROM tasks 
                            WHERE status='blocked' ORDER BY created_at DESC LIMIT 20""").fetchall()
    return jsonify([dict(zip(["id", "agent", "payload", "created"], r)) for r in rows])

@app.route("/api/leads/csv")
def leads_csv():
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(["ID", "Name", "Email", "Phone", "Type", "Score", "Status", "Created"])
    with conn() as c:
        rows = c.execute("SELECT id, name, email, phone, type, intent_score, status, created_at FROM leads").fetchall()
        for row in rows:
            writer.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=leads.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
