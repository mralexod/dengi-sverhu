"""Версия 2 сайта «Деньги сверху»: кнопка покупки (Lava.top) + страницы 38 лазеек для поиска.

Старая версия (корень сайта, index.html) не меняется. Всё новое — в папке v2/.
Запуск (из корня репозитория):
  BOOK_DIR=<папка книга-v2> python3 src/build_v2.py
"""
import html
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as b  # noqa: E402

ROOT = b.ROOT
SITE = b.SITE_URL
V2 = SITE + "v2/"
LAVA = "https://app.lava.top/products/ab0b1254-8001-4e73-a939-efcdeb64f8ac"
PRICE = "1 390 ₽"
BOOK_DIR = os.environ.get("BOOK_DIR", "")
PDF_V2 = "assets/dengi-sverhu-fragment-v2.pdf"

CART = ('<svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="10" cy="20" r="1.3"/><circle cx="17" cy="20" r="1.3"/></svg>')


def lava(src):
    return f"{LAVA}?utm_source={src}&utm_medium=site_v2"


# ---------- главная v2: та же страница, но кнопка «Купить» вместо «в Telegram» ----------
def buy(v="ghost", label=f"Купить книгу · {PRICE}", src="v2_main"):
    v = {"ghost": "gold", "navy": "navy"}.get(v, v)
    return f'<a href="{lava(src)}" target="_blank" rel="noopener" class="{b.BTN} {b.VAR[v]}">{CART}{label}</a>'


SRC_SNIP = '<script>/* метка источника из ссылки (?utm_source= или ?from=) переходит в кнопки покупки */(function(){try{var p=new URLSearchParams(location.search);var s=p.get(\'utm_source\')||p.get(\'from\');if(!s)return;s=s.replace(/[^A-Za-z0-9_-]/g,\'\').slice(0,40);if(!s)return;document.querySelectorAll(\'a[href*="app.lava.top"]\').forEach(function(a){a.href=a.href.replace(/utm_source=[^&]*/,\'utm_source=\'+s)})}catch(e){}})();</script>'


def main_page():
    if os.path.exists(os.path.join(ROOT, PDF_V2)):
        b.PDF = PDF_V2
    b.tg = buy
    b.dl.__defaults__ = ("ghost", "Бесплатный фрагмент")
    b.FAQ[0] = ("Где купить полную книгу?",
                f'На странице оплаты Lava.top: <a class="underline decoration-gold underline-offset-4" href="{lava("v2_faq")}" '
                f'target="_blank" rel="noopener">купить за {PRICE}</a>. Оплата картой, PDF и 3 приложения приходят на почту сразу. '
                'Новые лазейки — в канале <a class="underline decoration-gold underline-offset-4" href="https://t.me/dengisverhu" '
                'target="_blank" rel="noopener">t.me/dengisverhu</a>.')
    b.SITE_URL = V2
    h = b.page()
    b.SITE_URL = SITE
    h = h.replace(V2, SITE)
    h = h.replace("Полная книга со всеми приложениями — в Telegram-канале «Деньги сверху». Там же новые лазейки и ответы на вопросы.",
                  f"Книга и 3 приложения в PDF. Оплата картой на Lava.top — файлы приходят на почту сразу после оплаты. Цена запуска: <b>{PRICE}</b>.")
    h = h.replace("Скачать и купить полную книгу", "Купить полную книгу")
    h = h.replace("Перейти в канал t.me/dengisverhu", f"Купить за {PRICE}")
    h = h.replace("Фрагмент: PDF · 13 страниц · без регистрации", f"Фрагмент бесплатно · полная книга {PRICE}, PDF на почту сразу")
    # шапка: ссылка на 38 лазеек
    h = re.sub(r'<a href="https://t\.me/dengisverhu"([^>]*)>(<svg.*?</svg>)Полная книга</a>',
               lambda m: f'<a href="{lava("v2_header")}"{m.group(1)}>{CART.replace("h-5 w-5", "h-4 w-4")}Купить · {PRICE}</a>', h, count=1, flags=re.S)
    h = h.replace("</body>", SRC_SNIP + "</body>", 1)  # метка источника из ссылки → в кнопки покупки
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(h)


