import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

def scrape_page(url, writer):
    try:
        response = requests.get(
            url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10
            )
        if response.status_code != 200:
            return False
    except requests.exceptions.RequestException:
        return False
    
    soup = BeautifulSoup(response.text, "html.parser")
    laptops = soup.find_all("div", class_="product-wrapper card-body")

    for laptop in laptops:
        name_tag = laptop.find("a", class_="title")
        name = name_tag.get("title","") if name_tag else ""

        price_tag = laptop.find("h4", class_="price")
        price = price_tag.get_text(strip=True).replace("$","") if price_tag else ""

        description_tag = laptop.find("p", class_="description card-text")
        description = description_tag.get_text(strip=True) if description_tag else ""

        review_tag = laptop.find("span", itemprop="reviewCount")
        review = review_tag.get_text(strip=True) if review_tag else ""

        writer.writerow([name, price, description, review])
        time.sleep(0.3)
    return True

with open("adv4.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price($)", "Description", "Reviews"])

    page = 1
    url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=1"

    while True:
        success = scrape_page(url, writer)
        if not success:
            break

        print(f"---Page {page} scraped---")
        page += 1

        try:
            response = requests.get(
                url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10
            )
            if response.status_code != 200:
                break
        except requests.exceptions.RequestException:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        next_tag = soup.find("a", class_="page-link", rel="next")


        if next_tag:
            next_url = next_tag.get("href")
            url = urljoin(url, next_url)
        else:
            break