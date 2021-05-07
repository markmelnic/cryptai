from time import sleep
from dotenv import load_dotenv
load_dotenv()

from cmc import CMC, BASE_URL
from telegram import Bot

INTERVAL = 3600

cmc = CMC(load_db=True)
bot = Bot()

while True:
    new_coins = cmc.check_new(add=True)
    if new_coins:
        if len(new_coins) == 1:
            pass
            bot.send_message("❗ A new coin just hit the market	❗")
        else:
            pass
            bot.send_message("❗ New coins just hit the market ❗")

        for c in new_coins:
            details = cmc.fetch_coin(c.link)

            bot.send_message(
                f"{c.name} - {c.symbol}"
                f"\n{BASE_URL[:-1] + c.link}\n"
                f"\nPrice: {details['price']}"
                f"\nVolume (24h): {details['volume']}"
                # f"\nCMC Rank: {details['cnc_rank']}"
            )

    sleep(INTERVAL)
