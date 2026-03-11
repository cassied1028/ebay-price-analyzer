from __future__ import annotations

import json
from pathlib import Path
from statistics import mean, median
from typing import Any
import subprocess

from fastapi import FastAPI, HTTPException, Query, Request
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


def load_listings(mode: str) -> list[dict[str, Any]]:
    data_file = DATA_SOLD_FILE if mode == "sold" else DATA_CURRENT_FILE
    if not data_file.exists():
        raise HTTPException(status_code=404, detail=f"No {mode} data yet")
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
    sold_raw = load_listings("sold")
    current_raw = load_listings("current")

    sold_cleaned, sold_stats = clean_listings(sold_raw, limit)
    current_cleaned, current_stats = clean_listings(current_raw, limit)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "sold_listings": sold_cleaned,
            "sold_stats": sold_stats,
            "current_listings": current_cleaned,
            "current_stats": current_stats,
        },
    )


@app.post("/search")
def run_search(q: str = Form(...)):
    scraper = str(ROOT / "scraper" / "index.js")

    # IMPORTANT: this assumes your index.js supports a final arg: "sold" or "current"
    subprocess.run(["node", scraper, q, "sold"], check=True)
    subprocess.run(["node", scraper, q, "current"], check=True)

    return RedirectResponse(url="/", status_code=303)