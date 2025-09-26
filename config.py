from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

@dataclass(frozen=True)
class Config:
    TG_TOKEN: str
    TG_CHAT_ID: str
    PH_TOKEN: str
    POST_AT_HOUR_LOCAL: int
    TIMEZONE: str

def _need(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"❌ Missing env var: {key}")
    return value

cfg = Config(
    TG_TOKEN=_need("TELEGRAM_BOT_TOKEN"),
    TG_CHAT_ID=_need("TELEGRAM_CHAT_ID"),
    PH_TOKEN=_need("PRODUCTHUNT_TOKEN"),
    POST_AT_HOUR_LOCAL=int(os.getenv("POST_AT_HOUR_LOCAL", "9")),
    TIMEZONE=os.getenv("TIMEZONE", "America/Mexico_City"),
)