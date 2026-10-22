# Northstar Retail Analytics — BI + Data Assistant

**An interactive retail analytics portfolio project combining Power BI, Python, and Streamlit.**

[🚀 Launch Live Demo](https://northstar-retail-analytics-mxqqcmroaemfjwb4mixffb.streamlit.app/) · [📂 GitHub Repository](https://github.com/Harshithreddi/northstar-retail-analytics) · [📊 Power BI Report](Northstar_Retail_Analytics.pbix)

## Project Overview

Northstar Retail Analytics demonstrates how business intelligence, reusable Python analytics, statistical anomaly detection, and a web-based Business Assistant can work together to explore retail sales performance.

The project uses a synthetic dataset of 2,000 fictional sales orders to analyze revenue, profitability, regional performance, monthly trends, and potentially unusual transactions.

## Project Features

### 1. Power BI Dashboard
- Key performance indicators: total revenue, profit, order count, and profit margin.
- Monthly revenue trends.
- Regional revenue analysis.
- Interactive business reporting using fictional retail data.

### 2. Python Analytics Engine
- Reusable KPI calculation functions.
- Revenue analysis by region.
- Product profitability analysis.
- Monthly revenue summaries.
- Product-specific revenue anomaly detection using the Interquartile Range (IQR) method.

### 3. Streamlit Analytics Application
- Interactive region, category, and date filters.
- KPI cards and interactive charts.
- Dashboard, Business Assistant, and Data Explorer sections.
- CSV exports for data exploration and supported assistant results.

### 4. Business Assistant
The current version uses Python-based question matching and analytics functions to answer supported business questions.

Example questions:
- Which region generated the highest revenue?
- Which product is most profitable?
- Show monthly revenue.
- Find unusual orders.
- What is the total revenue?

**Current limitation:** The assistant is rule-based and is not yet integrated with a large language model. A conversational chatbot interface and further AI capabilities are planned for Version 2.

## Live Demo

**[Open Northstar Retail Analytics](https://northstar-retail-analytics-mxqqcmroaemfjwb4mixffb.streamlit.app/)**

Explore the interactive application and try its supported business questions.

## Power BI Report

The Power BI report is included in this repository:

[`Northstar_Retail_Analytics.pbix`](Northstar_Retail_Analytics.pbix)

Download the report and open it in Power BI Desktop to explore the dashboard. The report uses synthetic demonstration data.

## Screenshots

Screenshots of the actual running application will be added here.

Recommended screenshots:
- Power BI dashboard
- Streamlit dashboard and KPI cards
- Business Assistant with a sample question and answer
- Data Explorer with filters and data table

Save the screenshots in a folder named `screenshots` in the repository, then embed them here using Markdown image links.

Example, after adding the corresponding image files:

```markdown
![Power BI Dashboard](screenshots/powerbi-dashboard.png)

![Business Assistant](screenshots/business-assistant.png)

![Data Explorer](screenshots/data-explorer.png)
```

## Technology Stack

- **Languages:** Python, SQL
- **Data analysis:** Pandas, NumPy
- **Visualization:** Power BI, Plotly
- **Web application:** Streamlit
- **Analytics:** KPI calculations, profitability analysis, IQR-based anomaly detection
- **Version control:** Git and GitHub

## Repository Structure

```text
northstar-retail-analytics/
├── app.py
├── generate_dataset.py
├── test_analytics.py
├── requirements.txt
├── README.md
├── Northstar_Retail_Analytics.pbix
├── data/
│   └── sales_data.csv
└── src/
    └── analytics.py
```

## Getting Started

### Prerequisites
- Python installed
- Git installed

### 1. Clone the repository

```bash
git clone https://github.com/Harshithreddi/northstar-retail-analytics.git
cd northstar-retail-analytics
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Generate the dataset if needed

```powershell
python generate_dataset.py
```

### 5. Run the analytics tests

```powershell
python test_analytics.py
```

### 6. Launch the application

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in your terminal.

## Statistical Anomaly Detection

The application uses the Interquartile Range (IQR) method to identify unusually low or high revenue values within product groups.

These flags identify transactions that may warrant further review. A statistical anomaly does not prove that a transaction is incorrect or fraudulent.

## Data and Security

- The retail dataset is fictional and intended for demonstration.
- No real customer data is intended to be included.
- API keys, passwords, access tokens, and private configuration files must never be committed to GitHub.
- Local secrets are excluded using `.gitignore`.
- Review Power BI connection details and all repository files before sharing publicly.

## Roadmap

### Version 1 — Current
- Synthetic retail dataset.
- Python analytics functions.
- Power BI dashboard.
- Streamlit analytics application.
- Rule-based Business Assistant.
- Statistical anomaly detection.

### Version 2 — Planned
- Floating bottom-right chatbot interface.
- Improved natural-language question handling.
- Expanded business insights and profitability analysis.
- Exploration of sales forecasting.
- Further deployment and usability improvements.

## Disclaimer

This is an ongoing portfolio and learning project. All analytical outputs are intended for demonstration and should be validated before being used to make real business decisions.
