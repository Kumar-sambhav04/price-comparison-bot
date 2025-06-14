import csv
import os
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Product Lists ---
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
        "url": "https://www.flipkart.com/apple-iphone-16-white-256-gb/p/itma0ed9b33a2973?pid=MOBH4DQFCU7ZY9HG"
    },
    {
        "name": "iPhone 16 Pro",
        "url": "https://www.flipkart.com/apple-iphone-16-pro-natural-titanium-128-gb/p/itm4397c54ec56b7?pid=MOBH4DQFX4FR2HYZ"
    }
]

# --- Flipkart Scraper using Selenium ---
def scrape_flipkart(product):
    try:
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=options)
        driver.get(product["url"])
        wait = WebDriverWait(driver, 10)

        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "B_NuCI")))
        except:
            driver.quit()
            return {
                "name": product["name"],
                "price": "Blocked or Timeout",
                "rating": "N/A",
                "availability": "N/A",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        try:
            price_element = driver.find_element(By.CLASS_NAME, "_30jeq3")
            price = price_element.text.strip()
        except:
            price = "N/A"

        page_text = driver.page_source.lower()
        availability = "Unavailable" if any(x in page_text for x in ["out of stock", "sold out", "notify me"]) else "Available"

        driver.quit()

        return {
            "name": product["name"],
            "price": price,
            "rating": "N/A",
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

# --- Amazon API Placeholder ---
def scrape_amazon(product):
    return {
        "name": product["name"],
        "price": "Coming Soon (Amazon API)",
        "rating": "Coming Soon",
        "availability": "Coming Soon",
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

# --- Main Script ---
if __name__ == "__main__":
    print("🔍 Scraping Flipkart...")
    flipkart_data = [scrape_flipkart(p) for p in flipkart_products]
    save_to_csv(flipkart_data, "flipkarsr.csv")

    print("🔍 Scraping Amazon (Placeholder)...")
    amazon_data = [scrape_amazon(p) for p in amazon_products]
    save_to_csv(amazon_data, "amazonsr.csv")

    print("Data saved to CSVs.")
