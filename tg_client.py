import requests
from typing import Optional
from config import cfg

def send_message(text: str, chat_id: Optional[str] = None) -> dict:
    url = f"https://api.telegram.org/bot{cfg.TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id or cfg.TG_CHAT_ID,
        "text": text,
        "disable_web_page_preview": False,
    }
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()
    return r.json()