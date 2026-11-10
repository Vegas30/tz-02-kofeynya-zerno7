#!/usr/bin/env python3
"""
Подготовка картинок для сайта «Зерно 7».

Берёт то, что выдали GPT или Gemini (PNG, JPG, WebP любого размера), обрезает по центру до нужной
пропорции, уменьшает до размера из таблицы, сжимает так, чтобы файл был не больше 300 КБ (требование ТЗ 3.3),
и сохраняет в WebP (для превью ссылок og-*  в JPEG).

Запуск:
    pip install pillow
    python tools/prepare_images.py raw/gpt out/gpt
    python tools/prepare_images.py raw/gemini out/gemini

Имя исходного файла должно совпадать с идентификатором из docs/image-prompts.md, расширение любое:
hero.png, class-01.jpg, teacher-02.webp и т. д. Файлы с неизвестными именами пропускаются с предупреждением.
Важное в кадре держите ближе к центру: края обрезаются.
"""
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Нужна библиотека Pillow: pip install pillow")

LIMIT = 280 * 1024  # запас до лимита ТЗ в 300 КБ

# идентификатор: (ширина, высота, формат)
SPECS = {
    "hero": (1600, 1000, "webp"),
    "class-01": (1200, 800, "webp"), "class-02": (1200, 800, "webp"), "class-03": (1200, 800, "webp"),
    "class-04": (1200, 800, "webp"), "class-05": (1200, 800, "webp"), "class-06": (1200, 800, "webp"),
    "teacher-01": (800, 1000, "webp"), "teacher-02": (800, 1000, "webp"), "teacher-03": (800, 1000, "webp"),
    "guide-step-1": (1000, 750, "webp"), "guide-step-2": (1000, 750, "webp"), "guide-step-3": (1000, 750, "webp"),
    "guide-step-4": (1000, 750, "webp"), "guide-step-5": (1000, 750, "webp"),
    "beans-light": (800, 800, "webp"), "beans-medium": (800, 800, "webp"), "beans-dark": (800, 800, "webp"),
    "roastery": (1200, 800, "webp"), "cafe-interior": (1200, 800, "webp"),
    "course-barista": (1000, 750, "webp"), "course-latte-art": (1000, 750, "webp"),
    "course-alternative": (1000, 750, "webp"), "course-corporate": (1000, 750, "webp"),
    "og-main": (1200, 630, "jpg"), "og-latte-guide": (1200, 630, "jpg"), "og-beans": (1200, 630, "jpg"),
}


def crop_to_ratio(img, w, h):
    """Обрезает изображение по центру до пропорции w:h."""
    src_w, src_h = img.size
    target = w / h
    if src_w / src_h > target:  # слишком широкое: режем по бокам
        new_w = int(src_h * target)
        left = (src_w - new_w) // 2
        return img.crop((left, 0, left + new_w, src_h))
    new_h = int(src_w / target)  # слишком высокое: режем сверху и снизу
    top = (src_h - new_h) // 2
    return img.crop((0, top, src_w, top + new_h))


def save_under_limit(img, path, fmt):
    """Подбирает качество от высокого к низкому, пока файл не станет не больше LIMIT. Возвращает (качество, масштаб)."""
    scale = 1.0
    while True:
        work = img if scale == 1.0 else img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
        for quality in (88, 82, 76, 70, 64, 58, 52, 46, 40):
            if fmt == "webp":
                work.save(path, "WEBP", quality=quality, method=6)
            else:
                work.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
            if path.stat().st_size <= LIMIT:
                return quality, scale
        scale -= 0.1  # даже на минимальном качестве не влезло: уменьшаем размер
        if scale < 0.4:
            return 40, scale


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    if not src.is_dir():
        sys.exit(f"Нет папки {src}")
    dst.mkdir(parents=True, exist_ok=True)
    done = set()
    print(f"{'файл':<22}{'размер':<12}{'КБ':>5}  качество")
    for f in sorted(src.iterdir()):
        if not f.is_file() or f.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        spec = SPECS.get(f.stem)
        if spec is None:
            print(f"{f.name:<22}пропущен: имя не из docs/image-prompts.md")
            continue
        w, h, fmt = spec
        img = Image.open(f).convert("RGB")
        img = crop_to_ratio(img, w, h)
        if img.width > w:  # увеличивать не нужно: если исходник меньше, оставляем как есть
            img = img.resize((w, h), Image.LANCZOS)
        out = dst / f"{f.stem}.{fmt}"
        quality, scale = save_under_limit(img, out, fmt)
        note = f"{quality}" + (f", масштаб {scale:.1f}: исходник слишком шумный, перегенерируйте" if scale < 1 else "")
        small = "  (исходник заметно меньше нужного)" if Image.open(f).width < 0.8 * w else ""
        print(f"{out.name:<22}{img.width}x{img.height:<6}{out.stat().st_size // 1024:>5}  {note}{small}")
        done.add(f.stem)
    missing = [k for k in SPECS if k not in done]
    if missing:
        print(f"\nНе хватает ({len(missing)}): " + ", ".join(missing))


if __name__ == "__main__":
    main()
