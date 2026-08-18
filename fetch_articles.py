import re
import requests
import json
from bs4 import BeautifulSoup

def fetch_article_links():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/139.0.0.0 Safari/537.36"
        )
    }
    session = requests.Session()
    session.headers.update(headers)

    BASE_URL = "https://iponcomp.com/sitemap.xml"

    try:
        response = session.get(BASE_URL, timeout=30)
        content = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print("Fetching sitemap xml failed")

        ###
        # Code below will fetch sitemap.xml and check if any of 
        # the product pages updated since last fetched

    if content:
        try:
            all_links_url = content.find_all("loc")
            all_links_time = content.find_all("lastmod")

            all_links_url = [link.get_text() for link in all_links_url]
            all_links_time = [link.get_text() for link in all_links_time]

            links = list(zip(all_links_url, all_links_time))

            exp = re.compile(r"https://media.icdn.hu/sitemap/product_\d-en_HU.xml")
            article_links = [link for link in links if exp.fullmatch(link[0])]

            all_links_final = []
            counter = 1
            for article_link in article_links:
                link_dict = {"url" : article_link[0], "date" : article_link[1], "visited": "0", "page" : counter}
                counter += 1
                all_links_final.append(link_dict)

            with open("sitemap_links.json", "r", encoding="utf-8") as file:
                old_list = json.load(file)

            for i in range(len(all_links_final)):
                if old_list[i]["date"] >= all_links_final[i]["date"]:
                    all_links_final[i]["visited"] = "1"

            with open("sitemap_links.json", "w", encoding="utf-8") as file:
                json.dump(all_links_final, file, indent=2)
        except Exception as e:
            print("Error occured:", e)

        ###
        # Code below will fetch all links that were updated 
        # and parse them for individual article links

        all_article_links = []
        try:
            with open("sitemap_links.json", "r", encoding="utf-8") as file:
                all_links_final = json.load(file)
            for article_link in all_links_final:
                if article_link["visited"] == "0":
                    link_id = 1
                    inner_response = session.get(article_link["url"], timeout=30)
                    inner_content = BeautifulSoup(inner_response.text, "html.parser")
                    article_links = inner_content.find_all("loc")
                    article_links = [link.get_text() for link in article_links]
                    for link in article_links:
                        link_dict = {"id" : link_id, "url" : link, "visited" : "0"}
                        link_id += 1
                        all_article_links.append(link_dict)

                    with open(f"links/article_links_{article_link["page"]}.json", "w", encoding="utf-8") as file:
                        json.dump(all_article_links, file, indent=2)
                        all_article_links = []

                    article_link["visited"] = "1"
                else:
                    print("Link already visited")

            with open("sitemap_links.json", "w", encoding="utf-8") as file:
                json.dump(all_links_final, file, indent=2)

        except Exception as e:
            print("Error occured:", e)