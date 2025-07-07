MESSAGES = {
    'ru': {
        'start': (
            'Привет! Отправьте количество TON или RUB, и я выполню конвертацию.\n'
            'Примеры: "100 TON", "2500 руб", "42"'
        ),
        'help': 'Отправьте число и валюту (TON или RUB). По умолчанию TON->RUB.',
        'unknown': 'Не удалось разобрать сообщение. Пример: "100 TON" или "2500 руб".',
        'price': '1 TON = {price_rub:.2f} RUB (≈ {price_usd:.2f} USD)',
        'set_lang': 'Язык установлен на {lang}',
    },
    'en': {
        'start': (
            'Hi! Send an amount in TON or RUB and I will convert it.\n'
            'Examples: "100 TON", "2500 rub", "42"'
        ),
        'help': 'Send a number and currency (TON or RUB). Default TON->RUB.',
        'unknown': 'Could not parse message. Example: "100 TON" or "2500 rub".',
        'price': '1 TON = {price_rub:.2f} RUB (≈ {price_usd:.2f} USD)',
        'set_lang': 'Language set to {lang}',
    },
}
