import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def load_sales_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"sales data is missing required columns: {missing}")
    df["date"] = pd.to_datetime(df["date"])
    return df


def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)
