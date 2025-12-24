import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(url, writer):
    response = requests.get(url)

    if response.status_code != 200:
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
        
        stock_tag = book.find("p", class_="instock availability")
        if stock_tag:
            stock = stock_tag.get_text(strip=True)
        else:
            stock = "Out of Stock"

        p_tag = book.find("p", class_="star-rating")
        rating = p_tag['class'][1]

        link = book.h3.a["href"]
        full_link = "https://books.toscrape.com/catalogue/" + link.replace("../", "")

        writer.writerow([title, price, stock, rating, full_link])
    return True

with open("mock2.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Availability", "Rating", "Link to Book"])

    #Page 1 (special case)
    scrape_page("https://books.toscrape.com/", writer)

    #Page 2 and onwards
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"

    for page in range(2, 55):
        url = base_url.format(page)
        success = scrape_page(url, writer)

        if not success:
            break

    print("Multiple pages scraped successfully")

