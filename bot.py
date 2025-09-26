from datetime import datetime
from pytz import timezone
from config import cfg
from ph_client import fetch_candidates
from filters import is_fintech, score
from composer import compose_message
from tg_client import send_message
from storage import ensure_db, was_posted, mark_posted

def should_post_now() -> bool:
    tz = timezone(cfg.TIMEZONE)
    now = datetime.now(tz)
    return now.hour == cfg.POST_AT_HOUR_LOCAL

def run(force: bool = True):
    ensure_db()
    if not force and not should_post_now():
        return

    posts = fetch_candidates(40)
    shortlist = [p for p in posts if is_fintech(p) and not was_posted(p["id"])]
    if not shortlist:
        send_message("⚠️ Сегодня нет свежих финтех-кандидатов на Product Hunt.")
        return

    winner = sorted(shortlist, key=score, reverse=True)[0]
    text = compose_message(winner)
    send_message(text)
    mark_posted(winner["id"])

if __name__ == "__main__":
    run(force=True)