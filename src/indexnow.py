"""Сообщить поисковикам (Яндекс, Bing через IndexNow) обо всех адресах из sitemap.xml.

Запускается GitHub Actions после каждого изменения sitemap.xml (.github/workflows/indexnow.yml).
Ключ лежит в корне сайта: 7150f194cd473a6d66b181e78564a3cd.txt
"""
import json
import re
import sys
import urllib.error
import urllib.request

HOST = "mralexod.github.io"
KEY = "7150f194cd473a6d66b181e78564a3cd"
KEY_URL = f"https://{HOST}/dengi-sverhu/{KEY}.txt"
ENDPOINTS = ["https://yandex.com/indexnow", "https://api.indexnow.org/indexnow"]


def main():
    urls = re.findall(r"<loc>(.*?)</loc>", open("sitemap.xml", encoding="utf-8").read())
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_URL, "urlList": urls}).encode()
    ok = True
    for ep in ENDPOINTS:
        req = urllib.request.Request(ep, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"{ep}: {r.status} — отправлено адресов: {len(urls)}")
        except urllib.error.HTTPError as e:
            print(f"{ep}: ошибка {e.code} {e.read()[:200]!r}")
            ok = ok and e.code in (200, 202)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
