import json
from cmc import CMC

if __name__ == '__main__':
    cmc = CMC()
    cmc.scrape()
    with open("coins.json", "w") as cfile:
        coins = {}
        print(len(cmc.coins))
        coins['coins'] = [c.dict for c in cmc.coins]
        json.dump(coins, cfile)
