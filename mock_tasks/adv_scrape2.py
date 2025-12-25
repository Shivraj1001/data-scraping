import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def scrape_page(url, writer):
    headers = {"User-Agent":"Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return False
    except requests.exceptions.RequestException:
        return False
    
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]

        price_tag = book.find("p", class_="price_color")
        if price_tag is None:
            continue

        price_text = price_tag.text
        price = float(price_text.replace("£", "").replace("Â", "").strip())
        writer.writerow([title, price])
    return True

with open("adv2.csv", "w", newline="", encoding="utf-8")as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price"])

    page = 1
    url = "https://books.toscrape.com/"

    while True:
        success = scrape_page(url, writer)
        if not success:
            break

        print(f"---Page {page} scrapped---")
        page += 1

        response = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        next_tag = soup.find("li", class_="next")
        if next_tag:
            next_url = next_tag.a["href"]
            url = urljoin(url, next_url)
        else:
            break
