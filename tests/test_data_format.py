import json
from pathlib import Path

CURRENT_FILE = Path("data/ebay_current_results.json")
SOLD_FILE = Path("data/ebay_sold_results.json")

def load_json_file(path: Path):
    assert path.exists(), f'{path} does not exist'
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{path} should contain a dict"
    return data

#helper for testing json files
def validate_listing_structure(data):
    assert "totalListingCount" in data
    assert "fewerWordsFallback" in data
    assert "listings" in data

    listing_count = data["totalListingCount"]
    assert isinstance(listing_count, int), f"{listing_count} should be an int"

    fewer_words_fallback = data["fewerWordsFallback"]
    assert isinstance(fewer_words_fallback, bool), f"{fewer_words_fallback} should be a bool"

    listings = data["listings"]
    assert isinstance(listings, list), f"{listings} should be a list"

    #checking all listing formatting
    for listing in listings:
        assert isinstance(listing,dict), f"{listing} should be a dict"

        #Checking for correct keys
        required_keys = {
            "Title",
            "Price",
            "Shipping",
            "Image",
            "ItemPrice",
            "ShippingPrice"
        }
        assert required_keys.issubset(listing.keys())

        #checking for correct values
        assert isinstance(listing["Title"], str)
        assert isinstance(listing["Price"], str)
        assert isinstance(listing["Shipping"], str)
        assert isinstance(listing["Image"], str)
        assert isinstance(listing["ItemPrice"], (int, float))
        assert isinstance(listing["ShippingPrice"], (int, float))

        assert listing["ItemPrice"] >= 0
        assert listing["ShippingPrice"] >= 0


def test_sold_json_structure():
    data = load_json_file(SOLD_FILE)
    validate_listing_structure(data)

    
def test_current_json_structure():
    data = load_json_file(CURRENT_FILE)
    validate_listing_structure(data)