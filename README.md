# Price Tracker Scraper

A Python tool that scrapes product data from an e-commerce site, stores it, and analyzes pricing trends.

## What it does

- Scrapes product **title, price, rating, and availability** across multiple pages
- Stores results in `data/products_latest.csv`
- Appends every run to `data/price_history.csv`, enabling **historical price tracking** across multiple scrapes
- Analyzes the data: average/min/max price, top cheapest and most expensive items, product count by rating
- Generates a price-distribution chart (`data/price_distribution.png`)

## Tech stack

`Python` · `Requests` · `BeautifulSoup` · `Pandas` · `Matplotlib`

## Usage

```bash
pip install requests beautifulsoup4 pandas matplotlib
python scraper.py     # collects and saves the data
python analyze.py     # analyzes the data and generates the chart
```

## Design notes

- **Rate limiting**: a 1-second delay is added between page requests to avoid overloading the server.
- **Custom User-Agent header**: sent with each request to identify as a standard browser.
- **Historical tracking**: each scraper run appends to a persistent CSV, so price changes can be analyzed over time rather than only viewing a single snapshot.

## Adapting to another site

The core logic (`fetch_page` → `parse_product` → `scrape_all_products`) generalizes to most static e-commerce pages. To adapt:

1. Check the target site's `robots.txt` before scraping anything.
2. Inspect the page (browser dev tools) to find the correct HTML tags/classes for price, title, etc., and update the selectors in `parse_product`.
3. For JavaScript-rendered sites, `requests` won't see the final content — use `Selenium` or `Playwright` instead.
4. Keep respectful rate limits and rotate `User-Agent`/proxies for larger-scale scraping.

## Example project use case

This pattern extends directly into a real freelance service: scheduled daily scraping, price-drop alerts (email/Telegram), and a database (SQLite/PostgreSQL) instead of CSV for production use.
