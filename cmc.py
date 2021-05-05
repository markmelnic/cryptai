from db import *

from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://coinmarketcap.com/"

class CMC:
    def __init__(self) -> None:
        self.coins = []

    def __repr__(self) -> str:
        return f'Indexed {len(self.coins)} coins'

    def __str__(self) -> str:
        return f'Indexed {len(self.coins)} coins'

    def index_coins(self, db: Session = get_db()):
        r = BeautifulSoup(get(BASE_URL).content, "html.parser")
        pages = r.find(class_="pagination").find_all("li")[-2].get_text()
        for i in range(1, int(pages) + 1):
            print(f"Indexing page {i}")
            r = get(BASE_URL + "?page=" + str(i))
            soup = BeautifulSoup(r.content, "html.parser")
            trows = soup.find(name="tbody").find_all("tr", recursive=False)
            for c in self._scrape_page(trows):
                self.coins.append(c)

                coin = CoinModel(
                    link=c.link,
                    name=c.name,
                    symbol=c.symbol
                )
                db.add(coin)
        db.commit()

    def _scrape_page(self, trows):
        for tr in trows:
            coin = tr.find(class_="cmc-link")
            details = coin.find_all("div")
            if len(details) == 0:
                details = coin.find_all("span")
                _, name, symbol = details
                name = name.get_text()
                symbol = symbol.get_text()
            else:
                _logo, name, symbol, rank = details
                rank = rank.get_text()
                symbol = symbol.get_text()[len(rank):]
                name = name.get_text()[:-len(symbol)-len(rank)]

            yield Coin(link=coin['href'],
                    symbol=symbol,
                    name=name)


class Coin:
    def __init__(self, **kw) -> None:
        self.link = kw['link']
        self.name = kw['name']
        self.symbol = kw['symbol']

        self.dict = {
            'link': self.link,
            'name': self.name,
            'symbol': self.symbol,
        }

    def __repr__(self) -> str:
        return f'{self.symbol} - {self.name}'

    def __str__(self) -> str:
        return f'{self.symbol} - {self.name}'
