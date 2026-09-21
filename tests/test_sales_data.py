import pandas as pd
import pytest

from sales_data import load_sales_data, total_sales, total_orders

CSV_CONTENT = """date,order_id,product,category,region,quantity,unit_price,total_amount
2024-01-15,ORD-1,Widget,Electronics,North,1,100.0,100.0
2024-02-10,ORD-2,Widget,Electronics,North,1,200.0,200.0
"""


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date": pd.to_datetime([
            "2024-01-15", "2024-01-20", "2024-02-10", "2024-02-15", "2024-03-05",
        ]),
        "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4", "ORD-5"],
        "product": ["A", "B", "C", "D", "E"],
        "category": ["Electronics", "Audio", "Electronics", "Wearables", "Audio"],
        "region": ["North", "South", "North", "East", "West"],
        "quantity": [1, 2, 1, 3, 2],
        "unit_price": [100.0, 50.0, 200.0, 30.0, 25.0],
        "total_amount": [100.0, 100.0, 200.0, 90.0, 50.0],
    })


def test_load_sales_data_reads_csv(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(CSV_CONTENT)

    df = load_sales_data(str(csv_path))

    assert len(df) == 2
    assert list(df.columns) == [
        "date", "order_id", "product", "category",
        "region", "quantity", "unit_price", "total_amount",
    ]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_sales_data_raises_on_missing_column(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text("date,order_id\n2024-01-15,ORD-1\n")

    with pytest.raises(ValueError):
        load_sales_data(str(csv_path))


def test_total_sales(sample_df):
    assert total_sales(sample_df) == 540.0


def test_total_orders(sample_df):
    assert total_orders(sample_df) == 5
