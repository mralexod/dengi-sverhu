"""Собирает index.html сайта «Деньги сверху» для GitHub Pages.

Запуск (из папки github-pages):
  python3 src/build.py
  npx @tailwindcss/cli -i src/input.css -o assets/styles.css --minify
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = os.environ.get("SITE_URL", "https://mralexod.github.io/dengi-sverhu/")
TG = "https://t.me/dengisverhu"
PDF = "assets/dengi-sverhu-fragment.pdf"
COVER = "assets/cover.png"
TITLE = "Деньги сверху — 38 лазеек к деньгам богатых | Ключник"
DESC = ("Книга Ключника о том, за что на самом деле платят богатые и как зарабатывать на этом с нуля — "
        "без вложений, без связей, законно. Скачай бесплатный фрагмент.")

KEY = ('<svg viewBox="0 0 220 90" class="{c}" fill="none" stroke="currentColor" stroke-width="5" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="40" cy="45" r="28"/>'
       '<circle cx="40" cy="45" r="11"/><path d="M68 45 H205"/><path d="M180 45 V66 M196 45 V60 M164 45 V58"/></svg>')
TG_ICON = ('<svg viewBox="0 0 24 24" class="{c}" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3 18.8 19c-.2 1-.9 '
           '1.3-1.7.8l-4.7-3.5-2.3 2.2c-.3.3-.5.5-1 .5l.3-4.8 8.8-7.9c.4-.3-.1-.5-.6-.2L6.7 13l-4.6-1.4c-1-.3-1-1 .2-1.5L20.6 '
           '3c.8-.3 1.6.2 1.3 1.3Z"/></svg>')
DL_ICON = ('<svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
           '<path d="M12 3v12m0 0l-5-5m5 5l5-5M4 19h16" stroke-linecap="round" stroke-linejoin="round"/></svg>')

BTN = ("inline-flex items-center justify-center gap-3 rounded-full px-7 py-4 font-display text-sm font-bold uppercase "
       "tracking-[0.12em] shadow-lg transition")
VAR = {
    "gold": "bg-gold text-navy hover:bg-gold-light",
    "navy": "bg-navy text-on-navy hover:bg-navy-soft",
    "ghost": "border border-gold/60 text-gold-light hover:bg-navy-soft shadow-none",
}


def dl(v="gold", label="Скачать бесплатный фрагмент"):
    return (f'<a href="{PDF}" target="_blank" rel="noopener" download="Деньги-сверху-фрагмент.pdf" '
            f'class="{BTN} {VAR[v]}">{DL_ICON}{label}</a>')


def tg(v="ghost", label="Полная книга в Telegram"):
    return f'<a href="{TG}" target="_blank" rel="noopener" class="{BTN} {VAR[v]}">{TG_ICON.format(c="h-5 w-5")}{label}</a>'


def kicker(t, light=False):
    c = "text-gold-light" if light else "text-gold"
    return f'<p class="font-display text-xs font-semibold uppercase tracking-[0.3em] {c}">{t}</p>'


STOP = [
    ("«Богатые — это не мой уровень»", "Тебе не нужно знать миллиардера. Ты заходишь через тех, кто их уже обслуживает: прорабов, тренеров, нянь, детейлеров. В книге — 10 дверей к богатым без денег и связей."),
    ("«У меня нет стартового капитала»", "35 из 38 лазеек не требуют стартовых денег. Ты стоишь между тем, кто ищет, и тем, кто может дать, — и берёшь процент за результат."),
    ("«Это рискованно и серо»", "Отдельная глава — где граница: что законно, что серо и куда не лезть никогда. Ни одна лазейка не требует кредитов и залогов."),
    ("«Я не знаю, с чего начать»", "Тест из 5 вопросов покажет твой тип и твою лазейку. План на 30 дней — что делать каждый день до первой сделки."),
]
INSIDE = [
    "За что богатые платят без торга, за чем стоят в очереди и на что охотятся",
    "Кто они: Россия, Европа, США — где живут, как проводят год, где собираются",
    "38 лазеек — каждая с живой историей, цифрами и первыми шагами",
    "Тест: Сводник, Управляющий, Организатор, Цифровой мастер или Хранитель — и какая лазейка твоя",
    "10 дверей к богатым без денег и связей",
    "Готовые тексты первых сообщений исполнителям, клиентам и знакомым",
    "Где граница: что законно, что серо, куда не лезть никогда",
    "Красные океаны: какие бизнесы сейчас нельзя открывать",
    "Как за 15 минут проверить любую схему — в том числе мою",
    "Что будет расти у богатых до 2030 года",
]
FAQ = [
    ("Где скачать и купить полную книгу?", 'В Telegram-канале «Деньги сверху»: <a class="underline decoration-gold underline-offset-4" href="https://t.me/dengisverhu" target="_blank" rel="noopener">t.me/dengisverhu</a>. Там же — новые лазейки и ответы на вопросы.'),
    ("Это точно законно?", "Да. В книге есть отдельная глава о том, где проходит граница: что законно, что серо и куда не лезть никогда. Все лазейки — в белой зоне или с чёткими правилами, как сделать «бело»."),
    ("У меня нет денег на старт. Совсем.", "35 из 38 лазеек не требуют стартовых денег: ты ничего не покупаешь и ничего не производишь. Берёшь процент за результат."),
    ("Я не знаю ни одного богатого человека.", "И не нужно. Ты заходишь через исполнителей, которые их уже обслуживают. Глава 13 — 10 дверей к богатым без денег и связей."),
    ("Сколько времени нужно?", "Час-два в день. Первые деньги в быстрых лазейках — через 2–4 недели, в медленных — через 2–3 месяца. Честные сроки указаны у каждой лазейки."),
    ("Что в бесплатном фрагменте?", "Обложка, полное содержание, «Как читать эту книгу» и введение целиком: почему деньги теперь только сверху, математика «58 продаж против 2» и почему тебе не нужен выход на миллионера."),
]
TABLE = [("1 000 ₽", "200"), ("3 500 ₽", "58"), ("20 000 ₽", "10"), ("100 000 ₽", "2"), ("200 000 ₽", "1")]
STATS = [("38", "лазеек с цифрами и шагами"), ("447 000", "долларовых миллионеров в России"),
         ("35 из 38", "без стартовых денег"), ("30 дней", "пошаговый план")]
PILLARS = [("Оптика", "Шесть разрывов, в которых рождаются деньги. Научишься их видеть — найдёшь 39-ю лазейку сам."),
           ("38 лазеек", "Каждая — живая история, сколько платят, нужен ли капитал, когда придут первые деньги, тесно там или свободно."),
           ("Твой выбор и 30 дней", "Тест покажет, какая лазейка твоя. План — что делать каждый день до первой сделки.")]
FULL = [("Книга", "167 страниц: 38 лазеек, тест, граница, 10 дверей, план на 30 дней"),
        ("Шаблоны и скрипты", "12 готовых сообщений: копируй и отправляй"),
        ("Рабочая тетрадь", "Проходишь книгу — получаешь свой план"),
        ("Куда пойдут деньги до 2030", "14 трендов, на которые стоит ставить")]


def page():
    badges = "".join(f'<span class="rounded-full border border-gold/40 px-4 py-1.5 font-display text-xs font-semibold uppercase tracking-[0.15em] text-gold-light">{b}</span>'
                     for b in ["Без вложений", "Без связей", "Без опыта", "Законно"])
    stats = "".join(f'<div><div class="font-display text-3xl font-extrabold text-navy md:text-4xl">{n}</div><div class="mt-1 text-sm text-ink-soft">{t}</div></div>' for n, t in STATS)
    stop = "".join(f'<div class="rounded-xl border bg-card p-7 shadow-sm"><div class="font-display text-sm font-bold text-gold">0{i+1}</div><h3 class="mt-2 text-lg font-bold text-navy">{t}</h3><p class="mt-3 leading-relaxed text-ink-soft">{d}</p></div>' for i, (t, d) in enumerate(STOP))
    rows = "".join(f'<tr class="border-t border-gold/20"><td class="py-3 text-on-navy">{c}</td><td class="py-3 text-right text-2xl font-extrabold text-gold">{n}</td></tr>' for c, n in TABLE)
    pillars = "".join(f'<div class="rounded-xl bg-navy p-7 text-on-navy"><div class="font-display text-4xl font-extrabold text-gold">{i+1}</div><h3 class="mt-3 text-xl font-bold">{t}</h3><p class="mt-3 leading-relaxed text-on-navy-soft">{d}</p></div>' for i, (t, d) in enumerate(PILLARS))
    inside = "".join(f'<li class="flex gap-3 text-lg leading-snug">{KEY.format(c="mt-1.5 h-4 w-9 flex-none text-gold")}<span>{x}</span></li>' for x in INSIDE)
    full = "".join(f'<div class="rounded-xl border bg-card p-5"><div class="font-display font-bold text-navy">{t}</div><div class="mt-1 text-ink-soft">{d}</div></div>' for t, d in FULL)
    faq = "".join(f'<details class="group p-6"><summary class="flex cursor-pointer list-none items-center justify-between gap-4 font-display font-bold text-navy">{q}<span class="text-gold transition group-open:rotate-45">+</span></summary><p class="mt-3 leading-relaxed text-ink-soft">{a}</p></details>' for q, a in FAQ)

    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{SITE_URL}{COVER}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f1a24">
<link rel="icon" type="image/png" href="{COVER}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=PT+Serif:ital,wght@0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<div class="min-h-screen bg-cream text-ink">

<header class="hero-glow text-on-navy">
  <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-5 py-6">
    <span class="font-display text-xs font-bold uppercase tracking-[0.35em] text-gold">Ключник</span>
    <a href="{TG}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 font-display text-xs font-semibold uppercase tracking-[0.15em] text-on-navy-soft hover:text-gold-light">{TG_ICON.format(c="h-4 w-4")}Полная книга</a>
  </div>
  <div class="mx-auto grid max-w-6xl items-center gap-12 px-5 pb-20 pt-8 md:grid-cols-[1.25fr_1fr] md:pb-28 md:pt-14">
    <div>
      {kicker("Законные, но почти никем не замеченные", True)}
      <h1 class="mt-5 text-4xl font-extrabold leading-[1.05] text-on-navy md:text-6xl">38 лазеек к деньгам богатых</h1>
      <p class="mt-4 font-display text-lg font-semibold text-gold-light md:text-xl">для тех, кто начинает с нуля</p>
      <blockquote class="mt-8 border-l-2 border-gold pl-5 text-lg italic text-on-navy md:text-xl">«Пока все дерутся за копейки эконом-клиентов, наверху стоит очередь из богатых, которым некого нанять».</blockquote>
      <p class="mt-6 max-w-xl text-base leading-relaxed text-on-navy-soft md:text-lg">За 2025 год в России стало на 22 000 миллионеров больше. Их деньги растут, а хороших людей, которые умеют их обслуживать, не хватает. Эта книга покажет, где ты встанешь в эту очередь — с другой стороны прилавка.</p>
      <div class="mt-8 flex flex-wrap gap-2">{badges}</div>
      <div class="mt-10 flex flex-wrap gap-3">{dl()}{tg()}</div>
      <p class="mt-3 font-display text-xs text-on-navy-soft">Фрагмент: PDF · 13 страниц · без регистрации</p>
    </div>
    <div class="flex justify-center"><img src="{COVER}" alt="Обложка книги «Деньги сверху», автор Ключник" class="w-64 -rotate-2 rounded-md shadow-2xl ring-1 ring-gold/30 md:w-80"></div>
  </div>
</header>

<section class="border-b bg-paper"><div class="mx-auto grid max-w-6xl grid-cols-2 gap-6 px-5 py-10 text-center md:grid-cols-4">{stats}</div></section>

<section class="mx-auto max-w-6xl px-5 py-20">
  {kicker("Давай честно")}
  <h2 class="mt-3 max-w-3xl text-3xl font-extrabold leading-tight text-navy md:text-4xl">Ты сам знаешь, почему до сих пор не зарабатываешь больше</h2>
  <div class="mt-12 grid gap-6 md:grid-cols-2">{stop}</div>
</section>

<section class="hero-glow text-on-navy"><div class="mx-auto grid max-w-6xl gap-12 px-5 py-20 md:grid-cols-2">
  <div>
    {kicker("Где на самом деле лежат деньги", True)}
    <h2 class="mt-3 text-3xl font-extrabold leading-tight md:text-4xl">Деньги не исчезли. Они переехали наверх.</h2>
    <div class="mt-6 space-y-4 text-lg leading-relaxed text-on-navy-soft">
      <p>Ты живёшь в двух экономиках. Внизу люди считают каждую тысячу, ждут скидок и режут расходы. Наверху — строят второй дом, полгода ищут няню и летят на Камчатку ловить рыбу за полмиллиона в неделю.</p>
      <p>Экономисты называют это K-образной экономикой. Почти все начинают свой первый бизнес внизу — и бьются за 58 клиентов в месяц, каждый из которых торгуется за сотню.</p>
      <p class="text-on-navy">Наверху тебе нужен один-два. И они не торгуются.</p>
    </div>
  </div>
  <div class="self-center rounded-xl border border-gold/30 bg-navy-deep/60 p-6">
    <p class="font-display text-xs font-semibold uppercase tracking-[0.2em] text-gold-light">Чтобы заработать 200 000 ₽ в месяц</p>
    <table class="mt-4 w-full font-display text-sm"><thead><tr class="text-left text-on-navy-soft"><th class="pb-3 font-semibold">Твой чек</th><th class="pb-3 text-right font-semibold">Нужно продаж</th></tr></thead><tbody>{rows}</tbody></table>
    <p class="mt-4 text-sm italic text-on-navy-soft">Тот же труд. Те же часы. Разница — в том, кому ты продаёшь.</p>
  </div>
</div></section>

<section class="mx-auto max-w-6xl px-5 py-20">
  {kicker("Это не то, что тебе показывали раньше")}
  <h2 class="mt-3 max-w-3xl text-3xl font-extrabold leading-tight text-navy md:text-4xl">Здесь нет курсов про мышление, мотивации и «визуализации богатства»</h2>
  <div class="mt-12 grid gap-6 md:grid-cols-3">{pillars}</div>
</section>

<section class="border-y bg-paper"><div class="mx-auto max-w-6xl px-5 py-20">
  {kicker("Что внутри")}
  <h2 class="mt-3 text-3xl font-extrabold text-navy md:text-4xl">Что ты узнаешь</h2>
  <ul class="mt-10 grid gap-x-10 gap-y-4 md:grid-cols-2">{inside}</ul>
  <p class="mt-10 max-w-2xl border-l-2 border-gold pl-5 text-lg italic text-ink-soft">Развидеть это уже нельзя. После этой книги ты не сможешь смотреть на кофейню у метро, на очередь в салон и на объявление «ищу няню» по-старому.</p>
</div></section>

<section class="mx-auto grid max-w-6xl items-center gap-12 px-5 py-20 md:grid-cols-[auto_1fr]">
  <div class="mx-auto flex h-40 w-40 items-center justify-center rounded-full bg-navy text-gold shadow-xl">{KEY.format(c="h-16 w-32")}</div>
  <div>
    {kicker("Кто пишет")}
    <h2 class="mt-3 text-3xl font-extrabold text-navy md:text-4xl">Меня зовут Ключник. Это не имя, а род занятий.</h2>
    <div class="mt-6 space-y-4 text-lg leading-relaxed text-ink-soft">
      <p>Всю жизнь меня окружали двери, в которые не пускают всех. Однажды я понял: у каждой из них есть ключ, и он почти никогда не стоит денег. Он стоит понимания — кто за дверью, что ему нужно и чего ему не хватает.</p>
      <p>Я разбирал отчёты крупнейших банков мира, сравнивал Россию, Европу и Америку и собрал связку из 38 ключей. Эта книга — её дубликат.</p>
      <p class="text-ink">Я не показываю лицо. Дело не во мне, а в карте. Тебе нужно не моё лицо, а твои первые деньги.</p>
    </div>
  </div>
</section>

<section id="fragment" class="hero-glow text-on-navy"><div class="mx-auto grid max-w-6xl items-center gap-12 px-5 py-20 md:grid-cols-[1fr_auto]">
  <div>
    {kicker("Бесплатно", True)}
    <h2 class="mt-3 text-3xl font-extrabold leading-tight md:text-5xl">Начни читать прямо сейчас</h2>
    <p class="mt-6 max-w-2xl text-lg leading-relaxed text-on-navy-soft">Обложка, полное содержание, «Как читать эту книгу» и введение целиком. Почему деньги теперь только сверху, математика «58 продаж против 2» и почему тебе не нужен выход на миллионера. Без регистрации.</p>
    <div class="mt-8 flex flex-wrap gap-3">{dl()}{tg()}</div>
  </div>
  <img src="{COVER}" alt="" class="mx-auto w-48 rotate-3 rounded-md shadow-2xl ring-1 ring-gold/30">
</div></section>

<section id="full" class="mx-auto max-w-4xl px-5 py-20 text-center">
  {kicker("Полная версия")}
  <h2 class="mt-3 text-3xl font-extrabold text-navy md:text-4xl">«Деньги сверху» — книга и 3 приложения</h2>
  <div class="mt-10 grid gap-4 text-left sm:grid-cols-2">{full}</div>
  <div class="mt-10 rounded-2xl border border-gold/50 bg-gold-soft p-8">
    <p class="font-display text-sm font-bold uppercase tracking-[0.2em] text-navy">Скачать и купить полную книгу</p>
    <p class="mx-auto mt-3 max-w-xl text-lg text-ink-soft">Полная книга со всеми приложениями — в Telegram-канале «Деньги сверху». Там же новые лазейки и ответы на вопросы.</p>
    <div class="mt-6 flex flex-col items-center gap-3">
      {tg("navy", "Перейти в канал t.me/dengisverhu")}
      <a href="{PDF}" target="_blank" rel="noopener" class="font-display text-sm text-ink-soft underline decoration-gold underline-offset-4 hover:text-navy">или сначала скачать бесплатный фрагмент</a>
    </div>
  </div>
</section>

<section class="border-t bg-paper"><div class="mx-auto max-w-3xl px-5 py-20">
  {kicker("Коротко и без уверток")}
  <h2 class="mt-3 text-3xl font-extrabold text-navy md:text-4xl">Вопросы, которые ты уже задал себе</h2>
  <div class="mt-10 divide-y rounded-xl border bg-card">{faq}</div>
</div></section>

<section class="hero-glow text-center text-on-navy"><div class="mx-auto max-w-3xl px-5 py-20">
  {KEY.format(c="mx-auto h-10 w-24 text-gold")}
  <h2 class="mt-6 text-3xl font-extrabold leading-tight md:text-4xl">Ты дочитал до самого низа. Значит, ты уже смотришь наверх.</h2>
  <p class="mt-4 text-lg text-on-navy-soft">Осталось сделать первый шаг.</p>
  <div class="mt-8 flex flex-wrap justify-center gap-3">{dl()}{tg()}</div>
</div></section>

<footer class="bg-navy-deep py-8 text-center font-display text-xs text-on-navy-soft">© 2026 Ключник · «Деньги сверху» · <a href="{TG}" target="_blank" rel="noopener" class="text-gold-light hover:text-gold">t.me/dengisverhu</a></footer>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page())
    print("index.html готов:", SITE_URL)