# ---------- 38 страниц лазеек ----------
ICONS = {"⏱": "время", "🔑": "доступ", "🛡": "безопасность", "❤️": "здоровье", "👑": "статус",
         "🆓": "с нуля, без денег", "🧠": "нужен навык или партнёр", "💸": "нужны деньги",
         "⚡": "1–4 недели", "🕐": "1–3 месяца", "🐢": "3+ месяца",
         "🟩": "свободно", "🟨": "есть, но можно выделиться", "🟥": "переполнено",
         "🟢": "белая", "🟡": "серая, есть правила", "🔴": "не лезть"}


def words(s):
    for k, v in ICONS.items():
        s = s.replace(k, f" {v}, ")
    return re.sub(r"\s*,\s*(\)|$)", r"\1", re.sub(r"\s+", " ", s)).strip(" ,")


def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[(.+?)\]\([^)]*\)", r"\1", s)
    return re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<em>\1</em>", s)


def slug(n, title):
    tr = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                  ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f",
                   "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya"]))
    t = "".join(tr.get(c, c) for c in title.lower())
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return f"{n:02d}-{t[:60].rstrip('-')}"


def parse():
    items = []
    for fn in sorted(os.listdir(BOOK_DIR)):
        if not re.match(r"0[789]-", fn):
            continue
        text = open(os.path.join(BOOK_DIR, fn), encoding="utf-8").read()
        for part in re.split(r"\n(?=### Лазейка \d+\.)", text)[1:]:
            lines = part.strip().split("\n")
            m = re.match(r"### Лазейка (\d+)\. (.+)", lines[0])
            n, title = int(m.group(1)), m.group(2).strip()
            meta = {}
            for kv in re.findall(r"\*\*([^*]+):\*\*\s*([^·]+)", lines[1] if len(lines) > 1 else ""):
                meta[kv[0].strip()] = kv[1].strip()
            body = "\n".join(lines[2:]).split("\n---")[0]
            paras = [p.strip() for p in re.split(r"\n\s*\n", body)
                     if p.strip() and not p.strip().startswith(("#", "|", "---"))]
            items.append({"n": n, "title": title, "meta": meta, "paras": paras, "slug": slug(n, title)})
    return sorted(items, key=lambda x: x["n"])


CSS = """
:root{--navy:#0f1a24;--deep:#080e14;--gold:#b08a3e;--gold-l:#d9bd85;--cream:#fbf8f2;--ink:#1f1c19;--soft:#625b53;--line:#e4dccd}
*{box-sizing:border-box;min-width:0}html,body{overflow-x:hidden}body{margin:0;overflow-wrap:break-word;background:var(--cream);color:var(--ink);font:18px/1.7 'PT Serif',Georgia,serif}
a{color:inherit}h1,h2,.d{font-family:Montserrat,system-ui,sans-serif}
.top{background:radial-gradient(120% 80% at 50% 0%,#1b2a38 0%,var(--navy) 55%,var(--deep) 100%);color:#f2ead9}
.w{max-width:760px;margin:0 auto;padding:0 20px}
.nav{display:flex;justify-content:space-between;gap:12px;padding:22px 0;font:600 12px Montserrat,sans-serif;letter-spacing:.2em;text-transform:uppercase}
.nav a{color:var(--gold-l);text-decoration:none}
.k{font:600 12px Montserrat,sans-serif;letter-spacing:.25em;text-transform:uppercase;color:var(--gold-l);margin:28px 0 0}
h1{font-size:clamp(30px,6vw,46px);line-height:1.1;margin:12px 0 18px;font-weight:800}
.meta{display:flex;flex-wrap:wrap;gap:8px;padding-bottom:40px}
.meta span{max-width:100%;border:1px solid rgba(176,138,62,.5);border-radius:999px;padding:5px 14px;font:600 13px Montserrat,sans-serif;color:#e8dcc2}
.meta b{color:var(--gold-l);font-weight:700}
article{padding:44px 0 10px}article p{margin:0 0 1.1em}
.fade{position:relative;max-height:9.5em;overflow:hidden}.fade:after{content:"";position:absolute;inset:auto 0 0 0;height:7em;background:linear-gradient(transparent,var(--cream))}
.box{margin:10px 0 40px;border:1px solid rgba(176,138,62,.6);background:#f6ecd8;border-radius:18px;padding:30px;text-align:center}
.box h2{margin:0 0 10px;font-size:24px;color:var(--navy)}.box p{margin:0 0 20px;color:var(--soft)}
.btn{display:inline-flex;max-width:100%;justify-content:center;align-items:center;gap:10px;border-radius:999px;padding:15px 28px;font:700 14px Montserrat,sans-serif;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;margin:5px}
.gold{background:var(--gold);color:var(--navy)}.navy{background:var(--navy);color:#f2ead9}.ghost{border:1px solid var(--gold);color:var(--navy)}
.list{columns:2;column-gap:28px;padding:0;list-style:none;font-size:16px}.list li{break-inside:avoid;margin:0 0 10px}
.list a{text-decoration:none;border-bottom:1px solid var(--line)}.list a:hover{border-color:var(--gold)}
.cliff{font-style:italic;color:var(--navy);border-left:3px solid var(--gold);padding-left:14px;margin:18px 0 0}.toc-h{font-size:20px;color:var(--navy);margin:34px 0 10px}.toc{list-style:none;padding:0;margin:0 0 10px}.toc li{padding:10px 0;border-bottom:1px solid var(--line);color:var(--soft)}
.pn{display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px;font:600 14px Montserrat,sans-serif;padding:10px 0 40px}.pn a{color:var(--gold);text-decoration:none}
footer{background:var(--deep);color:#b9ad97;text-align:center;font:12px Montserrat,sans-serif;padding:26px 20px}footer a{color:var(--gold-l)}
@media(max-width:640px){.list{columns:1}body{font-size:17px}}
"""

