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
    print(f"{len(new_coins)} new coins found")
    if new_coins:
        print("Sending notifications...")
        if len(new_coins) == 1:
            bot.send_message("❗ A new coin just hit the market	❗")
        else:
            bot.send_message("❗ New coins just hit the market ❗")

        for c in new_coins:
            print(f"{c.name} sent")
            bot.send_message(
                f"""
                {c.name} - {c.symbol}
                {BASE_URL[:-1] + c.link}
                """
            )

        print(f"Success, waiting {INTERVAL} seconds")

    sleep(INTERVAL)
