#!/usr/bin/env python3
"""Регрессионные проверки подготовки изображений; тестовые файлы живут только во временной папке.

Запуск: .venv/Scripts/python.exe -I tools/test_prepare_images.py
"""
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from PIL import Image


def load_tool(name):
    """Загружает инструмент по явному пути, без импорта из каталога исходных картинок."""
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prepare = load_tool("prepare_images")
check = load_tool("check")


class PrepareImagesTests(unittest.TestCase):
    def setUp(self):
        """Создаёт отдельные пустые папки исходников и результата для каждого теста."""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "raw"
        self.output = self.root / "img"
        self.source.mkdir()

    def make_source(self, name="hero.jfif", size=(160, 100)):
        """Создаёт однотонный JPEG только как временную тестовую фикстуру."""
        path = self.source / name
        with Image.new("RGB", size, "#7A4A2A") as image:
            image.save(path, "JPEG")
        return path

    def run_tool(self, specs):
        """Запускает обычный main с заданным тестовым каталогом и перехватывает отчёт."""
        report = io.StringIO()
        args = ["prepare_images.py", str(self.source), str(self.output)]
        with patch.object(prepare, "SPECS", specs), patch("sys.argv", args), redirect_stdout(report):
            code = prepare.main()
        return code, report.getvalue()

    def test_jfif_is_processed_without_changing_source(self):
        """Проверяет JFIF, реальный WebP, размеры и сохранность исходника."""
        source = self.make_source("hero.JFIF", (320, 200))
        before = source.read_bytes()
        code, report = self.run_tool({"hero": (160, 100, "webp")})
        self.assertEqual(code, 0, report)
        self.assertEqual(source.read_bytes(), before)
        with Image.open(self.output / "hero.webp") as result:
            self.assertEqual(result.format, "WEBP")
            self.assertEqual(result.size, (160, 100))
        self.assertIn("160x100", report)
        self.assertLessEqual((self.output / "hero.webp").stat().st_size, prepare.LIMIT)

    def test_crop_is_centered_for_wide_and_tall_images(self):
        """Проверяет обрезку по центру с обеих сторон на градиенте координат."""
        for size in ((8, 4), (4, 8)):
            with self.subTest(size=size), Image.new("RGB", size) as image:
                for x in range(size[0]):
                    for y in range(size[1]):
                        image.putpixel((x, y), (x, y, 0))
                with prepare.crop_to_ratio(image, 1, 1) as result:
                    self.assertEqual(result.size, (4, 4))
                    expected = (2, 0, 0) if size[0] > size[1] else (0, 2, 0)
                    self.assertEqual(result.getpixel((0, 0)), expected)

    def test_og_keeps_exact_size(self):
        """Проверяет JPEG для OG ровно 1200×630 после обрезки."""
        self.make_source("og-main.jfif", (1600, 1000))
        code, report = self.run_tool({"og-main": (1200, 630, "jpg")})
        self.assertEqual(code, 0, report)
        with Image.open(self.output / "og-main.jpg") as result:
            self.assertEqual(result.format, "JPEG")
            self.assertEqual(result.size, (1200, 630))

    def test_small_og_is_rejected_instead_of_upscaled(self):
        """Не позволяет выдать маленькое изображение за готовое превью."""
        self.make_source("og-main.jfif", (600, 315))
        code, report = self.run_tool({"og-main": (1200, 630, "jpg")})
        self.assertEqual(code, 1)
        self.assertIn("для OG нужен исходник", report)
        self.assertIn("Не хватает (1): og-main", report)
        self.assertFalse((self.output / "og-main.jpg").exists())

    def test_failed_compression_preserves_existing_file(self):
        """При недостижимом лимите не сохраняет недопустимый файл поверх существующего."""
        for fmt in ("jpg", "webp"):
            with self.subTest(fmt=fmt):
                path = self.root / ("existing." + fmt)
                path.write_bytes(b"existing file")
                with Image.new("RGB", (20, 20)) as image, patch.object(prepare, "LIMIT", 1):
                    with self.assertRaisesRegex(ValueError, "не удалось уложить"):
                        prepare.save_under_limit(image, path, fmt)
                self.assertEqual(path.read_bytes(), b"existing file")

    def test_report_uses_saved_dimensions_after_scaling(self):
        """Проверяет, что отчёт показывает результат, а не размеры до сжатия."""
        self.make_source(size=(100, 100))
        real_save = prepare.save_under_limit

        def save_smaller(image, path, fmt):
            """Имитирует уменьшение шумного кадра без медленной генерации шума."""
            with image.resize((50, 50)) as smaller:
                quality, _ = real_save(smaller, path, fmt)
            return quality, 0.5

        with patch.object(prepare, "save_under_limit", side_effect=save_smaller):
            code, report = self.run_tool({"hero": (100, 100, "webp")})
        self.assertEqual(code, 0, report)
        self.assertIn("50x50", report)
        self.assertNotIn("100x100", report)

    def test_corrupt_file_does_not_stop_other_assets(self):
        """Возвращает ошибку битого файла и всё же обрабатывает соседний исправный."""
        self.make_source()
        (self.source / "og-main.jfif").write_bytes(b"not a JPEG")
        code, report = self.run_tool({"hero": (160, 100, "webp"), "og-main": (1200, 630, "jpg")})
        self.assertEqual(code, 1)
        self.assertIn("ошибка:", report)
        self.assertIn("Не хватает (1): og-main", report)
        self.assertTrue((self.output / "hero.webp").exists())

    def test_missing_assets_are_reported(self):
        """Не считает пустую входную папку успешно подготовленным набором."""
        code, report = self.run_tool({"hero": (160, 100, "webp")})
        self.assertEqual(code, 1)
        self.assertIn("Не хватает (1): hero", report)

    def test_unknown_names_are_not_silently_remapped(self):
        """Оставляет нестандартное имя портрета на явное решение автора."""
        self.make_source("teacher-001.jfif")
        code, report = self.run_tool({"teacher-01": (80, 100, "webp")})
        self.assertEqual(code, 1)
        self.assertIn("пропущен: имя не из", report)
        self.assertFalse(any(self.output.iterdir()))

    def test_duplicate_identifiers_fail(self):
        """Не выбирает молча один из двух файлов с одинаковым идентификатором."""
        self.make_source("hero.jfif")
        self.make_source("hero.jpg")
        code, report = self.run_tool({"hero": (160, 100, "webp")})
        self.assertEqual(code, 1)
        self.assertIn("несколько исходников", report)

    def test_source_and_output_must_differ(self):
        """Защищает исходники от перезаписи при совпадении каталогов."""
        source = self.make_source()
        before = source.read_bytes()
        args = ["prepare_images.py", str(self.source), str(self.source)]
        with patch("sys.argv", args), self.assertRaisesRegex(SystemExit, "должны различаться"):
            prepare.main()
        self.assertEqual(source.read_bytes(), before)

    def test_site_checker_excludes_only_local_materials(self):
        """Исключает raw/out/окружение, сохраняя проверку файлов самого сайта."""
        for name in ("raw/a.png", "out/a.png", ".venv/a.png", "__pycache__/a.png",
                     "img/a.png", "index.html", "js/analytics.js", "css/base.css"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        with patch.object(check, "ROOT", self.root):
            actual = {p.relative_to(self.root).as_posix() for p in check.site_files({".png", ".html", ".js", ".css"})}
        self.assertEqual(actual, {"img/a.png", "index.html", "js/analytics.js", "css/base.css"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
