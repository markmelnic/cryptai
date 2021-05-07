from db import *
from xpaths import *

from requests import get
from requests_html import HTMLSession
from bs4 import BeautifulSoup as BS

BASE_URL = "https://coinmarketcap.com/"
BASE_GL = "https://coinmarketcap.com/gainers-losers/"

class CMC:
    def __init__(self, load_db=True) -> None:
        self.ses = HTMLSession()
        self.coins = []

        if load_db:
            self.__load_db()
            if self.coins == []:
                self.index_coins(add=True)
                self.__load_db()
        else:
            self.coins = []

    def __repr__(self) -> str:
        return f'Indexed {len(self.coins)} coins'

    def __str__(self) -> str:
        return f'Indexed {len(self.coins)} coins'

    def index_coins(self, add=False) -> list:
        coins = []
        soup = BS(get(BASE_URL).content, "html.parser")
        pages = soup.find(class_="pagination").find_all("li")[-2].get_text()
        for i in range(1, int(pages) + 1):
            r = get(BASE_URL + "?page=" + str(i))
            soup = BS(r.content, "html.parser")
            trows = soup.find(name="tbody").find_all("tr", recursive=False)
            for c in self._scrape_page(trows):
                coins.append(c)

        if add:
            self._add_to_db(coins)

        return coins

    def get_gl(self, type: bool) -> list:
        soup = BS(get(BASE_GL).content, "html.parser")
        tables = soup.find_all(class_="cmc-table")

        if type:
            return self._scrape_gl(tables[0])
        else:
            return self._scrape_gl(tables[1])

    def check_new(self, add=False) -> list:
        db = get_db()
        new_coins = []
        for c in self.index_coins():
            if not db.query(Coin).filter(Coin.symbol == c.symbol).first():
                new_coins.append(c)

        if add:
            self._add_to_db(new_coins)

        return new_coins

    def fetch_coins(self, coins: list) -> list:
        return [self.fetch_coin(c.link) for c in coins]

    def fetch_coin(self, url: str) -> dict:
        r = self.ses.get(BASE_URL[:-1] + url)
        return {
            'price': r.html.xpath(Xpaths.CP.price)[0].text,
            'volume': r.html.xpath(Xpaths.CP.volume)[0].text,
            'cnc_rank': r.html.xpath(Xpaths.CP.cnc_rank)[0].text
        }

    def _scrape_gl(self, table: BS) -> list:
        gl_coins = []
        trows = table.find("tbody").find_all("tr", recursive=False)
        for c in self._scrape_page(trows):
            gl_coins.append(c)
        return gl_coins

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

            yield Coin(
                link=coin['href'],
                symbol=symbol,
                name=name)

    def _add_to_db(self, coins: list) -> None:
        db = get_db()
        for c in coins:
            db.add(c)
        db.commit()

    def __load_db(self) -> None:
        db = get_db()
        self.coins = db.query(Coin).all()
