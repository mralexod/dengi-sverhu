"""Счётчик Яндекс Метрики 113667184 (аккаунт «Ключник», 18.10) — во все HTML сайта перед </head>.
Вызывается в конце build_v2.py и build_gid.py; можно запустить и отдельно: python3 src/add_metrika.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SNIP = """<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=113667184', 'ym');ym(113667184, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/113667184" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->"""

def run():
    n = 0
    for f in ROOT.rglob("*.html"):
        if ".git" in f.parts:
            continue
        t = f.read_text(encoding="utf-8")
        if "mc.yandex.ru/metrika" in t or "</head>" not in t:
            continue
        f.write_text(t.replace("</head>", SNIP + "</head>", 1), encoding="utf-8")
        n += 1
    print("Метрика добавлена в страниц:", n)

if __name__ == "__main__":
    run()
