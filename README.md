# Applied Analytics: Customer City KPIs

A small beginner-friendly project that loads customer data from a CSV file into
SQLite and calculates simple KPIs for one city.

## Project structure

```text
data/
  db/analytics.db
  raw/customers_raw.csv
src/
  etl_load_sqlite.py
  kpi_city.py
tests/
  test_kpi_city.py
requirements.txt
```

The SQLite database is created by the ETL script and is ignored by Git.

## Run the project

Open PowerShell in the project folder. These commands assume that `.venv` is
already created and activated.

```powershell
python -m pip install -r requirements.txt
python src\etl_load_sqlite.py
python src\kpi_city.py
python -m pytest
```

The KPI script prints Mumbai's KPIs and then tries a SQL-injection-style city
name. The second call returns no matching city data.
