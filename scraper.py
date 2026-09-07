"""
Price Tracker Scraper
Extracts product data (title, price, rating, availability) from an e-commerce
site and stores it as CSV, accumulating a price-history log across runs.
"""

import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGES = 5
REQUEST_DELAY = 1  # seconds between requests, to avoid overloading the server

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_page(url: str) -> BeautifulSoup:
    """Fetch a page and return it as a parsed BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def parse_product(product_html) -> dict:
    """Extract structured data from a single product's HTML block."""
    title = product_html.h3.a["title"]

    price_text = product_html.find("p", class_="price_color").get_text()
    price = float(price_text.replace("£", "").strip())

    availability = product_html.find("p", class_="instock").get_text(strip=True)

    rating_word = product_html.find("p", class_="star-rating")["class"][1]
    rating = RATING_MAP.get(rating_word)

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def scrape_all_products() -> pd.DataFrame:
    """Scrape every product across all configured pages into one DataFrame."""
    all_products = []

    for page_num in range(1, TOTAL_PAGES + 1):
        url = BASE_URL.format(page_num)
        print(f"Scraping page {page_num}/{TOTAL_PAGES} ...")

        soup = fetch_page(url)
        products = soup.find_all("article", class_="product_pod")

        for product in products:
            all_products.append(parse_product(product))

        time.sleep(REQUEST_DELAY)

    return pd.DataFrame(all_products)


if __name__ == "__main__":
    df = scrape_all_products()
    df.to_csv("data/products_latest.csv", index=False, encoding="utf-8-sig")

    # Append to a running history file, enabling price-change tracking over time
    try:
        history = pd.read_csv("data/price_history.csv")
        history = pd.concat([history, df], ignore_index=True)
    except FileNotFoundError:
        history = df

    history.to_csv("data/price_history.csv", index=False, encoding="utf-8-sig")

    print(f"\nScraped {len(df)} products successfully.")
    print("Saved to data/products_latest.csv and data/price_history.csv")
