from threading import Thread
from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

from processes import *

logging.info('Starting threads')
threads = [
    Thread(target=new_coins_indexer, args = ()),
    Thread(target=daily_gl_indexer, args = ()),
]
for th in threads:
    th.daemon = True
    th.start()
logging.info('All threads started successfully')

input()
