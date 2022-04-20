from bs4 import BeautifulSoup
import requests
import json
from html import unescape

root = "https://kbdfans.com"
switchesPage = "/collections/switches"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Accept-Language": "en-US"
}

response = requests.get(f"{root}{switchesPage}", headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Gets the total page count and grabs their links
pages = soup.find_all(name="span", class_="page")
pageLinks = [switchesPage]
for page in pages[1:]:
    link = page.find("a", href=True)['href']
    pageLinks.append(link)
print("Pages grabbed")

switchesProducts = {}  # data to be transferred to json
productNo = 0  # basically the iteration

# Goes through each page
for page in pageLinks:
    # Switches to page number
    response = requests.get(f"{root}{page}")
    soup = BeautifulSoup(response.text, "html.parser")
    print("Page number reached")

    # Finds and grabs links for all products on page
    products = soup.find_all(name="div", class_="product-block")
    links = []
    for product in products:
        divLink = product.find_next(name="div", class_="product-block__title")
        link = divLink.find("a", href=True)['href']
        links.append(link)
    print("Product links grabbed")

    for link in links:
        # Switches to product page
        response = requests.get(f"{root}{link}")
        soup = BeautifulSoup(response.text, "html.parser")
        # Scrapes product data
        productTitle = soup.find(name="h1", class_="product-detail__title").text
        productPrice = soup.find(name="span", class_="theme-money").text
        divSpecs = soup.find(name="div", id="tab1")
        specs = divSpecs.find_next(name="ul").find_all("li")
        productSpecs = [unescape(spec.text).replace(u'\xa0', ' ').replace('\n', '') for spec in specs]

        # Store into dictionary
        switchesProducts[productNo] = {
            "link": f"{root}{link}",
            "name": productTitle,
            "price": productPrice,
            "specs": productSpecs,
        }
        productNo += 1
        print("Product specs stored")
    print("All product specs stored for this page number")
print("All data scraped")
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(switchesProducts, f, ensure_ascii=False, indent=4)
print("Data written to JSON")
