import os, requests

class Bot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        self.base = f"https://api.telegram.org/bot{self.token}/"

    def send_message(self, message: str):
        url = self.base + f"sendMessage?chat_id={self.chat_id}&text={message}"
        if message is not None:
            requests.get(url)
