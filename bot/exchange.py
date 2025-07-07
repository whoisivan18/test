import aiohttp
import time

API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=rub,usd'

_price_cache = {
    'timestamp': 0.0,
    'price_rub': 0.0,
    'price_usd': 0.0,
}

async def fetch_price() -> tuple[float, float]:
    now = time.time()
    if now - _price_cache['timestamp'] < 60:
        return _price_cache['price_rub'], _price_cache['price_usd']
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            data = await resp.json()
            price_rub = float(data['the-open-network']['rub'])
            price_usd = float(data['the-open-network']['usd'])
            _price_cache.update({
                'timestamp': now,
                'price_rub': price_rub,
                'price_usd': price_usd,
            })
            return price_rub, price_usd
