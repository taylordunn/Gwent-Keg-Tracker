import requests
from bs4 import BeautifulSoup




page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.htlm")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
