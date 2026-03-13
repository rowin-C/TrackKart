from playwright.sync_api import sync_playwright
import re
import json
import os
import requests
import csv
from datetime import datetime

# 🔹 Telegram config
BOT_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CHAT_ID = "xxxxxxxxxxxxxxx"

PRODUCTS = [
    {
        "name": "Samsung S24",
        "url": "https://www.flipkart.com/samsung-galaxy-s24-5g-snapdragon-marble-gray-128-gb/p/itm8f6413060b707",
        "threshold": 43000
    },
    {
        "name": "Pixel 9a",
        "url": "https://www.flipkart.com/google-pixel-9a-porcelain-256-gb/p/itmfe749ceddac9a",
        "threshold": 38000
    },
]

STATE_FILE = "price_state.json"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)


def extract_price_from_html(html):
    prices = re.findall(r'₹[\d,]+', html)

    cleaned = [
        int(p.replace("₹", "").replace(",", ""))
        for p in prices
    ]

    for i in range(len(cleaned) - 1):
        current_price = cleaned[i]
        next_price = cleaned[i + 1]

        if current_price > 1000 and next_price < 1000:
            return current_price

    return None


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


LOG_FILE = "price_history.csv"

def log_price(name, price):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "product", "price"])

        writer.writerow([timestamp, name, price])


def main():
    state = load_state()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for product in PRODUCTS:
            name = product["name"]
            url = product["url"]
            threshold = product["threshold"]

            page.goto(url)
            page.wait_for_timeout(4000)

            html = page.content()
            price = extract_price_from_html(html)

            if price is None:
                print(f"{name}: Price not found")
                continue

            print(f"{name}: {price}")
            log_price(name, price)

            last_alerted_price = state.get(name)

            if price <= threshold and last_alerted_price != price:
                message = f"🔥 Price Drop!\n{name}\nNow: ₹{price}\nThreshold: ₹{threshold}"
                send_telegram(message)
                state[name] = price

        browser.close()

    save_state(state)


if __name__ == "__main__":
    main()
