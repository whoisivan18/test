# Telegram TON Converter Bot

This repository contains a simple Telegram bot to convert between TON cryptocurrency and Russian rubles using CoinGecko exchange rates.

## Usage

1. Install dependencies:

```bash
pip install pyTelegramBotAPI requests
```

2. Set the `TELEGRAM_BOT_TOKEN` environment variable to your bot token.

3. Run the bot:

```bash
python ton_converter_bot.py
```

The bot understands the following commands:

- `/ton2rub <amount>` – converts the given TON amount to rubles.
- `/rub2ton <amount>` – converts the given amount of rubles to TON.