HEAD = """<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{site}assets/cover.png"><meta property="og:type" content="article"><meta name="theme-color" content="#0f1a24">
<link rel="icon" type="image/png" href="{site}assets/cover.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=PT+Serif:wght@400;700&display=swap">
<script type="application/ld+json">{ld}</script><style>{css}</style></head><body>"""


import hashlib

SALT = "klyuchnik-2026"
STOP_OPENERS = {"и последнее.", "это не шутка.", "почему так?", "почему ключ?", "а теперь главное.", "и самое интересное."}
REDIRECT = """<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow">
<link rel="canonical" href="{to}"><meta http-equiv="refresh" content="0; url={to}"><title>Деньги сверху</title></head>
<body><a href="{to}">Деньги сверху · Ключник</a></body></html>"""


def code(n):
    """Случайный на вид, но постоянный адрес страницы лазейки: по нему не угадать соседнюю."""
    h = int(hashlib.sha256(f"{SALT}:{n}".encode()).hexdigest(), 16)
    abc = "abcdefghijkmnpqrstuvwxyz23456789"
    out = ""
    for _ in range(14):
        h, r = divmod(h, len(abc))
        out += abc[r]
    return out


def sentences(p, k):
    parts = re.split(r"(?<=[.!?…])\s+", p)
    return " ".join(parts[:k])


QWORDS = ("как ", "где ", "почему ", "о чём ", "с чего ", "сколько ", "кто ", "что ", "чем ", "когда ", "зачем ")
STANDARD = ["Сколько здесь платят на самом деле — и в какой момент забирать свой процент",
            "Где найти первых клиентов: места, о которых не думают 9 из 10",
            "Как думает богатый в этот момент — и какие слова он хочет услышать",
            "О чём молчат: ошибка, на которой здесь обжигаются",
            "Что сделать в первые 7 дней, если начинаешь с нуля"]


def openers(paras):
    """Оглавление главы без ответов: 2–3 вопроса из главы + общие закрытые пункты."""
    res = []
    for p in paras[2:]:
        m = re.match(r"([^.?!:]{8,70}[.?!:])(\s|$)", re.sub(r"\*\*", "", p))
        if not m:
            continue
        t = m.group(1).strip().rstrip(".:")
        tl = t.lower()
        if tl.startswith(QWORDS) and len(t) >= 15 and "богатый" not in tl and "с чего" not in tl:
            res.append(t if t.endswith("?") else t)
    res = res[:3]
    return res + STANDARD[:7 - len(res)]


def cta(n):
    return (f'<div class="box"><h2>Чем это заканчивается — в книге</h2>'
            f'<p>Полная глава: как устроены деньги в этой нише, где первые клиенты, в какой момент брать процент и о чём молчат. '
            f'И ещё 37 таких лазеек — с историями, цифрами и планом на 30 дней.</p>'
            f'<a class="btn gold" href="{SITE}?from=lz{n}">Открыть книгу «Деньги сверху»</a>'
            f'<p style="margin:16px 0 0;font-size:14px">Введение — бесплатно · полная книга {PRICE}, PDF на почту сразу</p></div>')


