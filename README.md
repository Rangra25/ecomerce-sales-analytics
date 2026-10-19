[README.md](https://github.com/user-attachments/files/33650942/README.md)
# E-commerce Sales & Profitability Analytics

A beginner-friendly Data Analyst portfolio project using SQL, Python, Pandas, Streamlit, and Plotly.

> **Dataset note:** `data/sales_data.csv` is a synthetic dataset generated for this portfolio project. It does not represent a real company. Be transparent about this in interviews.

## What it does
- Tracks revenue, profit, order count, average order value, and profit margin.
- Provides interactive filters for date range, region, category, and sales channel.
- Visualizes monthly revenue, category revenue, regional profit, and sales-channel mix.
- Includes SQL practice queries for KPIs, monthly trends, category/region performance, CTEs, and window functions.
- Allows filtered data to be downloaded as CSV.

## Project structure
```text
ecommerce_sales_analytics/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sales_data.csv
└── sql/
    └── analysis_queries.sql
```

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```

## Deploy online
You can deploy this repository using Streamlit Community Cloud:
1. Push this project folder to a GitHub repository.
2. Sign in to Streamlit Community Cloud and connect that repository.
3. Select `app.py` as the main file and deploy.
4. Test the public URL in a private/incognito browser before sharing it.

Deployment requires your own GitHub and Streamlit accounts. Do not put passwords or API keys in the repository.

## Suggested analysis questions
1. Which category generates the highest revenue?
2. Which region generates the highest profit?
3. How does revenue change month to month?
4. Which sales channel contributes the most revenue?
5. Which products have a profit margin below the overall average?
6. Does the leading category change when the date range is filtered?

## How to discuss this project in an interview
Use only claims you have verified yourself after running the app and reviewing the SQL.

**Example explanation:**
"I built an interactive sales analytics dashboard on a synthetic e-commerce dataset. I used SQL to calculate KPIs and analyse monthly, category, region, and channel performance. In Python and Streamlit, I created interactive filters and visualizations. The goal is to help a business understand revenue and profitability patterns."

Be prepared to explain:
- Revenue vs. profit vs. profit margin.
- Why `100.0` is used in SQL percentage calculations.
- `GROUP BY`, CTEs, `CASE WHEN`, and window functions.
- How each dashboard KPI is calculated.
- Limitations of synthetic data and why real business recommendations need real data.

## Resume bullet (use after you have run and understood it)
**E-commerce Sales & Profitability Analytics | SQL, Python, Pandas, Streamlit, Plotly**
- Built an interactive dashboard to explore revenue, profit, order volume, average order value, and profit margin by date, category, region, and sales channel.
- Wrote analytical SQL queries using aggregations, CTEs, and window functions to examine sales trends and product profitability.

## Before putting it on your resume
- Run the app yourself.
- Check the outputs and understand the formulas.
- Make at least one meaningful improvement of your own.
- Clearly label the data as synthetic.
