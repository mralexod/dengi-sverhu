"""Автопостинг в канал t.me/dengisverhu.

Берёт из posts.json самый ранний пост, у которого дата уже наступила (по Москве)
и номера которого ещё нет в sent.txt, и публикует его через Telegram Bot API.
За один запуск — не больше одного поста.

Переменные окружения:
  TG_BOT_TOKEN — токен бота-админа канала (секрет репозитория);
  TG_CHAT      — канал, по умолчанию @dengisverhu;
  DRY_RUN=1    — только показать, что ушло бы, ничего не отправлять.
"""
import datetime
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).parent
POSTS = HERE / "posts.json"
SENT = HERE / "sent.txt"


def today_msk():
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).date().isoformat()


def api(token, method, **params):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode() if params else None
    try:
        with urllib.request.urlopen(url, data=data, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}") or {"ok": False, "error_code": e.code}


def check():
    """Проверка бота: ничего не публикует, только спрашивает Telegram."""
    token = os.environ.get("TG_BOT_TOKEN", "").strip()
    if not token:
        print("❌ Секрет TG_BOT_TOKEN пустой или не найден.")
        sys.exit(1)
    me = api(token, "getMe")
    if not me.get("ok"):
        print("❌ Telegram не принял токен:", me.get("description"), "— токен неверный или перевыпущен.")
        sys.exit(1)
    bot = me["result"]
    print(f"✅ Токен рабочий: бот @{bot['username']} ({bot['first_name']})")
    chat = os.environ.get("TG_CHAT", "@dengisverhu")
    m = api(token, "getChatMember", chat_id=chat, user_id=bot["id"])
    if not m.get("ok"):
        print(f"❌ Бот не видит канал {chat}:", m.get("description"))
        sys.exit(1)
    r = m["result"]
    print(f"Статус в канале {chat}: {r['status']}")
    if r["status"] == "creator" or (r["status"] == "administrator" and r.get("can_post_messages")):
        print("✅ Бот может публиковать посты в канал.")
    else:
        print("❌ У бота нет права «Публикация сообщений» — включите его в настройках администратора канала.")
        sys.exit(1)


def main():
    if os.environ.get("CHECK") == "1":
        return check()
    posts = json.loads(POSTS.read_text(encoding="utf-8"))
    sent = {line.strip() for line in SENT.read_text().splitlines() if line.strip()}
    today = today_msk()
    due = [p for p in posts if p["date"] <= today and str(p["n"]) not in sent]
    if not due:
        print(f"{today}: публиковать нечего (отправлено {len(sent)} из {len(posts)})")
        return
    post = min(due, key=lambda p: (p["date"], p["n"]))
    print(f"{today}: пост {post['n']} «{post['title']}» (по плану {post['date']})")

    token = os.environ.get("TG_BOT_TOKEN", "").strip()
    if os.environ.get("DRY_RUN") == "1" or not token:
        print("Пробный запуск" + ("" if token else " (нет TG_BOT_TOKEN)") + " — не отправляю:\n")
        print(post["text"])
        return

    data = urllib.parse.urlencode({
        "chat_id": os.environ.get("TG_CHAT", "@dengisverhu"),
        "text": post["text"],
    }).encode()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        with urllib.request.urlopen(url, data=data, timeout=30) as r:
            answer = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("Telegram ответил ошибкой:", e.code, e.read().decode(errors="replace"))
        sys.exit(1)
    if not answer.get("ok"):
        print("Telegram не принял пост:", answer)
        sys.exit(1)
    with SENT.open("a") as f:
        f.write(f"{post['n']}\n")
    print("Опубликовано, message_id =", answer["result"]["message_id"])


if __name__ == "__main__":
    main()
