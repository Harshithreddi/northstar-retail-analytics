# Northstar Retail Analytics — BI + Data Assistant

**Version:** 1.0  
**Status:** Working portfolio project

## Project Overview

Northstar Retail Analytics is a portfolio project that combines Power BI, Python analytics, and a Streamlit web application to explore retail sales performance.

The application uses a fictional retail dataset to analyze revenue, profitability, regional performance, monthly trends, and potentially unusual transactions.

The goal is to demonstrate how data preparation, reusable analytical functions, visualization, and a business question-answering interface can work together in one project.

## Business Objectives

- Monitor key retail performance indicators.
- Compare revenue across regions.
- Understand product profitability.
- Analyze monthly sales trends.
- Identify transactions that may need further investigation.
- Make analytical results easier to explore through a web interface.

## Features

### 1. Retail Dataset

- 2,000 fictional sales orders.
- Order dates, regions, cities, products, and customer segments.
- Quantity, unit price, discount, revenue, cost, and profit.
- Sales channels and payment methods.

### 2. Power BI Dashboard

- Total revenue, total profit, order count, and profit margin.
- Monthly revenue trend.
- Revenue by region.

### 3. Python Analytics Engine

Reusable functions for:

- KPI calculation.
- Revenue and profit analysis by region.
- Product profitability analysis.
- Monthly revenue and profit summaries.
- Product-specific revenue anomaly detection.

### 4. Streamlit Application

- Interactive region, category, and date filters.
- KPI cards and interactive charts.
- Dashboard, Business Assistant, and Data Explorer sections.
- CSV export for the dataset and assistant results.

### 5. Business Assistant

The current version uses Python-based question matching and analytical functions to answer supported questions, including:

- Which region generated the highest revenue?
- Which product is most profitable?
- Show monthly revenue.
- Find unusual orders.
- What is the total revenue?

The current assistant is not presented as a fully integrated large language model. A floating chatbot interface and further AI capabilities are planned enhancements.

## Technology Stack

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Power BI
- Git and GitHub

## Project Structure

```text
northstar-retail-analytics/
├── app.py
├── generate_dataset.py
├── test_analytics.py
├── src/
│   └── analytics.py
├── data/
│   └── sales_data.csv
├── requirements.txt
├── README.md
└── .gitignore
```

A Power BI report can be shared separately after checking that it contains no embedded credentials, sensitive information, or private connection details.

## Getting Started

### Prerequisites

- Python installed on your computer.
- Git installed.
- The project files cloned from GitHub.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/northstar-retail-analytics.git
cd northstar-retail-analytics
```

Replace `YOUR-USERNAME` with the repository owner's GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Install dependencies

On Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Generate the dataset if it is not included

```powershell
.\.venv\Scripts\python.exe generate_dataset.py
```

### 5. Run the analytics tests

```powershell
.\.venv\Scripts\python.exe test_analytics.py
```

### 6. Launch the application

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL shown in the terminal.

## Statistical Anomaly Detection

The application uses the Interquartile Range (IQR) method to flag unusually low or high revenue within product groups.

These results identify transactions for review. A statistical flag does not prove that a transaction is incorrect.

## Version 1

Version 1 establishes the synthetic dataset, Python analytics functions, Power BI report, Streamlit application, and Business Assistant.

## Roadmap

- Version 2: Floating bottom-right chatbot interface.
- Improved question handling and business insights.
- Additional profitability analysis.
- Sales forecasting exploration.
- Application deployment and usability improvements.

## Data and Security

- The dataset is synthetic and intended for demonstration.
- No real customer data is intended to be included.
- API keys, passwords, access tokens, and private configuration files must not be committed.
- Local secrets are excluded using `.gitignore`.
- Review all files before publishing this repository.

## Disclaimer

This is an ongoing portfolio and learning project. Results are intended for demonstration and should be validated before use in real business decisions.
