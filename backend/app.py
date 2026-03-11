from __future__ import annotations

import json
from pathlib import Path
from statistics import mean, median
from typing import Any
import subprocess

from fastapi import FastAPI, Query, Request
from fastapi import Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"

DATA_SOLD_FILE = ROOT / "data" / "ebay_sold_results.json"
DATA_CURRENT_FILE = ROOT / "data" / "ebay_current_results.json"

TEMPLATES_DIR = ROOT / "backend" / "templates"

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def load_listings(mode: str) -> dict[str, Any]:
    data_file = DATA_SOLD_FILE if mode == "sold" else DATA_CURRENT_FILE
    if not data_file.exists():
        return {"totalListingCount": 0, "fewerWordsFallback": False, "listings": []}
    return json.loads(data_file.read_text(encoding="utf-8"))


def summary(nums: list[float]):
    if not nums:
        return {"count": 0, "median": None, "mean": None, "min": None, "max": None}
    return {
        "count": len(nums),
        "median": round(median(nums), 2),
        "mean": round(mean(nums), 2),
        "min": round(min(nums), 2),
        "max": round(max(nums), 2),
    }


def clean_listings(listings: list[dict[str, Any]], limit: int | None):
    if limit:
        listings = listings[:limit]

    cleaned = [
        {
            "Title": x.get("Title", ""),
            "ItemPrice": float(x.get("ItemPrice", 0) or 0),
            "ShippingPrice": float(x.get("ShippingPrice", 0) or 0),
            "Image": x.get("Image", ""),
        }
        for x in listings
    ]

    item_prices = [x["ItemPrice"] for x in cleaned]
    ship_prices = [x["ShippingPrice"] for x in cleaned]
    totals = [x["ItemPrice"] + x["ShippingPrice"] for x in cleaned]

    stats = {
        "listings_count": len(cleaned),
        "item": summary(item_prices),
        "shipping": summary(ship_prices),
        "total": summary(totals),
    }

    return cleaned, stats


@app.get("/")
def homepage(request: Request, limit: int | None = Query(default=None, gt=0)):
    sold_data = load_listings("sold")
    current_data = load_listings("current")

    sold_total = sold_data["totalListingCount"]
    current_total = current_data["totalListingCount"]

    sold_raw = sold_data["listings"]
    current_raw = current_data["listings"]

    sold_cleaned, sold_stats = clean_listings(sold_raw, limit)
    current_cleaned, current_stats = clean_listings(current_raw, limit)

    sold_fewer_words = sold_data.get("fewerWordsFallback", False)
    current_fewer_words = current_data.get("fewerWordsFallback", False)

    sell_through_rate = None
    if current_total > 0:
        sell_through_rate = round((sold_total / current_total) * 100, 2)

    current_query = request.query_params.get("q", "")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "sold_listings": sold_cleaned,
            "sold_stats": sold_stats,
            "current_listings": current_cleaned,
            "current_stats": current_stats,
            "sell_through_rate": sell_through_rate,
            "sold_total": sold_total,
            "current_total": current_total,
            "sold_fewer_words":sold_fewer_words,
            "current_fewer_words":current_fewer_words,
            "current_query":current_query,

        },
    )


@app.post("/search")
def run_search(q: str = Form(...)):
    scraper = str(ROOT / "scraper" / "index.js")
    subprocess.run(["node", scraper, q], check=True)
    return RedirectResponse(url=f"/?q={q}", status_code=303)