def nav():
    return f'<div class="nav"><a href="{SITE}">Деньги сверху · Ключник</a><a href="{SITE}#full">Книга</a></div>'


def foot():
    return (f'<footer>Книга «Деньги сверху. 38 лазеек к деньгам богатых для тех, кто начинает с нуля», автор — Ключник · '
            f'<a href="{SITE}">mralexod.github.io/dengi-sverhu</a></footer></body></html>')


def lz_page(it):
    url = f"{SITE}{code(it['n'])}/"
    chek = it["meta"].get("Чек", "")
    title = f"{it['title']} — как заработать с нуля | Ключник, «Деньги сверху»"
    desc = (f"Как заработать на нише «{it['title']}» с нуля: чек {chek}, старт — {words(it['meta'].get('Старт', ''))}, "
            f"первые деньги — {words(it['meta'].get('Первые деньги', ''))}. Лазейка {it['n']} из 38 в книге Ключника «Деньги сверху».")[:300]
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": it["title"],
                     "author": {"@type": "Person", "name": "Ключник"}, "inLanguage": "ru", "url": url,
                     "isPartOf": {"@type": "Book", "name": "Деньги сверху", "author": {"@type": "Person", "name": "Ключник"},
                                  "url": SITE}}, ensure_ascii=False)
    labels = [("Чек", "Чек"), ("Старт", "Старт"), ("Первые деньги", "Первые деньги"), ("Конкуренция", "Конкуренция")]
    meta = "".join(f'<span><b>{lab}:</b> {html.escape(words(it["meta"][k]))}</span>' for k, lab in labels if k in it["meta"])
    p = it["paras"]
    hook = f"<p>{md_inline(p[0])}</p>"
    tail = f'<div class="fade"><p>{md_inline(sentences(p[1], 2))}</p></div>' if len(p) > 1 else ""
    tail += '<p class="cliff">Чем закончилась эта история и как в ней зарабатывают с нуля — в полной главе.</p>'
    toc = "".join(f'<li>🔒 {html.escape(t)}</li>' for t in openers(p))
    toc = f'<h2 class="toc-h">В полной главе</h2><ul class="toc">{toc}</ul>' if toc else ""
    return (HEAD.format(title=html.escape(title), desc=html.escape(desc), url=url, site=SITE, ld=ld, css=CSS)
            + f'<div class="top"><div class="w">{nav()}<p class="k">Одна из 38 лазеек · книга «Деньги сверху»</p>'
            f'<h1>{html.escape(it["title"])}</h1><div class="meta">{meta}</div></div></div>'
            f'<div class="w"><article>{hook}{tail}{toc}</article>{cta(it["n"])}</div>' + foot())


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    main_page()
    urls = [SITE]
    if BOOK_DIR:
        items = parse()
        assert len(items) == 38, f"нашлось лазеек: {len(items)}"
        for it in items:
            write(os.path.join(ROOT, code(it["n"]), "index.html"), lz_page(it))
            urls.append(f"{SITE}{code(it['n'])}/")
            # старые адреса /v2/lazeyki/... ведут на главную
            write(os.path.join(ROOT, "v2", "lazeyki", it["slug"], "index.html"), REDIRECT.format(to=SITE))
        write(os.path.join(ROOT, "v2", "lazeyki", "index.html"), REDIRECT.format(to=SITE))
        mp = "\n".join(f"{it['n']}\t{code(it['n'])}\t{it['title']}" for it in items)
        write(os.path.join(os.environ.get("MAP_DIR", "/tmp"), "lazeyki-adresa.tsv"), mp + "\n")
    write(os.path.join(ROOT, "v2", "index.html"), REDIRECT.format(to=SITE))
    gid = os.path.join(ROOT, "gid", "urls.txt")  # гиды (src/build_gid.py) не теряем при пересборке
    if os.path.exists(gid):
        urls += [u.strip() for u in open(gid, encoding="utf-8") if u.strip()]
    today = date.today()
    body = "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    write(os.path.join(ROOT, "sitemap.xml"), '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")
    print("готово, страниц в sitemap:", len(urls))


if __name__ == "__main__":
    main()
