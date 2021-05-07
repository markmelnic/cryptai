
import logging
from time import sleep
from telegram import Bot
from cmc import CMC, BASE_URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(message)s')

INTERVAL = 3600

def new_coins_indexer() -> None:
    bot = Bot()
    cmc = CMC(load_db=True)

    while True:
        logging.info(f'Started indexing new coins')
        new_coins = cmc.check_new(add=True)
        if new_coins:
            if len(new_coins) == 1:
                pass
                bot.send_message("❗ A new coin just hit the market	❗")
            else:
                pass
                bot.send_message("❗ New coins just hit the market ❗")

            for c in new_coins:
                logging.info(f'#{c.symbol} - {c.name}: Sending notification')
                details = cmc.fetch_coin(c.link)
                bot.send_message(
                    f"{c.name} - {c.symbol}"
                    f"\n{BASE_URL[:-1] + c.link}\n"
                    f"\nPrice: {details['price']}"
                    f"\nVolume (24h): {details['volume']}"
                    # f"\nCMC Rank: {details['cnc_rank']}"
                )
                logging.info(f'#{c.symbol} - {c.name}: Notification sent')
        logging.info(f'{len(new_coins)} new coins have been found. Waiting {INTERVAL} seconds')

        sleep(INTERVAL)
