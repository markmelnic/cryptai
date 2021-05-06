from time import sleep
from dotenv import load_dotenv
load_dotenv()

from cmc import CMC
from telegram import Bot

cmc = CMC(load_db=True)
bot = Bot()

while True:
    new_coins = cmc.check_new()
    if new_coins:
        pass # send telegram message

    sleep(3600)
