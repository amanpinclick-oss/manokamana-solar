# Manokamana Solar - Digital Growth Engine

This is a self‑maintaining growth system for Solar EPC.

## Local Setup (Windows - No Docker)

1. **Install Python**: Make sure you have Python installed from python.org.
2. **Setup AI**: Download and run the **Ollama** app from [ollama.com](https://ollama.com).
3. **Run**: Double-click the `run_local.bat` file in this folder.
4. **Dashboard**: Open `http://localhost:8080` in your browser.

## Architecture
- **Orchestrator**: Daily loop for task assignment.
- **Agents**: Stateless scripts for SEO, Content, Leads, and Compliance.
- **Data**: SQLite store for tasks, metrics, and leads.
