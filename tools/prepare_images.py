#!/usr/bin/env python3
"""
Подготовка картинок для сайта «Зерно 7».

Берёт то, что выдали GPT или Gemini (PNG, JPEG/JFIF, WebP любого размера), обрезает по центру до нужной
пропорции, уменьшает до размера из таблицы, сжимает так, чтобы файл был не больше 300 КБ (требование ТЗ 3.3),
и сохраняет в WebP (для превью ссылок og-* в JPEG строго 1200×630).
Исходники не изменяются. Неполный набор или ошибка обработки дают код выхода 1.

Запуск из корня проекта (Pillow устанавливается в локальную виртуальную среду):
    python -I -m venv .venv
    .venv/Scripts/python.exe -I -m pip install Pillow
    .venv/Scripts/python.exe -I tools/prepare_images.py raw/gpt out/gpt
    .venv/Scripts/python.exe -I tools/prepare_images.py raw/gemini out/gemini

Имя исходного файла должно совпадать с идентификатором из docs/image-prompts.md, расширение любое:
hero.png, class-01.jpg, teacher-02.webp и т. д. Файлы с неизвестными именами пропускаются с предупреждением.
Важное в кадре держите ближе к центру: края обрезаются.
"""
import sys
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Нужна библиотека Pillow: установите её в .venv по инструкции в README.md")

LIMIT = 280 * 1024  # запас до лимита ТЗ в 300 КБ
SOURCE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".jfif", ".webp"}

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
    """Подбирает сжатие; пишет только допустимый файл, не уменьшает размер OG."""
    scales = (1.0,) if fmt == "jpg" else (1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4)
    for scale in scales:
        size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
        work = img if scale == 1.0 else img.resize(size, Image.Resampling.LANCZOS)
        try:
            for quality in (88, 82, 76, 70, 64, 58, 52, 46, 40):
                with BytesIO() as buffer:
                    if fmt == "webp":
                        work.save(buffer, "WEBP", quality=quality, method=6)
                    else:
                        work.save(buffer, "JPEG", quality=quality, optimize=True, progressive=True)
                    if buffer.tell() <= LIMIT:
                        path.write_bytes(buffer.getvalue())
                        return quality, scale
        finally:
            if work is not img:
                work.close()
    raise ValueError(f"не удалось уложить {path.name} в {LIMIT // 1024} КБ")


def main():
    """Обрабатывает известные изображения и сообщает о неполном или испорченном наборе."""
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    if not src.is_dir():
        sys.exit(f"Нет папки {src}")
    if src.resolve() == dst.resolve():
        sys.exit("Папки исходников и результата должны различаться")
    dst.mkdir(parents=True, exist_ok=True)
    done, seen = set(), set()
    errors = False
    print(f"{'файл':<26}{'размер':<12}{'КБ':>5}  качество")
    for source in sorted(src.iterdir()):
        if not source.is_file() or source.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        spec = SPECS.get(source.stem)
        if spec is None:
            print(f"{source.name:<26}пропущен: имя не из docs/image-prompts.md")
            continue
        if source.stem in seen:
            print(f"{source.name:<26}ошибка: несколько исходников с одним идентификатором")
            errors = True
            continue
        seen.add(source.stem)
        w, h, fmt = spec
        out = dst / f"{source.stem}.{fmt}"
        try:
            with Image.open(source) as original:
                with ImageOps.exif_transpose(original) as oriented:
                    with oriented.convert("RGB") as img:
                        cropped = crop_to_ratio(img, w, h)
            with cropped:
                if fmt == "jpg" and (cropped.width < w or cropped.height < h):
                    raise ValueError("для OG нужен исходник не меньше 1200×630 после обрезки")
                small = cropped.width < 0.8 * w or cropped.height < 0.8 * h
                size = (w, h) if cropped.width > w else cropped.size
                with cropped.resize(size, Image.Resampling.LANCZOS) as prepared:
                    quality, scale = save_under_limit(prepared, out, fmt)
            with Image.open(out) as result:
                actual_w, actual_h = result.size
            note = str(quality)
            if scale < 1:
                note += f", масштаб {scale:.1f}: исходник слишком шумный, перегенерируйте"
            if small:
                note += "  (исходник заметно меньше нужного)"
            print(f"{out.name:<26}{f'{actual_w}x{actual_h}':<12}{out.stat().st_size / 1024:>5.1f}  {note}")
            done.add(source.stem)
        except (OSError, ValueError) as error:
            print(f"{source.name:<26}ошибка: {error}")
            errors = True
    missing = [key for key in SPECS if key not in done]
    if missing:
        print(f"\nНе хватает ({len(missing)}): " + ", ".join(missing))
    return 1 if errors or missing else 0


if __name__ == "__main__":
    sys.exit(main())
