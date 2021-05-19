
import logging
from time import sleep
from telegram import Bot
from cmc import CMC, BASE_URL, BASE_GL

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
                message = cmc.fetch_coin(c.link)
                bot.send_message(
                    f"{c.name} - {c.symbol}"
                    f"\n{BASE_URL[:-1] + c.link}\n" +
                    message
                )
                logging.info(f'#{c.symbol} - {c.name}: Notification sent')
        logging.info(f'{len(new_coins)} new coins have been found. Waiting {INTERVAL} seconds')

        sleep(INTERVAL)

def daily_gl_indexer() -> None:
    bot = Bot()
    cmc = CMC(load_db=True)

    while True:
        logging.info(f'Started indexing daily gainers and losers')
        gl_type = True
        if gl_type:
            message = f"❗ Top gainers today ❗"
        else:
            message = f"❗ Top losers today ❗"
        gl_coins = cmc.index_gl(type=gl_type)
        message += f"\nBrowse all gainers and losers here:\n{BASE_GL}"

        for i, c in enumerate(gl_coins):
            if i == 3:
                break
            message += f"\n\n{i+1}. {c.symbol} - {c.name}\n{BASE_URL[:-1] + c.link}"

        bot.send_message(message)
        logging.info(f'GL process executed successfully. Waiting {INTERVAL*24} seconds')

        sleep(INTERVAL*24)
