import os
import requests
import telebot

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable not set")

bot = telebot.TeleBot(BOT_TOKEN)

API_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_ton_price_rub() -> float:
    """Fetch TON price in RUB from CoinGecko."""
    params = {"ids": "the-open-network", "vs_currencies": "rub"}
    resp = requests.get(API_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["the-open-network"]["rub"]


def convert_ton_to_rub(amount: float) -> float:
    return amount * get_ton_price_rub()


def convert_rub_to_ton(amount: float) -> float:
    price = get_ton_price_rub()
    return amount / price if price else 0


def parse_amount(text: str) -> float:
    try:
        return float(text.replace(',', '.'))
    except ValueError:
        return 0.0


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.reply_to(
        message,
        "Привет! Я конвертирую TON и рубли.\n"
        "Используй /ton2rub <количество> или /rub2ton <количество>."
    )


@bot.message_handler(commands=['ton2rub'])
def handle_ton2rub(message: telebot.types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Введите количество TON после команды.")
        return
    amount = parse_amount(parts[1])
    if amount <= 0:
        bot.reply_to(message, "Некорректное количество TON.")
        return
    result = convert_ton_to_rub(amount)
    bot.reply_to(message, f"{amount} TON ≈ {result:.2f} RUB")


@bot.message_handler(commands=['rub2ton'])
def handle_rub2ton(message: telebot.types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Введите количество рублей после команды.")
        return
    amount = parse_amount(parts[1])
    if amount <= 0:
        bot.reply_to(message, "Некорректное количество рублей.")
        return
    result = convert_rub_to_ton(amount)
    bot.reply_to(message, f"{amount} RUB ≈ {result:.4f} TON")


if __name__ == '__main__':
    print('Bot is polling...')
    bot.infinity_polling()
