from backend.app import summary, clean_listings

def test_summary_empty():
    result = summary([])
    assert result == {
        "count": 0,
        "median": None,
        "mean": None,
        "min": None,
        "max": None,
    }

def test_clean_listings_basic():
    listings = [
        {
            "Title": "Item A",
            "ItemPrice": 10,
            "ShippingPrice": 2,
            "Image": "img-a.jpg",
        },
        {
            "Title": "Item B",
            "ItemPrice": 20,
            "ShippingPrice": 0,
            "Image": "img-b.jpg",
        },
    ]

    cleaned, stats = clean_listings(listings, limit=None)

    assert len(cleaned) == 2
    assert cleaned[0]["Title"] == "Item A"
    assert cleaned[0]["ItemPrice"] == 10.0
    assert cleaned[0]["ShippingPrice"] == 2.0
    assert cleaned[0]["Image"] == "img-a.jpg"

    assert stats["listings_count"] == 2
    assert stats["item"]["median"] == 15
    assert stats["shipping"]["median"] == 1
    assert stats["total"]["median"] == 16