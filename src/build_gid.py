"""Гиды «Деньги сверху»: полезные страницы под разные аудитории и запросы, каждая ведёт на книгу.

Запуск (из корня репозитория):  python3 src/build_gid.py
Пишет gid/<slug>/index.html, оглавление gid/index.html и дописывает адреса в sitemap.xml.
Тексты — в src/gid_data_*.py (цифры только из книги). Новая партия = новый файл gid_data_N.py.
"""
import glob
import html
import importlib
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_v2 as v  # noqa: E402

SITE = v.SITE
ROOT = v.ROOT
PRICE = v.PRICE
CATS = ["Профессии", "Ситуации", "Как сделать", "Сколько стоит", "Чек-листы", "Понятия", "Инструменты"]

EXTRA_CSS = """
article h2{font-size:24px;line-height:1.25;margin:1.6em 0 .5em}
article ul,article ol{padding-left:1.3em;margin:0 0 1.1em}article li{margin:.25em 0}
.tw{overflow-x:auto;margin:0 0 1.2em}table{border-collapse:collapse;font-size:16px;width:100%}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}th{font-family:Montserrat,sans-serif;font-size:13px;letter-spacing:.04em}
.lead{font-size:20px;color:#e8dcc2;margin:0;padding-bottom:40px;max-width:640px}
.calc{border:1px solid var(--line);border-radius:12px;padding:18px;margin:0 0 1.4em;background:#fff;display:grid;gap:12px}
.calc label{display:grid;gap:6px;font:600 14px Montserrat,sans-serif}
.calc input{font:18px 'PT Serif',serif;padding:10px;border:1px solid var(--line);border-radius:8px;width:100%}
.calc-out{margin:0;font-size:18px}
.rel{margin:0 0 30px;font-size:16px}
.hub h2{font-size:22px;margin:1.8em 0 .6em}.hub ul{list-style:none;padding:0;display:grid;gap:10px}
.hub a{text-decoration:none;border-bottom:1px solid var(--gold)}.hub p{margin:.2em 0 0;font-size:15px;color:var(--soft)}
"""


def load():
    items = []
    here = os.path.dirname(os.path.abspath(__file__))
    for path in sorted(glob.glob(os.path.join(here, "gid_data_*.py"))):
        mod = importlib.import_module(os.path.basename(path)[:-3])
        for name in dir(mod):
            if re.fullmatch(r"G\d+", name):
                items.extend(getattr(mod, name))
    slugs = [i["slug"] for i in items]
    assert len(slugs) == len(set(slugs)), "повторяется slug"
    return items


