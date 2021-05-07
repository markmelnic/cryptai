from threading import Thread
from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

from telegram import Bot
from processes import *

bot = Bot()

logging.info('Starting threads')
threads = [
    Thread(target=new_coins_indexer, args = (bot, )),
]
for th in threads:
    th.start()
logging.info('All threads started successfully')

for th in threads:
    th.join()
