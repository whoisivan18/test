import re
from typing import Optional, Tuple

NUMBER_RE = re.compile(r'(?P<amount>[\d,.]+)\s*(?P<currency>[a-zA-Zа-яА-Я₽]*)')

TON_ALIASES = {'ton', 'toncoin', 'тон', 'тонкоин'}
RUB_ALIASES = {'rub', 'ruble', 'руб', '₽'}


def parse_amount(message: str) -> Optional[Tuple[float, str]]:
    match = NUMBER_RE.search(message.strip())
    if not match:
        return None
    amount_str = match.group('amount').replace(',', '.').strip()
    try:
        amount = float(amount_str)
        if amount < 0:
            return None
    except ValueError:
        return None
    currency = match.group('currency').lower()
    return amount, currency


def detect_direction(currency: str, default: str) -> Tuple[str, str]:
    if currency in TON_ALIASES or currency == 'ton':
        return 'TON', 'RUB'
    if currency in RUB_ALIASES:
        return 'RUB', 'TON'
    if default == 'rub_to_ton':
        return 'RUB', 'TON'
    return 'TON', 'RUB'


def convert(amount: float, from_currency: str, price_rub: float) -> float:
    if from_currency == 'TON':
        return amount * price_rub
    else:
        return amount / price_rub
