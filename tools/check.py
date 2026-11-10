#!/usr/bin/env python3
"""
Проверка сайта «Зерно 7» на соответствие ТЗ. Только стандартная библиотека Python 3.9+.

Запуск из корня репозитория:   python tools/check.py
Для macOS/Linux:               python3 tools/check.py

Что проверяет автоматически: файлы, SEO-теги, alt, формат и размер изображений, одинаковые
шапка и подвал, форму согласия, запрет type="module" и fetch локальных файлов, цены вне списка,
наличие событий, битые локальные ссылки, фирменные цвета и шрифты, документы курса.
Чего НЕ проверяет: Lighthouse, внешний вид, адаптивность, поведение теста и формы: это вручную
(см. docs/workflow.md).

Код выхода: 0, если нет FAIL; 1, если есть.
"""
import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index", "courses", "menu", "beans", "latte-guide", "contacts", "thanks", "privacy"]
ALL_PAGES = PAGES + ["404"]
MENU_PAGES = ["index", "courses", "menu", "beans", "contacts"]
# Допустимые суммы берутся из js/data.js (priceRub, priceFromRub); запасной список — из сокращённого ТЗ.
FALLBACK_RUB = {140, 180, 190, 240, 260, 280, 690, 5900, 8900, 14900, 24000}
# События, которые программирует исполнитель (ТЗ 4.2). file_download, page_view, scroll, click,
# form_start, form_submit собирает расширенная статистика GA4, кода не требуют.
REQUIRED_EVENTS = ["generate_lead", "cta_click", "view_course", "select_course_date", "quiz_complete",
                   "menu_filter", "bean_view", "promo_copy", "contact_click", "messenger_click",
                   "social_click", "form_error"]
OPTIONAL_EVENTS = ["map_open", "gallery_view"]  # «по выбору»: дают дополнительные баллы
FORM_FIELDS = ["name", "phone", "email", "course", "start_month", "request_id",
               "utm_source", "utm_medium", "utm_campaign", "utm_content"]
BRAND_COLORS = ["#7a4a2a", "#f6efe6", "#24211f"]
MAX_IMG = 300 * 1024
SKIP_DIRS = {".git", "docs", "tools", "node_modules", ".obsidian", ".vercel", "screens", "apps-script"}

results = []  # (уровень, сообщение)


def ok(msg):
    results.append(("PASS", msg, 0))


def fail(msg, weight=1):
    results.append(("FAIL", msg, weight))


def warn(msg):
    results.append(("WARN", msg, 0))


