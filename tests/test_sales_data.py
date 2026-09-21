import pandas as pd
import pytest

from sales_data import load_sales_data

CSV_CONTENT = """date,order_id,product,category,region,quantity,unit_price,total_amount
2024-01-15,ORD-1,Widget,Electronics,North,1,100.0,100.0
2024-02-10,ORD-2,Widget,Electronics,North,1,200.0,200.0
"""


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
