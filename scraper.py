import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

# Product URLs
products = {
    "amazon": [
        {
            "name": "iPhone 16 Pro",
            "url": "https://www.amazon.in/dp/B0DGHYQQ6J"
        },
        {
            "name": "iPhone 16",
            "url": "https://www.amazon.in/dp/B0DGJKT2V7"
        }
    ],
    "flipkart": [
        {
            "name": "iPhone 16 Pro",
            "url": "https://www.flipkart.com/apple-iphone-16-pro-natural-titanium-128-gb/p/itm4397c54ec56b7"
        },
        {
            "name": "iPhone 16",
            "url": "https://www.flipkart.com/apple-iphone-16-white-256-gb/p/itma0ed9b33a2973"
        }
    ]
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_amazon(product):
    try:
        r = requests.get(product["url"], headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")

        price_tag = soup.select_one("span.a-offscreen") or soup.find("span", class_="a-price-whole")
        rating_tag = soup.select_one("span.a-icon-alt")
        availability_tag = soup.select_one("#availability span")

        # Optional: Log missing fields for debugging
        if not price_tag or not rating_tag or not availability_tag:
            print(f"[DEBUG] Missing data for {product['name']}")

        return {
            "name": product["name"],
            "price": price_tag.text.strip() if price_tag else "N/A",
            "rating": rating_tag.text.strip() if rating_tag else "N/A",
            "availability": availability_tag.text.strip() if availability_tag else "N/A",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return {
            "name": product["name"],
            "price": "Error",
            "rating": "Error",
            "availability": str(e),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def scrape_flipkart(product):
    try:
        r = requests.get(product["url"], headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        price = soup.select_one("div._30jeq3")
        rating = soup.select_one("div._3LWZlK")
        availability = "Available" if price else "Out of stock"

        return {
            "name": product["name"],
            "price": price.text.strip() if price else "N/A",
            "rating": rating.text.strip() if rating else "N/A",
            "availability": availability,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"name": product["name"], "price": "Error", "rating": "Error", "availability": str(e), "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

def append_to_csv(filename, data):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([data["time"], data["name"], data["price"], data["rating"], data["availability"]])

# Main script
for p in products["amazon"]:
    result = scrape_amazon(p)
    append_to_csv("amazonsr.csv", result)

for p in products["flipkart"]:
    result = scrape_flipkart(p)
    append_to_csv("flipkarsr.csv", result)
