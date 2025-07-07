import asyncio
from collections import defaultdict
from aiogram import Router, F
from aiogram.types import Message

from .exchange import fetch_price
from .utils import parse_amount, detect_direction, convert
from .i18n import MESSAGES
from .config import Config
from .bot import price_messages

router = Router()

user_requests: dict[int, list[float]] = defaultdict(list)

def check_rate_limit(user_id: int) -> bool:
    now = asyncio.get_event_loop().time()
    timestamps = user_requests[user_id]
    timestamps = [t for t in timestamps if now - t < 60]
    user_requests[user_id] = timestamps
    if len(timestamps) >= 10:
        return False
    timestamps.append(now)
    return True

async def send_price(message: Message, config: Config):
    price_rub, price_usd = await fetch_price()
    text = MESSAGES[config.lang]['price'].format(price_rub=price_rub, price_usd=price_usd)
    sent = await message.answer(text)
    price_messages[message.chat.id] = sent.message_id


@router.message(F.text.regexp(r'^/start'))
async def cmd_start(message: Message, config: Config):
    if not check_rate_limit(message.from_user.id):
        return
    await message.answer(MESSAGES[config.lang]['start'])


@router.message(F.text.regexp(r'^/help'))
async def cmd_help(message: Message, config: Config):
    if not check_rate_limit(message.from_user.id):
        return
    await message.answer(MESSAGES[config.lang]['help'])


@router.message(F.text.regexp(r'^/price'))
async def cmd_price(message: Message, config: Config):
    if not check_rate_limit(message.from_user.id):
        return
    await send_price(message, config)


@router.message(F.text.regexp(r'^/setlang'))
async def cmd_setlang(message: Message, config: Config):
    if not check_rate_limit(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) > 1 and parts[1] in ('ru', 'en'):
        config.lang = parts[1]
        await message.answer(MESSAGES[config.lang]['set_lang'].format(lang=config.lang))
    else:
        await message.answer('Usage: /setlang ru|en')


@router.message(F.text.regexp(r'^/convert'))
async def cmd_convert(message: Message, config: Config):
    if not check_rate_limit(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 4:
        await message.answer('Usage: /convert <amount> <from> <to>')
        return
    amount_str, from_cur, to_cur = parts[1], parts[2].lower(), parts[3].lower()
    parsed = parse_amount(f'{amount_str} {from_cur}')
    if not parsed:
        await message.answer(MESSAGES[config.lang]['unknown'])
        return
    amount, _ = parsed
    price_rub, _ = await fetch_price()
    if from_cur in ('rub', 'ruble', 'руб', '₽'):
        from_currency = 'RUB'
    else:
        from_currency = 'TON'
    result = convert(amount, from_currency, price_rub)
    await message.answer(f'{result:.4f} {to_cur.upper()}')


@router.message(F.text)
async def any_text(message: Message, config: Config):
    if not check_rate_limit(message.from_user.id):
        return
    parsed = parse_amount(message.text)
    if not parsed:
        await message.answer(MESSAGES[config.lang]['unknown'])
        return
    amount, currency = parsed
    from_cur, to_cur = detect_direction(currency, config.default_direction)
    price_rub, _ = await fetch_price()
    result = convert(amount, from_cur, price_rub)
    await message.answer(f'{result:.4f} {to_cur}')
