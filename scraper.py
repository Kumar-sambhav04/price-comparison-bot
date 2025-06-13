import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# Product lists
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

flipkart_products = [
    {
        "name": "iPhone 16",
        "url": "https://www.flipkart.com/apple-iphone-16-white-256-gb/p/itma0ed9b33a2973?pid=MOBH4DQFCU7ZY9HG&lid=LSTMOBH4DQFCU7ZY9HGLY6DQP&marketplace=FLIPKART&q=iphone%2016%20&sattr[]=color&sattr[]=storage&st=storage"
    },
    {
        "name": "iPhone 16 Pro",
        "url": "https://www.flipkart.com/apple-iphone-16-pro-natural-titanium-128-gb/p/itm4397c54ec56b7?pid=MOBH4DQFX4FR2HYZ&lid=LSTMOBH4DQFX4FR2HYZKVRW3N&marketplace=FLIPKART&q=iphone+16+pro&store=tyy%2F4io&srno=s_1_1&otracker=AS_Query_OrganicAutoSuggest_3_9_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_9_na_na_na&fm=search-autosuggest&iid=321f70d5-3781-4ad0-bbba-70bf9fb14dcf.MOBH4DQFX4FR2HYZ.SEARCH&ppt=sp&ppn=sp&ssid=ijf9jpd2bk0000001749620886044&qH=6f0b50cc832ce851"
    }
]

# Headers to simulate browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# --- AMAZON (Placeholder) ---
def scrape_amazon(product):
    return {
        "name": product["name"],
        "price": "Coming Soon (API)",
        "rating": "Coming Soon",
        "availability": "Coming Soon",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# --- FLIPKART Scraper ---
def extract_availability(html_text):
    html_text = html_text.lower()
    if "out of stock" in html_text or "sold out" in html_text or "get notified" in html_text:
        return "Unavailable"
    else:
        return "Available"

def scrape_flipkart(product):
    try:
        r = requests.get(product["url"], headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        html_text = soup.get_text()

        price_tag = soup.select_one("div._30jeq3")
        price = price_tag.text.strip() if price_tag else "N/A"

        availability = extract_availability(html_text)

        return {
            "name": product["name"],
            "price": price,
            "rating": "N/A",  # Ratings aren't in static HTML
            "availability": availability,
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

# --- CSV Saving ---
def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["name", "price", "rating", "availability", "time"])
        if not file_exists:
            writer.writeheader()
        for row in data:
            writer.writerow(row)

# --- Main Function ---
if __name__ == "__main__":
    print("🔍 Scraping Flipkart...")
    flipkart_data = [scrape_flipkart(p) for p in flipkart_products]
    save_to_csv(flipkart_data, "flipkarsr.csv")

    print("🔍 Scraping Amazon (placeholder)...")
    amazon_data = [scrape_amazon(p) for p in amazon_products]
    save_to_csv(amazon_data, "amazonsr.csv")

    print("Data saved to CSVs")
