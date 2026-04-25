from database.insert import insert_products
from scraper.fetcher import fetch_page
from bs4 import BeautifulSoup
Base_url="https://books.toscrape.com/catalogue/page-{}.html"

def scrape_books():
    all_books=[]

    for page in range(1,6):
        url=Base_url.format(page)
        print(f"Scraping page {page}...")
        html=fetch_page(url)

        if not html:
            continue
        soup=BeautifulSoup(html, "html.parser")
        books=soup.select(".product_pod")

        for book in books:
            title=book.h3.a["title"]
            price_text = book.select_one(".price_color").text
            price_clean = price_text.encode('ascii', 'ignore').decode()
            price = float(price_clean.replace("£", ""))

            rating=book.p["class"][1]

            all_books.append({
                "title":title,
                "price": price
                ,
                "rating": rating
            })
    return all_books

if __name__=="__main__":
    data=scrape_books()

    insert_products(data)
    print(f"Total books Scraped: {len(data)}")

    for book in data[:10]:
        print(book)