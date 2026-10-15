"""Разведка для статей Дзена: подсказки Яндекса/Google (что ищут) + топ-10 выдачи (что пишут конкуренты).
Запуск: SEEDS="запрос 1|запрос 2" python3 src/seo_research.py  → seo/research-<дата>.json
Пока нет API Вордстата: подсказки показывают реальные формулировки запросов (без частотности).
"""
import datetime, html, json, os, re, time, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "ru-RU,ru;q=0.9"}


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def yandex_suggest(q):
    try:
        t = get("https://suggest.yandex.ru/suggest-ff.cgi?uil=ru&n=10&part=" + urllib.parse.quote(q))
        d = json.loads(t)
        return [x if isinstance(x, str) else x[1] for x in d[1]]
    except Exception as e:
        return [f"ошибка: {e}"]


def google_suggest(q):
    try:
        t = get("https://suggestqueries.google.com/complete/search?client=firefox&hl=ru&gl=ru&q=" + urllib.parse.quote(q))
        return json.loads(t)[1]
    except Exception as e:
        return [f"ошибка: {e}"]


def ddg_top(q, n=10):
    try:
        t = get("https://html.duckduckgo.com/html/?kl=ru-ru&q=" + urllib.parse.quote(q))
    except Exception as e:
        return [{"ошибка": str(e)}]
    out = []
    for m in re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', t, re.S):
        href = html.unescape(m.group(1))
        u = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("uddg", [href])[0]
        if "duckduckgo.com/y.js" in u:
            continue
        out.append({"url": u, "title": re.sub("<.*?>", "", html.unescape(m.group(2))).strip()})
        if len(out) >= n:
            break
    return out


def page_outline(url):
    try:
        t = get(url, timeout=15)
    except Exception as e:
        return {"ошибка": str(e)[:80]}
    body = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)
    hs = [re.sub(r"\s+", " ", re.sub("<.*?>", "", html.unescape(h))).strip()
          for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", body, re.S | re.I)]
    text = re.sub(r"\s+", " ", html.unescape(re.sub("<.*?>", " ", body)))
    return {"слов": len(text.split()), "подзаголовки": [h for h in hs if h][:25]}


def main():
    seeds = [s.strip() for s in os.environ.get("SEEDS", "").split("|") if s.strip()]
    res = []
    for q in seeds:
        item = {"запрос": q, "подсказки_яндекс": yandex_suggest(q), "подсказки_google": google_suggest(q),
                "хвосты": {}, "топ": []}
        for tail in ["как", "сколько", "где", "с нуля"]:
            item["хвосты"][tail] = yandex_suggest(f"{q} {tail}")[:6]
            time.sleep(0.5)
        for r in ddg_top(q):
            if "url" in r:
                r.update(page_outline(r["url"]))
            item["топ"].append(r)
            time.sleep(1)
        res.append(item)
        print("готово:", q, "| подсказок:", len(item["подсказки_яндекс"]), "| в топе:", len(item["топ"]), flush=True)
    os.makedirs("seo", exist_ok=True)
    path = f"seo/research-{datetime.date.today()}.json"
    json.dump(res, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("записано", path)


if __name__ == "__main__":
    main()
