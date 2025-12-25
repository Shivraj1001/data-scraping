import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin


def scrape_page(url, writer):
    try:
        response = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        if response.status_code != 200:
            return False
    except requests.exceptions.RequestException:
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    base_url = url

    for book in books:
        title = book.h3.a["title"]

        relative_url = book.h3.a["href"]
        product_url = urljoin(base_url, relative_url)

        try:
            response2 = requests.get(
                product_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
            )
            if response2.status_code != 200:
                continue
        except requests.exceptions.RequestException:
            continue

        book_page = BeautifulSoup(response2.text, "html.parser")
        product_info = book_page.find_all("td")

        upc = product_info[0].get_text(strip=True)
        product_type = product_info[1].get_text(strip=True)
        price = float(
            product_info[3]
            .get_text(strip=True)
            .replace("£", "")
            .replace("Â", "")
        )
        availability = product_info[5].get_text(strip=True)

        writer.writerow(
            [title, product_url, upc, product_type, price, availability]
        )

        time.sleep(0.5)

    return True


with open("adv3.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        ["Title", "Link", "UPC", "Product Type", "Price (incl. tax)", "Availability"]
    )

    page = 1
    url = "https://books.toscrape.com/"

    while True:
        success = scrape_page(url, writer)
        if not success:
            break

        print(f"--- Page {page} scraped ---")
        page += 1

        try:
            response = requests.get(
                url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
            )
            if response.status_code != 200:
                break
        except requests.exceptions.RequestException:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        next_tag = soup.find("li", class_="next")

        if next_tag:
            next_url = next_tag.a["href"]
            url = urljoin(url, next_url)
        else:
            break


        
        