def check(cond, good, bad, level="FAIL"):
    if cond:
        ok(good)
    else:
        (fail if level == "FAIL" else warn)(bad)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.links = []
        self.imgs = []
        self.scripts = []
        self.anchors = []
        self.inputs = []
        self.h1 = 0
        self.text = []
        self._skip = 0
        self._form = 0
        self.has_form = False
        self.form_privacy = False

    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        a["_has"] = {k for k, _ in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "script":
            self.scripts.append(a)
            self._skip += 1
        elif tag == "style":
            self._skip += 1
        elif tag == "a":
            self.anchors.append(a)
            if self._form and "privacy.html" in a.get("href", ""):
                self.form_privacy = True
        elif tag in ("input", "select", "textarea"):
            a["_tag"] = tag
            self.inputs.append(a)
        elif tag == "h1":
            self.h1 += 1
        elif tag == "form":
            self._form += 1
            self.has_form = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
        elif tag == "form":
            self._form = max(0, self._form - 1)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if not self._skip:
            self.text.append(data)


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def image_size(path):
    """(ширина, высота) для JPEG и WebP, иначе None."""
    try:
        b = path.read_bytes()
    except OSError:
        return None
    if b[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(b):
            if b[i] != 0xFF:
                i += 1
                continue
            m = b[i + 1]
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                i += 2
                continue
            seg = struct.unpack(">H", b[i + 2:i + 4])[0]
            if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", b[i + 5:i + 9])
                return w, h
            i += 2 + seg
    elif b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        kind = b[12:16]
        if kind == b"VP8X":
            return (int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1)
        if kind == b"VP8 ":
            return (struct.unpack("<H", b[26:28])[0] & 0x3FFF, struct.unpack("<H", b[28:30])[0] & 0x3FFF)
        if kind == b"VP8L":
            v = struct.unpack("<I", b[21:25])[0]
            return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
    return None


def local_target(page_path, ref):
    """Путь локального файла по ссылке или None, если ссылка внешняя/служебная."""
    ref = ref.strip()
    if not ref or re.match(r"^(https?:|//|mailto:|tel:|#|javascript:|data:)", ref, re.I):
        return None
    p = unquote(urlparse(ref).path)
    if not p:
        return None
    base = ROOT if p.startswith("/") else page_path.parent
    return (base / p.lstrip("/")).resolve()


def site_files(exts):
    out = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            out.append(p)
    return out


def data_js_text():
    p = ROOT / "js/data.js"
    return read(p) if p.exists() else ""


def allowed_prices():
    found = {int(x) for x in re.findall(r"price(?:From)?Rub:\s*(\d+)", data_js_text())}
    return found or FALLBACK_RUB


def main():
    allowed = allowed_prices()
    # 1. Обязательные файлы
    # Отсутствующая страница весит как 6 провалов: иначе её непройденные проверки просто не считались бы.
    for page in ALL_PAGES:
        name = f"{page}.html"
        if (ROOT / name).exists():
            ok(f"Файл {name} на месте")
        else:
            fail(f"Нет файла {name} (его проверки не выполнялись)", 6)
    for name in ["README.md", "js/data.js", "js/analytics.js", "js/form.js", "docs/prompts.md",
                 "docs/quiz.md", "docs/images.md", "docs/events.md"]:
        check((ROOT / name).exists(), f"Файл {name} на месте", f"Нет файла {name}")

    pages = {}
    for name in ALL_PAGES:
        p = ROOT / f"{name}.html"
        if p.exists():
            parser = Page()
            raw = read(p)
            parser.feed(raw)
            pages[name] = (p, raw, parser)

    # 1а. Файлы из Приложения А
    check((ROOT / "files/program-barista.pdf").exists(), "files/program-barista.pdf на месте",
          "нет files/program-barista.pdf (путь задан в Приложении А)")
    if "courses" in pages:
        check(any("program-barista.pdf" in a.get("href", "") for a in pages["courses"][2].anchors),
              "courses: есть ссылка на program-barista.pdf", "courses: нет ссылки на files/program-barista.pdf")
    if "latte-guide" in pages:
        check(any(a.get("href", "").lower().endswith(".pdf") for a in pages["latte-guide"][2].anchors),
              "latte-guide: есть ссылка на PDF гида", "latte-guide: нет ссылки на PDF гида")
    if "index" in pages:
        n_img = len(pages["index"][2].imgs)
        check(n_img >= 6, f"index: {n_img} изображений (галерея 6–8)", f"index: {n_img} изображений, а в галерее нужно 6–8", "WARN")

    # 2. SEO и разметка
    titles, descs = {}, {}
    for name, (p, raw, pg) in pages.items():
        check(pg.lang == "ru", f"{name}: lang=ru", f"{name}: у <html> нет lang=\"ru\"")
        check(pg.title.strip() != "", f"{name}: есть <title>", f"{name}: пустой или отсутствует <title>")
        d = pg.meta.get("description", "").strip()
        check(d != "", f"{name}: есть meta description", f"{name}: нет meta description")
        titles.setdefault(pg.title.strip(), []).append(name)
        descs.setdefault(d, []).append(name)
        for tag in ("og:title", "og:description", "og:image"):
            check(pg.meta.get(tag, "").strip() != "", f"{name}: есть {tag}", f"{name}: нет {tag}")
        check(any("icon" in (l.get("rel", "").lower()) for l in pg.links),
              f"{name}: подключён favicon", f"{name}: нет <link rel=\"icon\">")
        check("viewport" in pg.meta, f"{name}: есть meta viewport", f"{name}: нет meta viewport")
        check(pg.h1 == 1, f"{name}: один <h1>", f"{name}: <h1> должно быть ровно одно (сейчас {pg.h1})", "WARN")
    for what, group in (("title", titles), ("description", descs)):
        dup = [v for k, v in group.items() if k and len(v) > 1]
        check(not dup, f"{what} уникальны на каждой странице",
              f"Одинаковый {what} у страниц: " + "; ".join(", ".join(v) for v in dup))

    # 3. Шапка, подвал, текущий пункт меню
    sigs = {"header": {}, "footer": {}}
    for name, (p, raw, pg) in pages.items():
        for tag in ("header", "footer"):
            m = re.search(rf"<{tag}\b.*?</{tag}>", raw, re.S | re.I)
            if not m:
                fail(f"{name}: нет <{tag}>")
                continue
            norm = re.sub(r"\s+", " ", re.sub(r'\s*aria-current="page"', "", m.group(0))).strip()
            sigs[tag][name] = norm
        h = re.search(r"<header\b.*?</header>", raw, re.S | re.I)
        if h:
            n = h.group(0).count('aria-current="page"')
            if n > 1:
                fail(f"{name}: в шапке больше одного aria-current=\"page\"")
            elif name in MENU_PAGES:
                check(n == 1, f"{name}: текущий пункт меню выделен", f"{name}: в меню не выделен текущий пункт", "WARN")
    for tag, group in sigs.items():
        if group:
            first_name, first = next(iter(group.items()))
            diff = [n for n, s in group.items() if s != first]
            check(not diff, f"<{tag}> одинаков на всех страницах",
                  f"<{tag}> отличается от {first_name} на страницах: {', '.join(diff)} "
                  f"(разрешено отличие только в aria-current)")

    # 4. Форма (contacts)
    if "contacts" in pages:
        _, raw, pg = pages["contacts"]
        check(pg.has_form, "contacts: есть форма", "contacts: нет <form>")
        boxes = [i for i in pg.inputs if i.get("type", "").lower() == "checkbox"]
        check(bool(boxes), "contacts: есть флажок согласия", "contacts: нет флажка согласия (checkbox)")
        if boxes:
            check(all("checked" not in b["_has"] for b in boxes), "флажок согласия по умолчанию снят",
                  "флажок согласия отмечен по умолчанию")
            check(any("required" in b["_has"] for b in boxes), "флажок согласия обязателен (required)",
                  "у флажка согласия нет required (JS-проверку проверьте вручную)", "WARN")
        check(pg.form_privacy, "в форме есть ссылка на privacy.html", "в форме нет ссылки на privacy.html")
        names = {i.get("name", "") for i in pg.inputs}
        miss = [f for f in FORM_FIELDS if f not in names]
        check(not miss, "в форме есть все поля из ТЗ 6.3", "в форме нет полей: " + ", ".join(miss))

    # 5. Скрипты и локальные ссылки
    for name, (p, raw, pg) in pages.items():
        for s in pg.scripts:
            check(s.get("type", "").lower() != "module", f"{name}: нет type=\"module\"",
                  f"{name}: <script type=\"module\"> не откроется двойным кликом (file://)")
            src = s.get("src")
            if src:
                t = local_target(p, src)
                if t is not None:
                    check(t.exists(), f"{name}: скрипт {src} найден", f"{name}: нет файла скрипта {src}")
        for l in pg.links:
            t = local_target(p, l.get("href", ""))
            if t is not None:
                check(t.exists(), f"{name}: {l['href']} найден", f"{name}: нет файла {l['href']}")
        for a in pg.anchors:
            t = local_target(p, a.get("href", ""))
            if t is not None:
                check(t.exists(), f"{name}: ссылка {a['href']} ведёт на файл", f"{name}: битая ссылка {a['href']}")
    for js in site_files({".js"}):
        txt = read(js)
        bad = re.search(r"fetch\(\s*['\"`][^'\"`]*\.json", txt)
        check(not bad, f"{js.name}: нет fetch локальных JSON", f"{js.name}: fetch(*.json) не работает на file://")

    # 6. Цены и скидки
    seen_bad = set()
    for name, (p, raw, pg) in pages.items():
        text = " ".join(pg.text)
        for m in re.finditer(r"(\d{1,3}(?:[\s\u00a0\u202f]\d{3})+|\d+)[\s\u00a0\u202f]*(?:₽|руб)", text):
            val = int(re.sub(r"\D", "", m.group(1)))
            if val not in allowed:
                seen_bad.add((name, val))
        if re.search(r"скидк\w*.{0,40}\d+\s*%|\d+\s*%.{0,40}скидк", text, re.I | re.S):
            warn(f"{name}: назван размер скидки в процентах, в ТЗ он не указан")
    check(not seen_bad, "в HTML нет цен вне списка из ТЗ",
          "цены вне списка ТЗ: " + ", ".join(f"{n}: {v} ₽" for n, v in sorted(seen_bad)))

    # 7. Заглушки
    ph = re.compile(r"\blorem\b|\bipsum\b|Ваш текст|Заголовок\b|\bXXX\b", re.I)
    hit = []
    for f in site_files({".html", ".js", ".css", ".md"}):
        if f.name in ("data.js", "AGENTS.md"):
            continue
        m = ph.search(read(f))
        if m:
            hit.append(f"{f.relative_to(ROOT)}: «{m.group(0)}»")
    check(not hit, "нет заглушек (Lorem ipsum, «Заголовок», «Ваш текст»)", "найдены заглушки: " + "; ".join(hit))

    # 8. Изображения
    imgs_md = read(ROOT / "docs/images.md") if (ROOT / "docs/images.md").exists() else ""
    for name, (p, raw, pg) in pages.items():
        for im in pg.imgs:
            check(im.get("alt", "").strip() != "", f"{name}: у {im.get('src', '?')} есть alt",
                  f"{name}: у изображения {im.get('src', '?')} пустой alt")
            t = local_target(p, im.get("src", ""))
            if t is not None:
                check(t.exists(), f"{name}: изображение {im['src']} найдено", f"{name}: нет файла {im['src']}")
    for f in site_files({".jpg", ".jpeg", ".webp", ".png", ".gif", ".bmp", ".avif"}):
        rel = f.relative_to(ROOT).as_posix()
        if "icons/" in rel or f.name.startswith(("favicon", "apple-touch")):
            continue
        check(f.suffix.lower() in (".jpg", ".jpeg", ".webp"), f"{rel}: формат допустим",
              f"{rel}: формат {f.suffix} (нужен WebP или JPEG)")
        size = f.stat().st_size
        check(size <= MAX_IMG, f"{rel}: {size // 1024} КБ ≤ 300", f"{rel}: {size // 1024} КБ больше 300 КБ")
        check(f.name in imgs_md, f"{rel}: источник указан в docs/images.md", f"{rel}: нет строки в docs/images.md")
    og_seen = set()
    for name, (p, raw, pg) in pages.items():
        og = pg.meta.get("og:image", "")
        if not og or og in og_seen:
            continue
        og_seen.add(og)
        t = local_target(p, og)
        if t is None:  # абсолютный адрес: ищем файл по имени
            cand = [f for f in site_files({".jpg", ".jpeg", ".webp"}) if f.name == Path(urlparse(og).path).name]
            t = cand[0] if cand else None
            if t is None:
                warn(f"{name}: og:image {og}: файл не найден в репозитории, размер не проверить")
                continue
        dims = image_size(t) if t.exists() else None
        check(dims == (1200, 630), f"og:image {t.name}: 1200×630",
              f"og:image {t.name}: размер {dims}, нужно 1200×630" if dims else f"og:image {t.name}: не удалось прочитать размер")

    # 9. События и аналитика
    code = "\n".join(read(f) for f in site_files({".js", ".html"}) if f.name != "data.js")
    missing = [e for e in REQUIRED_EVENTS if e not in code]
    check(not missing, f"все {len(REQUIRED_EVENTS)} обязательных событий найдены в коде",
          "нет в коде обязательных событий: " + ", ".join(missing))
    missing_opt = [e for e in OPTIONAL_EVENTS if e not in code]
    check(not missing_opt, "события «по выбору» есть (map_open, gallery_view)",
          "нет событий «по выбору»: " + ", ".join(missing_opt) + " (дают +2 балла каждое)", "WARN")
    an = ROOT / "js/analytics.js"
    if an.exists():
        at = read(an)
        check("dataLayer" in at and "gtag" in at, "analytics.js: заглушка gtag и dataLayer", "в analytics.js нет gtag и dataLayer")
        check("sessionStorage" in at, "analytics.js сохраняет UTM в sessionStorage", "в analytics.js нет sessionStorage (ТЗ 6.3)")
    stray = [f.relative_to(ROOT).as_posix() for f in site_files({".js", ".html"})
             if f.name not in ("analytics.js", "data.js") and re.search(r"gtag\(\s*['\"]event", read(f))]
    check(not stray, "gtag('event') вызывается только в js/analytics.js",
          "gtag('event') вне analytics.js (ТЗ 4.3): " + ", ".join(stray))
    n_attr = sum(read(f).count("data-event=") for f in site_files({".html"}))
    check(n_attr >= 10, f"в разметке {n_attr} элементов data-event", f"в разметке только {n_attr} data-event (ожидается не меньше 10)", "WARN")
    for name, (p, raw, pg) in pages.items():
        check("ga4:start" in raw and "ga4:end" in raw, f"{name}: есть слот для тега GA4", f"{name}: нет слота <!-- ga4:start --><!-- ga4:end --> в <head>", "WARN")
    js_lines = sum(len(read(f).splitlines()) for f in site_files({".js"}) if f.name != "data.js")
    check(js_lines <= 600, f"JS (без data.js): {js_lines} строк", f"JS (без data.js): {js_lines} строк, цель до 600: на приёмке вы объясняете каждую строку", "WARN")
    ev = read(ROOT / "docs/events.md") if (ROOT / "docs/events.md").exists() else ""
    gap = [e for e in REQUIRED_EVENTS if e not in ev]
    check(not gap, "docs/events.md описывает все обязательные события", "в docs/events.md нет событий: " + ", ".join(gap), "WARN")

    # 10. Стиль
    css = "\n".join(read(f).lower() for f in site_files({".css"}))
    html_all = "\n".join(raw.lower() for _, raw, _ in pages.values())
    style = css + html_all
    for c in BRAND_COLORS:
        check(c in style, f"фирменный цвет {c.upper()} используется", f"нет фирменного цвета {c.upper()}")
    check("unbounded" in style and "inter" in style, "подключены Unbounded и Inter", "не найдены шрифты Unbounded и Inter")
    check("@media" in css, "в CSS есть медиа-запросы", "в CSS нет @media (адаптивность проверьте вручную)", "WARN")
    check(re.search(r"min-(height|width):\s*44px", css) is not None, "заданы цели нажатия 44px",
          "в CSS не найден min-height/min-width: 44px (проверьте кнопки вручную)", "WARN")

    # 11. Документы и README
    readme = read(ROOT / "README.md") if (ROOT / "README.md").exists() else ""
    check(".vercel.app" in readme, "в README есть адрес .vercel.app", "в README нет адреса вида <имя>.vercel.app")
    check("Пробелы" in readme, "в README есть раздел «Пробелы»", "в README нет раздела «Пробелы»", "WARN")
    check("Не получилось" in readme and "Нейросеть использовалась для" in readme,
          "в README есть две финальные строки (ТЗ 11)", "в README нет строк «Не получилось: …» и «Нейросеть использовалась для: …»", "WARN")
    check((ROOT / "screens/lighthouse").is_dir() and any((ROOT / "screens/lighthouse").iterdir()),
          "есть снимок Lighthouse в screens/lighthouse/", "нет снимка Lighthouse в screens/lighthouse/ (ТЗ 11)", "WARN")
    prompts = read(ROOT / "docs/prompts.md") if (ROOT / "docs/prompts.md").exists() else ""
    n = len(re.findall(r"^## \d+", prompts, re.M))
    check(n >= 11, f"в журнале запросов {n} записей", f"в docs/prompts.md {n} записей; ТЗ требует запрос на структуру, на каждую страницу и на исправления (не меньше 11)", "WARN")
    check("нструмент" in prompts, "в журнале указан инструмент и версия", "в docs/prompts.md не указаны инструмент и версия нейросети (ТЗ 3.1)", "WARN")
    try:
        import subprocess
        out = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=10)
        commits = int(out.stdout.strip()) if out.returncode == 0 else None
    except Exception:
        commits = None
    if commits is not None:
        check(commits >= 10, f"коммитов в истории: {commits}", f"коммитов {commits}, ТЗ требует не меньше 10 (3.4)", "WARN")
    data = read(ROOT / "js/data.js") if (ROOT / "js/data.js").exists() else ""
    bare = re.sub(r"/\*.*?\*/", "", data, flags=re.S)
    bare = re.sub(r"//[^\n]*", "", bare)
    for what, key, need in (("позиций меню", "category:", 20), ("сортов зерна", "country:", 6),
                            ("преподавателей", "experience:", 3), ("вопросов FAQ", "q:", 5)):
        have = len(re.findall(r"\b" + re.escape(key), bare))
        check(have >= need, f"в data.js {what}: {have} (нужно {need})",
              f"в data.js {what}: {have}, по Приложению А нужно {need}", "WARN")
    todo = data.count("TODO(заказчик)")
    check(todo == 0, "в data.js нет TODO(заказчик)", f"в data.js осталось {todo} пометок TODO(заказчик): пробелы данных", "WARN")

    # Итог
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    for level, msg, _ in sorted(results, key=lambda r: order[r[0]]):
        if level != "PASS" or "-v" in sys.argv:
            print(f"[{level}] {msg}")
    p, f, w = (sum(1 for r in results if r[0] == k) for k in ("PASS", "FAIL", "WARN"))
    penalty = sum(r[2] for r in results if r[0] == "FAIL")
    points = max(0.0, 30 - 1.5 * penalty)
    print(f"\nИтого: PASS {p}, FAIL {f}, WARN {w}. Штраф {penalty} (отсутствующая страница = 6).")
    print(f"Блок A рубрики: {points:g} из 30 (30 минус 1,5 за каждый штрафной пункт). PASS-строки: ключ -v.")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
