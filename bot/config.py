import os
from dataclasses import dataclass

@dataclass
class Config:
    bot_token: str
    lang: str = os.getenv("LANG", "ru")
    default_direction: str = os.getenv("DEFAULT_DIRECTION", "ton_to_rub")


def load_config() -> Config:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")
    return Config(bot_token=token)
