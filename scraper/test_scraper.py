import requests
from bs4 import BeautifulSoup
Base_url="https://books.toscrape.com/catalogue/page-{}.html"
all_books=[]

for page in range(1,6):
    url=Base_url.format(page)
    response=requests.get(url)
    soup=BeautifulSoup(response.text, "html.parser")

    books=soup.select(".product_pod")

    print(books)
    for book in books:
        title=book.h3.a["title"]
        all_books.append(title)
print(f"Total books Scraped: {len(all_books)}")
for b in all_books[:10]:
    print(b)