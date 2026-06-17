# Cyber Hackathon Project 🚀

## 👥 Team
- Ximena Prado Zegarra
- Namrata Dixit

## 💡 Project Overview
This project delivers an AI-driven solution to automate phishing campaign reporting at Maersk. It replaces manual data processing from tools like Trend Vision One and Abnormal AI with an automated workflow that consolidates, calculates, and analyzes results. The solution also generates insights by identifying trends, enabling more targeted awareness and reducing human cyber risk.

## 🔐 Problem
Phishing campaign data is currently generated across multiple platforms, such as Trend Vision One and Abnormal AI, requiring manual extraction and calculation.
This process is time-consuming, prone to errors, and limits the ability to quickly identify trends, high-risk users, and recurring behaviours—reducing the effectiveness of cyber awareness efforts.

## ⚙️ Solution
This project introduces an AI-powered solution that automates the consolidation, calculation, and analysis of phishing campaign data.
It eliminates manual reporting while providing actionable insights, including trend analysis and detection of risky behaviours. This enables faster, data-driven decision-making and more targeted cyber awareness initiatives.

## 🛠️ Technologies
- **Dify** – used to design and orchestrate the end-to-end AI workflow  
- **Python (Code Nodes)** – implemented custom logic for data processing, calculations, and metrics (e.g., click/report rates)  
- **CSV / Excel** – input data source for phishing campaign results  
- **AI Automation** – to generate insights and streamline reporting  
- **GitHub** – for version control and collaboration 


## 📊 Impact
- Reduces manual reporting time by automating data consolidation and calculations  
- Improves accuracy by eliminating human error in report generation
- Enables targeted awareness by identifying high-risk audiences
- Accelerates decision-making with real-time, actionable insights
- Increases efficiency and scalability of reporting across multiple campaigns

## ⚙️ Data Processing

The preprocessing logic (originally implemented in Dify) is available in:
`/src/data_preprocessing.py`

It handles:
- Data cleaning
- Duplicate removal
- User activity prioritization

## 📊 Metrics Calculation

The metrics logic is available in:
`/src/metrics_calculation.py`

It calculates:
- Total users
- Clicked users
- Click rate

## 📊 Reporting Metrics

The reporting logic is available in:
`/src/reporting_metrics.py`

It calculates:
- Unique reported users
- Reporting rate
- User engagement with phishing reporting mechanisms

## 🧠 Risk Classification

The risk engine is implemented in:
`/src/risk_classification.py`

It classifies phishing outcomes into:
- Low Risk
- Medium Risk
- High Risk

Based on user behavior (click vs report rates), enabling targeted awareness actions.

## 📤 Final Output

The pipeline outputs structured metrics ready for dashboards and reporting:

- **Click Rate** – Percentage of users who clicked the phishing link  
- **Reporting Rate** – Percentage of users who reported the email  
- **Scenario** – Behavioral classification based on user actions  
- **Risk Label** – Assigned risk level (e.g., Low, Medium, High)  

These outputs are designed to feed directly into human risk dashboards and support data-driven decision-making.

## 🧩 End-to-End Pipeline

## 🧩 End-to-End Pipeline

```mermaid
flowchart TD
A[Input Data] --> B[Preprocessing]
B --> C[Click Metrics]
B --> D[Reporting Metrics]
C --> E[Risk Classification]
D --> E
E --> F[AI Summary]
F --> G[Final Output]
``

## 🎯 Output Design

The final node structures all outputs into standardized variables, enabling seamless integration with dashboards and reporting tools.

This ensures insights are not only generated, but also easily consumable for leadership and risk analysis.
``