def inline(s):
    s = html.escape(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def render(body, extra_html=""):
    out = []
    for block in re.split(r"\n\s*\n", body.strip()):
        lines = block.strip().split("\n")
        if lines[0] == "[[CALC]]":
            out.append(extra_html)
            continue
        if lines[0].startswith("## "):
            out.append(f"<h2>{inline(lines[0][3:])}</h2>")
            lines = lines[1:]
            if not lines:
                continue
        if all(l.startswith("|") for l in lines):
            rows = [[c.strip() for c in l.strip("|").split("|")] for l in lines if not re.fullmatch(r"\|[-| ]+\|", l)]
            th = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            tr = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tw"><table><tr>{th}</tr>{tr}</table></div>')
        elif all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"\d+\. ", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\d+\. ', '', l))}</li>" for l in lines) + "</ol>")
        else:
            out.append("<p>" + "<br>".join(inline(l) for l in lines) + "</p>")
    return "".join(out)


def cta(it):
    src = f"gid_{it['slug'][:40]}"
    more = ""
    if it.get("lz"):
        more = (f'<p class="rel">Эта тема подробно — в лазейке №{it["lz"]}: '
                f'<a href="{SITE}{v.code(it["lz"])}/">начало главы</a>.</p>')
    return (more + f'<div class="box"><h2>Откуда это</h2>'
            f'<p>Из книги «Деньги сверху. 38 лазеек к деньгам богатых для тех, кто начинает с нуля» (автор — Ключник): '
            f'истории, цифры чека, где брать первых клиентов, граница закона и план на 30 дней.</p>'
            f'<a class="btn gold" href="{SITE}?from={src}">Читать введение бесплатно</a>'
            f'<p style="margin:16px 0 0;font-size:14px">Полная книга {PRICE}, PDF на почту сразу · '
            f'<a href="{v.lava(src)}" target="_blank" rel="noopener">купить</a></p></div>')


def page(it):
    url = f"{SITE}gid/{it['slug']}/"
    title = f"{it['title']} | «Деньги сверху»"
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": it["title"],
                     "description": it["desc"], "inLanguage": "ru", "url": url,
                     "datePublished": str(date.today()),
                     "author": {"@type": "Person", "name": "Ключник"},
                     "isPartOf": {"@type": "Book", "name": "Деньги сверху", "author": {"@type": "Person", "name": "Ключник"},
                                  "url": SITE}}, ensure_ascii=False)
    nav = (f'<div class="nav"><a href="{SITE}">Деньги сверху · Ключник</a>'
           f'<a href="{SITE}gid/">Все гиды</a></div>')
    return (v.HEAD.format(title=html.escape(title), desc=html.escape(it["desc"]), url=url, site=SITE, ld=ld,
                          css=v.CSS + EXTRA_CSS)
            + f'<div class="top"><div class="w">{nav}<p class="k">{html.escape(it["cat"])} · гид</p>'
            f'<h1>{html.escape(it["title"])}</h1><p class="lead">{html.escape(it["desc"])}</p></div></div>'
            f'<div class="w"><article>{render(it["body"], it.get("html", ""))}</article>{cta(it)}</div>' + v.foot())


def hub(items):
    url = f"{SITE}gid/"
    title = "Гиды: как зарабатывать на обслуживании состоятельных клиентов | «Деньги сверху»"
    desc = (f"{len(items)} практических гидов для разных профессий и жизненных ситуаций: цены рынка, "
            "чек-листы, калькулятор и как начать без вложений. По книге Ключника «Деньги сверху».")
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Гиды «Деньги сверху»",
                     "url": url, "inLanguage": "ru"}, ensure_ascii=False)
    parts = []
    for cat in CATS:
        group = [i for i in items if i["cat"] == cat]
        if not group:
            continue
        lis = "".join(f'<li><a href="{SITE}gid/{i["slug"]}/">{html.escape(i["title"])}</a>'
                      f'<p>{html.escape(i["desc"])}</p></li>' for i in group)
        parts.append(f"<h2>{cat}</h2><ul>{lis}</ul>")
    return (v.HEAD.format(title=html.escape(title), desc=html.escape(desc), url=url, site=SITE, ld=ld,
                          css=v.CSS + EXTRA_CSS)
            + f'<div class="top"><div class="w">{v.nav()}<p class="k">Гиды · «Деньги сверху»</p>'
            f'<h1>Гиды для тех, кто хочет зарабатывать больше</h1>'
            f'<p class="lead">{html.escape(desc)}</p></div></div>'
            f'<div class="w"><article class="hub">{"".join(parts)}</article>'
            f'{cta({"slug": "hub", "lz": None})}</div>' + v.foot())


def main():
    items = load()
    for it in items:
        v.write(os.path.join(ROOT, "gid", it["slug"], "index.html"), page(it))
    v.write(os.path.join(ROOT, "gid", "index.html"), hub(items))
    urls = [f"{SITE}gid/"] + [f"{SITE}gid/{i['slug']}/" for i in items]
    v.write(os.path.join(ROOT, "gid", "urls.txt"), "\n".join(urls) + "\n")
    sm = os.path.join(ROOT, "sitemap.xml")
    text = open(sm, encoding="utf-8").read()
    known = set(re.findall(r"<loc>(.*?)</loc>", text))
    add = "".join(f"  <url><loc>{u}</loc><lastmod>{date.today()}</lastmod></url>\n" for u in urls if u not in known)
    v.write(sm, text.replace("</urlset>", add + "</urlset>"))
    print(f"гидов: {len(items)}, новых адресов в sitemap: {add.count('<url>')}")


if __name__ == "__main__":
    main()
