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


def main():
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
