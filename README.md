# TON \u21c4 RUB Telegram Bot

A simple Telegram bot for converting Toncoin to Russian Rubles and back.

## Quick Start

```bash
git clone <repo>
cd <repo>
export BOT_TOKEN=YOUR_TOKEN
docker-compose up --build
```

## Features
- Free-form conversion like `100 TON` or `2500 rub`.
- Commands: `/start`, `/help`, `/price`, `/convert`, `/setlang`.
- Live price ticker updated every 15 minutes.
- Basic rate limiting and multi-language replies (RU/EN).

## Tests

Run tests with:
```bash
pip install -r requirements.txt
pytest
```

