from contextlib import closing
from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "db" / "analytics.db"


def city_kpi(city: str) -> dict[str, int | float | str] | None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}; run src\\etl_load_sqlite.py first."
        )

    query = """
        SELECT
            COUNT(*) AS customer_count,
            AVG(monthly_spend) AS average_monthly_spend,
            SUM(churned) * 100.0 / COUNT(*) AS churn_rate_pct
        FROM customers_raw
        WHERE city = ?
    """
    with closing(sqlite3.connect(DB_PATH)) as connection:
        row = connection.execute(query, (city,)).fetchone()

    customer_count = row[0]
    if customer_count == 0:
        return None

    return {
        "city": city,
        "customer_count": customer_count,
        "average_monthly_spend": round(row[1], 2),
        "churn_rate_pct": round(row[2], 2),
    }


if __name__ == "__main__":
    print(city_kpi("Mumbai"))
    print(city_kpi("Mumbai' OR 1=1 --"))
