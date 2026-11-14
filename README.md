# Finnish Data & ICT Job Market Analytics

In this project, Finnish data and ICT job market statistics are collected, processed, stored and visualized.

The data is retrieved from Statistics Finland's PxWeb API. The project focuses on monthly statistics about jobseekers and open vacancies in selected data and ICT occupations in Finland and Uusimaa.

## Project structure

```text
finnish-data-ict-job-market/
├── data/
│   ├── raw/
│   │   └── job_market_data.json
│   └── processed/
│       └── job_market_data.csv
├── database/
│   └── job_market.db
├── src/
│   ├── inspect_api.py
│   ├── extract.py
│   ├── transform.py
│   └── database.py
├── dashboard/
│   └── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Instructions

1. Clone this repository.

2. Create and activate a virtual environment.

In Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

3. Install the required libraries:

```cmd
pip install -r requirements.txt
```

4. Run the data pipeline in the following order:

```cmd
python src/extract.py
python src/transform.py
python src/database.py
```

5. Start the dashboard:

```cmd
streamlit run dashboard/app.py
```

6. Open the dashboard in your browser at:

http://localhost:8501

## Data source

Statistics Finland – PxWeb API

https://pxdata.stat.fi/PxWeb/api/v1/fi/StatFin/tyonv/12tu.px

The original statistics are provided by the KEHA Centre Employment Service Statistics.
