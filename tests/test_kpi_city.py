import sqlite3

import pytest

import src.kpi_city as kpi_city


@pytest.fixture
def customers_database(tmp_path, monkeypatch):
    database_path = tmp_path / "analytics.db"
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE customers_raw (
                customer_id INTEGER PRIMARY KEY,
                city TEXT NOT NULL,
                monthly_spend REAL NOT NULL,
                churned INTEGER NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO customers_raw
                (customer_id, city, monthly_spend, churned)
            VALUES (?, ?, ?, ?)
            """,
            [
                (1, "Mumbai", 1200.00, 0),
                (2, "Mumbai", 2500.00, 1),
                (3, "Mumbai", 1800.00, 0),
                (4, "Delhi", 950.00, 0),
            ],
        )
    monkeypatch.setattr(kpi_city, "DB_PATH", database_path)
    return database_path


def test_city_kpi_returns_city_metrics(customers_database):
    assert kpi_city.city_kpi("Mumbai") == {
        "city": "Mumbai",
        "customer_count": 3,
        "average_monthly_spend": 1833.33,
        "churn_rate_pct": 33.33,
    }


def test_city_kpi_does_not_match_sql_injection(customers_database):
    assert kpi_city.city_kpi("Mumbai' OR 1=1 --") is None
