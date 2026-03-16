
# 🛍️ eBay Sold Listings Analyzer

A full-stack pricing analysis tool that helps eBay resellers determine realistic market prices using live listing data.

This project uses:

* **Puppeteer (Node.js)** to scrape sold eBay listings
* **FastAPI (Python)** to analyze pricing data
* **Server-rendered HTML (Jinja templates)** to display results in a clean dashboard
* **Pytest** to validate API routes, helper logic, and scraper output

The app helps determine realistic pricing using:

* Median prices
* Average prices
* Min / Max
* Total price (item + shipping)
* Sell-through rate

---

## 📂 Project Structure

```
project-root/
├── backend/
│   ├── app.py                 # FastAPI backend
│   ├── __init__.py            # Makes backend a Python package
│   └── templates/
│       └── index.html         # Server-rendered dashboard
│
├── scraper/
│   ├── index.js               # Puppeteer scraper
│   ├── package.json
│   └── package-lock.json
│
├── web/
│   └── styles.css             # Static styling
│
├── data/
│   ├── ebay_sold_results.json # Generated data (ignored in git)
│   └── ebay_current_results.json # Generated data (ignored in git)
│
├── tests/                     # Regression tests
│   ├── test_api.py
│   ├── test_app_helpers.py
│   └── test_data_format.py
│
├── pytest.ini                 # Pytest configuration
│
├── screenshots/               # Puppeteer debug screenshots
├── venv/                      # Python virtual environment (ignored)
└── README.md
```

---

## ⚙️ How It Works

### 1️⃣ Scraper (`scraper/index.js`)

* Launches a headless Chromium browser
* Searches eBay for a specified query
* Collects both:
  * sold/completed listings
  * current active listings
* Extracts:
  * title
  * item price
  * shipping price
  * image
* Saves results to:

```text
data/ebay_sold_results.json
data/ebay_current_results.json
```

The scraper is triggered automatically by the FastAPI backend when a user submits a search from the dashboard.

You can modify the number of listings scraped by changing:

```js
const search_number = 25;
```

---

### 2️⃣ Backend (`backend/app.py`)

* Loads scraped JSON data
* Calculates:

  * Median
  * Mean
  * Min / Max
  * Total price (item + shipping)
* Renders a pricing dashboard using Jinja templates

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone <repo-url>
cd project-root
```

---

### 2️⃣ Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn jinja2 python-multipart pytest httpx
```

---

### 3️⃣ Install Node dependencies (scraper only)

```bash
cd scraper
npm install
cd ..
```

---

## 🚀 Running the Application

### 1️⃣ Start the backend server

uvicorn backend.app:app --reload --port 3000

### 2️⃣ Open the dashboard

http://localhost:3000

### 3️⃣ Search for an item

Enter an eBay search query using the search bar.

When a search is submitted, the backend automatically:

• runs the Puppeteer scraper  
• collects sold and current listings  
• saves results to the `data/` folder  
• reloads the dashboard with pricing analysis

---
## Running Tests
This project includes regression tests for:

• FastAPI API routes
• helper functions used for pricing analysis
• JSON scraper output structure

Tests are located in the tests/ directory.

### Run all tests:

```bash
python -m pytest -v
```

The included pytest.ini file configures pytest so the project root is automatically added to the Python path, allowing imports like:

```py
from backend.app import summary
```
without needing to manually set PYTHONPATH.

---

## 🛠 Technologies Used

* Node.js
* Puppeteer
* Python 3
* FastAPI
* Jinja2
* Pytest (regression testing)
* HTML/CSS
* JSON file storage

---

## ⚠️ Notes

* This scraper relies on eBay’s current HTML structure.
* If eBay updates their layout, selectors may need updating.
* Best Offer sales do not reveal final accepted price — scraper uses displayed sold price.
* Use responsibly and in accordance with eBay’s Terms of Service.

---

## 💡 Future Improvements

* color code higher priced items & lower priced items
* Trimmed mean (remove outliers)
* CSV export?
* Deployment (Render / Railway)

---

## 📅 Project Started

February 2026

