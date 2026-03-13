# TrackKart 🛒

A Flipkart product price tracker built with Playwright that monitors product prices and sends you a Telegram notification when the price drops below your set threshold.

## Features

- Scrapes live product prices from Flipkart using Playwright
- Set a custom price threshold per product
- Instant Telegram notification when price drops below threshold
- Tracks price history in a local CSV file (`price_history.csv`)
- Avoids duplicate alerts using a JSON state file (`price_state.json`)
- Supports tracking multiple products at once
- Runs headlessly in the background

## Requirements

- Python 3.12+
- Playwright
- A Telegram Bot token and chat ID

## Installation

```bash
git clone https://github.com/rowin-C/TrackKart.git
cd TrackKart
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

## Configuration

Create a `.env` file in the root directory:

```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
PRODUCT_URL=https://www.flipkart.com/your-product-url
PRICE_THRESHOLD=999
```

> **How to get your Telegram Bot Token and Chat ID:**
> Follow this tutorial → [How to Create a Telegram Bot and Get Chat ID](https://core.telegram.org/bots/tutorial)

## Usage

```bash
python price_test.py
```

The script will launch a headless browser, scrape the current price, log it, and send a Telegram alert if the price is at or below your threshold.

## Tracking Multiple Products

You can track multiple products by appending items to the `PRODUCTS` array in `main.py`:

```python
PRODUCTS = [
    {
        "name": "Samsung S24",
        "url": "https://www.flipkart.com/samsung-s24-url",
        "threshold": 55000
    },
    {
        "name": "boAt Headphones",
        "url": "https://www.flipkart.com/boat-headphones-url",
        "threshold": 1499
    },
    {
        "name": "Logitech Mouse",
        "url": "https://www.flipkart.com/logitech-mouse-url",
        "threshold": 799
    },
]
```

Each product has its own name, URL, and price threshold. You'll get a separate Telegram notification for each product that drops below its threshold.

## How It Works

1. Playwright launches a headless Chromium browser
2. It navigates to each Flipkart product page
3. Scrapes and parses the current price from the page HTML
4. Logs the price with a timestamp to `price_history.csv`
5. Compares the price against your set threshold
6. If the price is at or below the threshold and hasn't already been alerted at that price, a Telegram message is sent
7. State is saved to `price_state.json` to prevent duplicate notifications

## Telegram Notification Format

```
🔥 Price Drop!
Samsung S24
Now: ₹54999
Threshold: ₹55000
```

## .gitignore Recommendations

Make sure your `.gitignore` includes:

```
venv/
.env
__pycache__/
*.pyc
price_state.json
price_history.csv
```

## License

MIT
