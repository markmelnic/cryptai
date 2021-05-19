from dotenv import load_dotenv
load_dotenv()

from cmc import CMC, BASE_URL

cmc = CMC()

cmc.fetch_coin("/currencies/consentium/")
