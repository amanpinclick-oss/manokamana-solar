# Manokamana Solar Agentic Engine: Deployment Guide ☀️🚀

This guide outlines the steps required to move the Manokamana Solar Agentic Engine from simulation to a live production environment.

## 1. Prerequisites
- **Python**: Version 3.10 or higher.
- **Project Structure**: Ensure you have the following directories in your project root:
  - `agents/` (Core agent nodes)
  - `core/` (Orchestration and utilities)
  - `content/` (Generated blog assets)
  - `reports/` (System performance data)
  - `public/` (Static site build output)

## 2. Environment Setup

### Install Dependencies
Run the following command in your terminal to install the required libraries:
```powershell
pip install python-dotenv
```
*(Note: As the project grows, ensure all node-specific libraries like `openai`, `google-api-python-client`, etc., are installed if you replace the mock logic.)*

### Configure Secrets
1. Copy the template configuration:
   ```powershell
   copy .env.example .env
   ```
2. Open `.env` and populate the following keys with your real credentials:
   - `OPENAI_API_KEY`: For content generation (NODE_3).
   - `GSC_SERVICE_ACCOUNT_JSON`: Path to your Google Search Console key (NODE_2).
   - `DEPLOYMENT_WEBHOOK_URL`: Your static site rebuild trigger (NODE_1).
   - `SALES_WEBHOOK_URL`: Your Slack or CRM hook (NODE_4).
   - `GA4_PROPERTY_ID`: For analytics reporting (NODE_6).

## 3. Launching the Engine

### Run Simulation / Initial Seed
To verify your setup and generate the first batch of assets and reports, run:
```powershell
python main.py
```

### Sustained Operations
For production, you should run the orchestrator as a background process or via a cron job. The system is designed to trigger specific nodes based on events or schedules (e.g., NODE_7 monthly, NODE_2 weekly).

## 4. Directory Overview
- **`content/blogs/`**: This is where the agent writes its Markdown digital assets. Point your Static Site Generator (Vite, Next.js, Hugo) here.
- **`reports/`**: Check `system_summary.json` for dashboard data and `leads_detailed.csv` for your sales team.
- **`logs/`**: Detailed execution logs for debugging agent decisions.

## 5. Scaling & Optimization
- **Phase Control**: The system automatically scales from Phase 1 to Phase 4 based on lead volume. Monitor the `budget_phase` in the reports.
- **Topic Weights**: The system will self-correct its SEO focus monthly based on which topics yield the highest-scoring leads.

---
**Status**: Integrated & Verified. Ready for Production Launch.
