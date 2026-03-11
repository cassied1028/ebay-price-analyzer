
# 🛍️ eBay Sold Listings Analyzer

A full-stack pricing analysis tool for eBay resellers.

This project uses:

* **Puppeteer (Node.js)** to scrape sold eBay listings
* **FastAPI (Python)** to analyze pricing data
* **Server-rendered HTML (Jinja templates)** to display results in a clean dashboard

The app helps determine realistic pricing using:

* Median prices
* Average prices
* Min / Max
* Total price (item + shipping)

---

## 📂 Project Structure

```
project-root/
├── backend/
│   ├── app.py                 # FastAPI backend
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
│   └── ebay_sold_results.json # Generated data (ignored in git)
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
* Filters for:

  * Sold listings
  * Completed listings
* Extracts:

  * Title
  * Item price
  * Shipping price
* Saves results to:

```
data/ebay_sold_results.json
```

* Saves a screenshot for debugging to:
```
screenshots/current_ebay_search.png
```

You can modify two variables:

```js
const query = 'your ebay search';
const search_number = 50;
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
pip install fastapi uvicorn jinja2
```

---

### 3️⃣ Install Node dependencies (scraper only)

```bash
cd scraper
npm install
cd ..
```

---

### 4️⃣ Run the scraper

```bash
node scraper/index.js
```

---

### 5️⃣ Start the backend server

```bash
uvicorn backend.app:app --reload --port 3000
```

Open in browser:

```
http://localhost:3000
```

---

## 🛠 Technologies Used

* Node.js
* Puppeteer
* Python 3
* FastAPI
* Jinja2
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

* add search bar & run scraper from dashboard
* color code higher priced items & lower priced items
* Trimmed mean (remove outliers)
* CSV export?
* Deployment (Render / Railway)

---

## 📅 Project Started

February 2026

