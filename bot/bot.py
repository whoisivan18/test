import asyncio
from collections import defaultdict

from aiogram import Bot, Dispatcher

from .config import load_config, Config
from .handlers import router
from .exchange import fetch_price
from .i18n import MESSAGES


price_messages: dict[int, int] = defaultdict(int)


async def price_ticker(bot: Bot, config: Config):
    while True:
        price_rub, price_usd = await fetch_price()
        text = MESSAGES[config.lang]['price'].format(price_rub=price_rub, price_usd=price_usd)
        for chat_id, msg_id in list(price_messages.items()):
            try:
                await bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id)
            except Exception:
                pass
        await asyncio.sleep(900)


async def on_startup(bot: Bot):
    asyncio.create_task(price_ticker(bot, config))


async def main():
    global config
    config = load_config()
    bot = Bot(config.bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(lambda _: asyncio.create_task(price_ticker(bot, config)))

    async with bot:
        await dp.start_polling(bot, config=config)


if __name__ == '__main__':
    asyncio.run(main())
