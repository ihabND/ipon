import re
import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0.0.0 Safari/537.36"
    )
}
session = requests.Session()
session.headers.update(headers)

visited = 0
save_interval = 10
try:
    folder = Path("links")
    for file in folder.glob("*.json"):
        print("Scraping from:", file)

        with open(file, "r", encoding="utf-8") as opened:
            product_links = json.load(opened)
        for product_link in product_links:
            if product_link["visited"] == "0":
                product_response = session.get(product_link["url"])
                product_content = BeautifulSoup(product_response.text, "html.parser")
                product_json = product_content.find("script", {"type" : "application/ld+json"})
                product_link["visited"] = "1"
                visited += 1
                if visited % save_interval == 0:
                    with open(file, "w", encoding="utf-8") as opened_write:
                        json.dump(product_links, opened_write, indent=2)



except Exception as e:
    print("Error occured:", e)