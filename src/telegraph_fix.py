"""Правка зеркал гидов на Telegraph по 38-ФЗ: убрать цену и ссылку на оплату,
вместо них — ссылка на бесплатное введение на сайте. Токен — из секрета TELEGRAPH_TOKEN.
Запуск: DRY_RUN=1 python3 src/telegraph_fix.py  (показать правку первой страницы, ничего не менять)
"""
import json, os, re, sys, time, urllib.parse, urllib.request

API = "https://api.telegra.ph/"
TOKEN = os.environ.get("TELEGRAPH_TOKEN", "")
DRY = os.environ.get("DRY_RUN") == "1"
LIMIT = int(os.environ.get("LIMIT", "1000"))
SITE = "https://mralexod.github.io/dengi-sverhu/"


def call(method, **params):
    for _ in range(20):
        data = urllib.parse.urlencode({k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v)
                                       for k, v in params.items()}).encode()
        r = json.load(urllib.request.urlopen(API + method, data, timeout=60))
        if r.get("ok"):
            return r["result"]
        m = re.search(r"FLOOD_WAIT_(\d+)", str(r.get("error", "")))
        if not m:
            raise RuntimeError(f"{method}: {r}")
        print("лимит Telegraph, жду", m.group(1), "с", flush=True)
        time.sleep(int(m.group(1)) + 2)
    raise RuntimeError("слишком много FLOOD_WAIT")


def text_of(n):
    if isinstance(n, str):
        return n
    return "".join(text_of(c) for c in n.get("children", []))


def has_lava(n):
    if isinstance(n, str):
        return False
    if "lava.top" in (n.get("attrs") or {}).get("href", ""):
        return True
    return any(has_lava(c) for c in n.get("children", []))


def trim_sale(p):
    """Если в абзаце есть и ссылки на сайт, и хвост «Полная книга — 1 390 ₽ … купить», отрезать только хвост."""
    kids = p.get("children", [])
    if not any(isinstance(k, dict) and "dengi-sverhu" in (k.get("attrs") or {}).get("href", "") for k in kids):
        return False
    out = []
    for i, k in enumerate(kids):
        if isinstance(k, str):
            m = re.search(r"[.;]?\s*(Полная книга|Книга целиком|Купить|\d[\d ]* ₽)", k)
            if m:
                head = k[:m.start()].rstrip(" .,;:—")
                if head:
                    out.append(head)
                out.append(".")
                p["children"] = out
                return True
        elif "lava.top" in (k.get("attrs") or {}).get("href", ""):
            p["children"] = out + ["."]
            return True
        out.append(k)
    return False


def fix(nodes, slug):
    out, changed = [], False
    for n in nodes:
        if isinstance(n, dict) and n.get("tag") == "p" and has_lava(n) and trim_sale(n):
            changed = True
            out.append(n)
            continue
        if isinstance(n, dict) and (has_lava(n) or "1 390" in text_of(n)):
            if isinstance(n, dict) and n.get("tag") in ("p", "blockquote", "h4", "h3", "aside", "figure", "ul", "ol"):
                changed = True
                if not any("введение" in text_of(x).lower() and "бесплатно" in text_of(x).lower() for x in out):
                    out.append({"tag": "p", "children": [
                        "Введение и оглавление книги — бесплатно на сайте: ",
                        {"tag": "a", "attrs": {"href": f"{SITE}?utm_source=tgph_{slug[:40]}"}, "children": ["читать"]}]})
                continue
            kids, ch = fix(n.get("children", []), slug)
            n = dict(n, children=kids)
            changed |= ch
        out.append(n)
    return out, changed


def main():
    if not TOKEN:
        sys.exit("нет секрета TELEGRAPH_TOKEN")
    here = os.path.dirname(os.path.abspath(__file__))
    pages = [l.split() for l in open(os.path.join(here, "telegraph_pages.txt"), encoding="utf-8") if l.strip()]
    done = n = 0
    for slug, path in pages[:LIMIT]:
        p = call("getPage", path=path, return_content="true")
        content, changed = fix(p["content"], slug)
        rest = json.dumps(content, ensure_ascii=False)
        if "lava.top" in rest or "1 390" in rest:
            print("ВНИМАНИЕ: осталось упоминание оплаты", path)
        if not changed:
            print("без изменений", path, flush=True)
            continue
        if DRY:
            print("ДО:", json.dumps(p["content"], ensure_ascii=False)[-900:])
            print("ПОСЛЕ:", rest[-600:])
            return
        call("editPage", access_token=TOKEN, path=path, title=p["title"], content=content,
             author_name=p.get("author_name", "Ключник"), author_url=p.get("author_url", ""))
        done += 1
        print("ok", path, flush=True)
        time.sleep(3)
    print("ИТОГ: исправлено", done, "из", len(pages[:LIMIT]))


if __name__ == "__main__":
    main()
