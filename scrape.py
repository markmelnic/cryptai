from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://coinmarketcap.com/?page="

for i in range(1, 50):
    r = get(BASE_URL + str(i))
    coins = BeautifulSoup(r.content, "html.parser").find(name="tbody")
    for tr in coins.find_all("tr", recursive=False):
        coin = tr.find(class_="cmc-link")
        link = coin['href']
        details = coin.find_all("div")
        if len(details) == 0:
            continue

        logo, name, symbol, rank = details
        rank = rank.get_text()
        symbol = symbol.get_text()[len(rank):]
        name = name.get_text()[:-len(symbol)-len(rank)]

        print(link, rank, name, symbol)
