"""
Price Tracker Analysis
Reads the scraped product data and reports summary statistics, top/bottom
priced items, and a price-distribution chart.
"""

import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = "data/products_latest.csv"


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE)


def print_summary(df: pd.DataFrame) -> None:
    print("=" * 50)
    print(f"Total products: {len(df)}")
    print(f"Average price: £{df['price'].mean():.2f}")
    print(f"Lowest price: £{df['price'].min():.2f}")
    print(f"Highest price: £{df['price'].max():.2f}")
    print("=" * 50)

    print("\nTop 5 cheapest products:")
    print(df.nsmallest(5, "price")[["title", "price"]].to_string(index=False))

    print("\nTop 5 most expensive products:")
    print(df.nlargest(5, "price")[["title", "price"]].to_string(index=False))

    print("\nProduct count by rating:")
    print(df["rating"].value_counts().sort_index().to_string())


def plot_price_distribution(df: pd.DataFrame, output_path="data/price_distribution.png") -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(df["price"], bins=15, color="#4A90D9", edgecolor="white")
    plt.title("Price Distribution")
    plt.xlabel("Price (£)")
    plt.ylabel("Number of Products")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"\nChart saved to {output_path}")


if __name__ == "__main__":
    df = load_data()
    print_summary(df)
    plot_price_distribution(df)
