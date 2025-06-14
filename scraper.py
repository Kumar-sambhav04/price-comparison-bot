import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# --- Products ---
flipkart_products = [
    {
        "name": "iPhone 16",
        "url": "https://www.flipkart.com/apple-iphone-16-white-256-gb/p/itma0ed9b33a2973"
    },
    {
        "name": "iPhone 16 Pro",
        "url": "https://www.flipkart.com/apple-iphone-16-pro-natural-titanium-128-gb/p/itm4397c54ec56b7"
    }
]

amazon_products = [
    {
        "name": "iPhone 16",
        "url": "https://www.amazon.in/dp/your-product-id"
    },
    {
        "name": "iPhone 16 Pro",
        "url": "https://www.amazon.in/dp/your-product-id"
    }
]

# --- ScraperAPI Key ---
SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")
if not SCRAPERAPI_KEY:
    raise ValueError("SCRAPERAPI_KEY not found in environment variables")

# --- Flipkart Scraper using ScraperAPI ---
def extract_availability(html_text):
    html_text = html_text.lower()
    if "out of stock" in html_text or "sold out" in html_text or "get notified" in html_text:
        return "Unavailable"
    else:
        return "Available"

def scrape_flipkart(product):
    try:
        scraperapi_url = f"http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url={product['url']}&render=true"
        response = requests.get(scraperapi_url, timeout=20)
        soup = BeautifulSoup(response.content, "html.parser")
        html_text = soup.get_text().lower()

        title_tag = soup.find("span", {"class": "B_NuCI"})
        if not title_tag:
            return {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": product["name"],
                "price": "Blocked or Timeout",
                "rating": "N/A",
                "availability": "N/A"
            }

        price_tag = soup.select_one("div._30jeq3")
        price = price_tag.text.strip() if price_tag else "N/A"

        availability = extract_availability(html_text)

        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": product["name"],
            "price": price,
            "rating": "N/A",
            "availability": availability
        }

    except Exception as e:
        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": product["name"],
            "price": "Error",
            "rating": "Error",
            "availability": str(e)
        }

# --- Amazon Placeholder (to be replaced later) ---
def scrape_amazon(product):
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": product["name"],
        "price": "Coming Soon (API)",
        "rating": "Coming Soon",
        "availability": "Coming Soon"
    }

# --- CSV Saver with Correct Column Order ---
def save_to_csv(data, filename):
    columns = ["time", "name", "price", "rating", "availability"]
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        if not file_exists:
            writer.writeheader()
        for row in data:
            writer.writerow(row)

# --- Main Execution ---
if __name__ == "__main__":
    print("Scraping Flipkart...")
    flipkart_data = [scrape_flipkart(p) for p in flipkart_products]
    save_to_csv(flipkart_data, "flipkarsr.csv")

    print("Scraping Amazon...")
    amazon_data = [scrape_amazon(p) for p in amazon_products]
    save_to_csv(amazon_data, "amazonsr.csv")

    print("Data saved to CSV files.")
