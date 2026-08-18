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

try:
    folder = Path("links")
    for file in folder.glob("*.json"):
        print("Scraping from:", file)
finally:
    pass