from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "customers_raw.csv"
DB_PATH = PROJECT_ROOT / "data" / "db" / "analytics.db"
COLUMNS = ["customer_id", "city", "monthly_spend", "churned"]


def main() -> None:
    customers = pd.read_csv(
        CSV_PATH,
        dtype={
            "customer_id": "int64",
            "city": "string",
            "monthly_spend": "float64",
            "churned": "int64",
        },
    )
    if list(customers.columns) != COLUMNS:
        raise ValueError(f"CSV must contain these columns in order: {COLUMNS}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS customers_raw (
                customer_id INTEGER PRIMARY KEY,
                city TEXT NOT NULL,
                monthly_spend REAL NOT NULL,
                churned INTEGER NOT NULL CHECK (churned IN (0, 1))
            )
            """
        )
        connection.execute("DELETE FROM customers_raw")
        connection.executemany(
            """
            INSERT INTO customers_raw
                (customer_id, city, monthly_spend, churned)
            VALUES (?, ?, ?, ?)
            """,
            customers.itertuples(index=False, name=None),
        )

    print(f"Loaded {len(customers)} customers into {DB_PATH}")


if __name__ == "__main__":
    main()
