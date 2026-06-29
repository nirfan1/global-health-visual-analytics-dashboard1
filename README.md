# Global Health Indicators Visual Analytics Dashboard

## Project Overview

This project is an interactive visual analytics dashboard designed to help users explore global health indicators across countries, regions, and years. The dashboard supports quick comparison, trend analysis, and pattern discovery through filters, charts, summary metrics, and a data table.

The project was created as a portfolio project for Information Systems, Business Analytics, Data Analytics, and IT Business Analyst internship applications.

## Problem Statement

Health data is often difficult to understand when it is stored in large tables. Decision-makers need a clear way to compare indicators, identify changes over time, and understand differences between countries or regions.

This dashboard solves that problem by turning health indicator data into interactive visuals that are easier to explore and explain.

## Main Features

- Upload and analyse a health indicators CSV file.
- Filter data by year, country, region, and indicator.
- View key summary metrics such as number of countries, indicators, year range, and average value.
- Analyse indicator trends over time.
- Compare countries for a selected indicator.
- View regional averages.
- Explore relationships between indicators using a correlation heatmap.
- Download the filtered dataset for further analysis.

## Tools and Technologies

- Python
- Streamlit
- Pandas
- Plotly
- CSV data processing
- Data visualisation
- Business analytics

## Dataset Format

The dashboard works best with a CSV file in long format:

| Country | Region | Year | Indicator | Value |
|---|---|---:|---|---:|
| Australia | Oceania | 2023 | Obesity Rate | 31.2 |

The app can also handle some wide-format datasets where indicators are separate numeric columns.

## How to Run the Project

1. Install Python.
2. Open the project folder in VS Code.
3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

5. Open the local link shown in the terminal.

## Suggested CV Description

Global Health Indicators Visual Analytics Dashboard  
- Built an interactive dashboard to analyse country-level health indicators using filters, charts, summary metrics, and trend comparisons.
- Used Python, Streamlit, Pandas, and Plotly to transform raw CSV data into clear visual insights for decision-making.
- Designed the dashboard to support data exploration, regional comparison, and communication of key patterns.

## Suggested LinkedIn Project Description

Created an interactive visual analytics dashboard to explore global health indicators across countries, regions, and years. The project includes trend charts, country comparisons, regional averages, summary metrics, a correlation heatmap, and downloadable filtered data. This project strengthened my skills in data analysis, dashboard design, Python, Streamlit, Pandas, and data storytelling.

## Folder Structure

```text
visual_analytics_dashboard_project/
│
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── sample_health_indicators.csv
```

## Notes

The sample dataset is only included so the dashboard runs immediately. For a real portfolio version, replace it with your actual dataset or a properly referenced public dataset.
