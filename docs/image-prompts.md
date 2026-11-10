---
title: Промпты для изображений
date: 2026-11-08
tags: [images, prompts, zerno7]
---

# Промпты для изображений

Картинки для сайта генерируются в GPT и Gemini, а затем сравниваются. Требования ТЗ (3.3): WebP или JPEG, не больше 300 КБ, 1200×630 для превью ссылок, у каждой картинки `alt`, источник каждой указан в [images.md](images.md).

Всего 27 изображений. **P1** (16 шт.) нужны по Приложению А: главный экран, галерея класса из 6 фото, 3 преподавателя, 5 шагов гида, превью ссылок. **P2** (11 шт.) делают сайт богаче; без них можно обойтись и взять нейтральные блоки. Начинайте с P1.

## Как генерировать

1. **Один набор — один чат.** Галерею класса, шаги гида и преподавателей делайте подряд в одном чате: модель держит одну комнату, одну чашку, один стиль. В новом чате класс будет другим.
2. **Промпты уже полные.** Ничего подставлять не нужно, копируйте блок целиком. Они на английском: так результат стабильнее. Названия людей и брендов в промптах нет.
3. **Нужное соотношение сторон.** Если инструмент не умеет заданное, берите ближайшее: `tools/prepare_images.py` обрежет по центру. Поэтому в промптах важное держится ближе к центру.
4. **Два-три варианта на каждую картинку,** выбирайте лучший. Сохраняйте как `raw/gpt/<id>.png` и `raw/gemini/<id>.png`, где `<id>` — идентификатор ниже (`hero`, `class-01`, …).
5. **Подготовка.** `pip install pillow`, затем `python tools/prepare_images.py raw/gpt out/gpt` и то же для `gemini`. Скрипт обрежет, уменьшит, сожмёт до 280 КБ и сохранит в WebP (превью ссылок в JPEG). Если он пишет «слишком шумный», перегенерируйте.
6. **Победитель по набору, не по картинке.** Смешивать в одной галерее картинки двух моделей не стоит: разный свет и цвет выдают склейку. Выбирайте модель для набора целиком (галерея, преподаватели, гид, зерно), потом копируйте файлы в `img/`.
7. **Журнал.** В [images.md](images.md) у каждой строки допишите модель, дату и идентификатор промпта. Запросы к нейросети по ТЗ записываются в [prompts.md](prompts.md): достаточно одной записи на набор («Галерея класса: промпты class-01…class-06, GPT и Gemini, выбрана X, обрезка скриптом»).

## Как сравнивать модели

Оценка от 1 до 5 по каждому набору, лучше вдвоём и не зная, какая модель дала какую картинку:

| Критерий | Что смотреть |
|---|---|
| Следование промпту | всё из описания на месте: три кофемашины, шесть учеников, сердце на пене |
| Реализм | нет пластиковой кожи, «лишних» пальцев, оплавленных чашек и питчеров |
| Единство набора | один класс, одна чашка, один стол, один свет |
| Чистота | нет текста, логотипов, кракозябр на пакетах и фартуках |
| Палитра | кофейный, сливочный и графитовый тона, без кислотных цветов |
| Запас для кадра | важное в центре, края можно обрезать |

Если у людей на фото странные руки или лица, перегенерируйте: на странице с преподавателями это сразу видно.

## Общее для всех промптов

Стилевой блок (вставлен в каждый промпт):

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark.
```

Общие описания, на которых держится единство наборов:

- **Класс:** `Setting: a bright coffee training room with a long light-oak counter, three professional two-group espresso machines in a row in a matte graphite finish, cream wall tiles, open shelves with plain white cups. People wear charcoal-grey aprons.`
- **Чашка для гида:** `Plain white ceramic cappuccino cup on a saucer standing on a light oak table, soft side light from the left, the same cup and table in every shot of the series.`
- **Портрет:** `A fictional person, natural friendly expression, looking at the camera, soft blurred cream-coloured cafe background, upper-body portrait, charcoal-grey apron.`

## Каталог

| Файл | Размер, px | Соотношение | Приоритет | Где используется |
|---|---|---|---|---|
| `hero.webp` | 1600×1000 | 16:10 | P1 | index.html, первый экран |
| `class-01.webp` | 1200×800 | 3:2 | P1 | index.html, галерея |
| `class-02.webp` | 1200×800 | 3:2 | P1 | index.html, галерея |
| `class-03.webp` | 1200×800 | 3:2 | P1 | index.html, галерея |
| `class-04.webp` | 1200×800 | 3:2 | P1 | index.html, галерея |
| `class-05.webp` | 1200×800 | 3:2 | P1 | index.html, галерея |
| `class-06.webp` | 1200×800 | 3:2 | P1 | index.html, галерея |
| `teacher-01.webp` | 800×1000 | 4:5 | P1 | index.html, карточка преподавателя |
| `teacher-02.webp` | 800×1000 | 4:5 | P1 | index.html, карточка преподавателя |
| `teacher-03.webp` | 800×1000 | 4:5 | P1 | index.html, карточка преподавателя |
| `guide-step-1.webp` | 1000×750 | 4:3 | P1 | latte-guide.html, шаг 1 |
| `guide-step-2.webp` | 1000×750 | 4:3 | P1 | latte-guide.html, шаг 2 |
| `guide-step-3.webp` | 1000×750 | 4:3 | P1 | latte-guide.html, шаг 3 |
| `guide-step-4.webp` | 1000×750 | 4:3 | P1 | latte-guide.html, шаг 4 |
| `guide-step-5.webp` | 1000×750 | 4:3 | P1 | latte-guide.html, шаг 5 |
| `og-main.jpg` | 1200×630 | 16:9 | P1 | index, courses, menu, contacts, thanks, privacy, 404 (og:image) |
| `beans-light.webp` | 800×800 | 1:1 | P2 | beans.html, карточки светлой обжарки и «Как выбрать обжарку» |
| `beans-medium.webp` | 800×800 | 1:1 | P2 | beans.html, карточки средней обжарки и «Как выбрать обжарку» |
| `beans-dark.webp` | 800×800 | 1:1 | P2 | beans.html, карточки тёмной обжарки и «Как выбрать обжарку» |
| `roastery.webp` | 1200×800 | 3:2 | P2 | beans.html, баннер страницы |
| `cafe-interior.webp` | 1200×800 | 3:2 | P2 | menu.html, баннер страницы и блок «Карта и адрес» |
| `course-barista.webp` | 1000×750 | 4:3 | P2 | courses.html и index.html, карточка «Бариста с нуля» |
| `course-latte-art.webp` | 1000×750 | 4:3 | P2 | courses.html и index.html, карточка «Латте-арт» |
| `course-alternative.webp` | 1000×750 | 4:3 | P2 | courses.html и index.html, карточка «Альтернативное заваривание» |
| `course-corporate.webp` | 1000×750 | 4:3 | P2 | courses.html и index.html, карточка «Корпоративный мастер-класс» |
| `og-latte-guide.jpg` | 1200×630 | 16:9 | P2 | latte-guide.html (og:image) |
| `og-beans.jpg` | 1200×630 | 16:9 | P2 | beans.html (og:image) |

Зёрна по степени обжарки: карточки сортов берут картинку по полю `roastLevel` (`beans-light`, `beans-medium`, `beans-dark`), поэтому шести сортам хватает трёх картинок.

Фавикон `img/favicon.svg` (чашка в фирменных цветах) уже нарисован и в генерации не нуждается.

## Главный экран

### `hero.webp` (1600×1000, P1)

**Где:** index.html, первый экран. **Alt:** Бариста наливает молоко в чашку и рисует на кофе сердце.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. A barista in a charcoal apron pours steamed milk from a stainless steel pitcher into a white cup, a latte art heart is forming, three-quarter view from behind the bar of a cozy cafe, a professional espresso machine softly blurred in the background. The subject sits in the right third of the frame, the left third is calm and softly blurred so that a headline can be placed over it. Aspect ratio 16:10, keep the main subject away from the edges.
```

## Галерея класса (6 фото, один и тот же класс)

### `class-01.webp` (1200×800, P1)

**Где:** index.html, галерея. **Alt:** Учебный класс школы бариста: три профессиональные кофемашины и группа учеников.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Setting: a bright coffee training room with a long light-oak counter, three professional two-group espresso machines in a row in a matte graphite finish, cream wall tiles, open shelves with plain white cups. People wear charcoal-grey aprons. Wide establishing shot of the room, all three espresso machines visible in a row on the counter, six students in a half circle listening to an instructor. Aspect ratio 3:2, keep the main subject away from the edges.
```

## Галерея класса

### `class-02.webp` (1200×800, P1)

**Где:** index.html, галерея. **Alt:** Преподаватель показывает ученикам, как работать с кофемашиной.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Setting: a bright coffee training room with a long light-oak counter, three professional two-group espresso machines in a row in a matte graphite finish, cream wall tiles, open shelves with plain white cups. People wear charcoal-grey aprons. Two students at an espresso machine, the instructor beside them pointing at the portafilter, focus on hands and machine. Aspect ratio 3:2, keep the main subject away from the edges.
```

### `class-03.webp` (1200×800, P1)

**Где:** index.html, галерея. **Alt:** Руки ученика трамбуют молотый кофе в холдере.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Setting: a bright coffee training room with a long light-oak counter, three professional two-group espresso machines in a row in a matte graphite finish, cream wall tiles, open shelves with plain white cups. People wear charcoal-grey aprons. Close-up of hands tamping ground coffee in a portafilter on the counter, fine coffee grounds on the oak surface, no faces. Aspect ratio 3:2, keep the main subject away from the edges.
```

### `class-04.webp` (1200×800, P1)

**Где:** index.html, галерея. **Alt:** Ученик взбивает молоко в питчере паровым краном кофемашины.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Setting: a bright coffee training room with a long light-oak counter, three professional two-group espresso machines in a row in a matte graphite finish, cream wall tiles, open shelves with plain white cups. People wear charcoal-grey aprons. A student steams milk in a stainless steel pitcher at the steam wand, steam rising, the instructor's hand nearby, medium close-up. Aspect ratio 3:2, keep the main subject away from the edges.
```

### `class-05.webp` (1200×800, P1)

**Где:** index.html, галерея. **Alt:** Три чашки с рисунками на молочной пене: сердце, тюльпан и розетта.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Setting: a bright coffee training room with a long light-oak counter, three professional two-group espresso machines in a row in a matte graphite finish, cream wall tiles, open shelves with plain white cups. People wear charcoal-grey aprons. Top-down view of three white cups on the oak counter with different latte art patterns: a heart, a tulip and a rosetta. Aspect ratio 3:2, keep the main subject away from the edges.
```

### `class-06.webp` (1200×800, P1)

**Где:** index.html, галерея. **Alt:** Ученики пробуют кофе, приготовленный воронкой и в кемексе.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Setting: a bright coffee training room with a long light-oak counter, three professional two-group espresso machines in a row in a matte graphite finish, cream wall tiles, open shelves with plain white cups. People wear charcoal-grey aprons. Another corner of the same room: students gathered around a table with a glass Chemex, a pour-over dripper and small cups, relaxed smiles, tasting. Aspect ratio 3:2, keep the main subject away from the edges.
```

## Преподаватели

### `teacher-01.webp` (800×1000, P1)

**Где:** index.html, карточка преподавателя. **Alt:** Максим Резников, преподаватель курса «Бариста с нуля».

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. A fictional person, natural friendly expression, looking at the camera, soft blurred cream-coloured cafe background, upper-body portrait, charcoal-grey apron. A man of about 35, short dark hair, light stubble, confident and warm, leaning on an espresso machine. Aspect ratio 4:5, keep the main subject away from the edges.
```

### `teacher-02.webp` (800×1000, P1)

**Где:** index.html, карточка преподавателя. **Alt:** Алина Тарасова, преподаватель латте-арта.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. A fictional person, natural friendly expression, looking at the camera, soft blurred cream-coloured cafe background, upper-body portrait, charcoal-grey apron. A woman of about 28, hair tied back, holding a stainless steel milk pitcher in one hand and a white cup with a latte art heart in the other. Aspect ratio 4:5, keep the main subject away from the edges.
```

### `teacher-03.webp` (800×1000, P1)

**Где:** index.html, карточка преподавателя. **Alt:** Игорь Воронцов, обжарщик и преподаватель альтернативного заваривания.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. A fictional person, natural friendly expression, looking at the camera, soft blurred cream-coloured cafe background, upper-body portrait, charcoal-grey apron. A man of about 42, short beard, calm expression, standing next to a small coffee roaster and holding a scoop of freshly roasted beans. Aspect ratio 4:5, keep the main subject away from the edges.
```

## Гид «Сердце на капучино» (5 шагов, одна чашка и один стол)

### `guide-step-1.webp` (1000×750, P1)

**Где:** latte-guide.html, шаг 1. **Alt:** Шаг 1: свежий эспрессо с золотистой пенкой в белой чашке.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Plain white ceramic cappuccino cup on a saucer standing on a light oak table, soft side light from the left, the same cup and table in every shot of the series. A freshly pulled espresso with golden crema in the cup, view from 45 degrees. Aspect ratio 4:3, keep the main subject away from the edges.
```

## Гид «Сердце на капучино»

### `guide-step-2.webp` (1000×750, P1)

**Где:** latte-guide.html, шаг 2. **Alt:** Шаг 2: взбитое молоко в питчере с гладкой микропенкой.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Plain white ceramic cappuccino cup on a saucer standing on a light oak table, soft side light from the left, the same cup and table in every shot of the series. Next to the cup of espresso, a hand holds a stainless steel pitcher of glossy steamed milk with smooth microfoam, gently swirling it. Aspect ratio 4:3, keep the main subject away from the edges.
```

### `guide-step-3.webp` (1000×750, P1)

**Где:** latte-guide.html, шаг 3. **Alt:** Шаг 3: молоко наливают в слегка наклонённую чашку.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Plain white ceramic cappuccino cup on a saucer standing on a light oak table, soft side light from the left, the same cup and table in every shot of the series. A hand tilts the cup slightly while the other pours steamed milk from a pitcher held high, the milk just starting to mix with the espresso. Aspect ratio 4:3, keep the main subject away from the edges.
```

### `guide-step-4.webp` (1000×750, P1)

**Где:** latte-guide.html, шаг 4. **Alt:** Шаг 4: питчер у самой поверхности, на кофе появляется белый круг.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Plain white ceramic cappuccino cup on a saucer standing on a light oak table, soft side light from the left, the same cup and table in every shot of the series. The pitcher is held low, close to the surface, and rocked gently; a white circle is forming on the crema, the cup is being brought back to level. Aspect ratio 4:3, keep the main subject away from the edges.
```

### `guide-step-5.webp` (1000×750, P1)

**Где:** latte-guide.html, шаг 5. **Alt:** Шаг 5: тонкая линия через белое пятно, готовое сердце на капучино.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Plain white ceramic cappuccino cup on a saucer standing on a light oak table, soft side light from the left, the same cup and table in every shot of the series. Finished cappuccino with a clean heart-shaped latte art, seen from above at a slight angle, a small stainless pitcher blurred beside it. Aspect ratio 4:3, keep the main subject away from the edges.
```

## Превью ссылок

### `og-main.jpg` (1200×630, P1)

**Где:** index, courses, menu, contacts, thanks, privacy, 404 (og:image). **Alt:** Чашка капучино с сердцем на деревянном столе и кофейные зёрна.

```
Photorealistic editorial photograph, soft natural light, warm coffee brown and cream palette, no text, no letters, no logos. A white cup of cappuccino with a latte art heart on a light oak table next to scattered coffee beans, the subject in the centre of the frame with calm space around it, wide composition. Aspect ratio 16:9, keep the main subject away from the edges.
```

## Зерно (по степени обжарки)

### `beans-light.webp` (800×800, P2)

**Где:** beans.html, карточки светлой обжарки и «Как выбрать обжарку». **Alt:** Зёрна светлой обжарки, высыпанные из бумажного пакета.

```
Photorealistic product photograph, top-down, soft daylight, cream linen surface. A pile of light-roasted coffee beans (cinnamon brown, dry matte surface) spilling from a small blank kraft paper bag. Square composition, warm coffee brown and cream palette. No text, no print on the bag, no logos. Aspect ratio 1:1, keep the main subject away from the edges.
```

### `beans-medium.webp` (800×800, P2)

**Где:** beans.html, карточки средней обжарки и «Как выбрать обжарку». **Alt:** Зёрна средней обжарки, высыпанные из бумажного пакета.

```
Photorealistic product photograph, top-down, soft daylight, cream linen surface. A pile of medium-roasted coffee beans (chocolate brown, matte surface) spilling from a small blank kraft paper bag. Square composition, warm coffee brown and cream palette. No text, no print on the bag, no logos. Aspect ratio 1:1, keep the main subject away from the edges.
```

### `beans-dark.webp` (800×800, P2)

**Где:** beans.html, карточки тёмной обжарки и «Как выбрать обжарку». **Alt:** Зёрна тёмной обжарки с блестящей поверхностью, высыпанные из бумажного пакета.

```
Photorealistic product photograph, top-down, soft daylight, cream linen surface. A pile of dark-roasted coffee beans (almost black, glossy oily surface) spilling from a small blank kraft paper bag. Square composition, warm coffee brown and cream palette. No text, no print on the bag, no logos. Aspect ratio 1:1, keep the main subject away from the edges.
```

## Зерно

### `roastery.webp` (1200×800, P2)

**Где:** beans.html, баннер страницы. **Alt:** Небольшая обжарочная машина, деревянный поднос со свежеобжаренным зерном и мешки с зелёным кофе.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. A small coffee roaster machine in a cosy corner, a wooden tray of freshly roasted beans in front of it, burlap sacks of green coffee beside it, warm light. Aspect ratio 3:2, keep the main subject away from the edges.
```

## Кофейня

### `cafe-interior.webp` (1200×800, P2)

**Где:** menu.html, баннер страницы и блок «Карта и адрес». **Alt:** Уютный зал кофейни со светлыми столами и баром.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Interior of a cosy specialty coffee shop for about forty guests, light-wood tables, cream and graphite walls, warm pendant lights, an espresso machine at the bar, a few guests at tables. Aspect ratio 3:2, keep the main subject away from the edges.
```

## Карточки курсов

### `course-barista.webp` (1000×750, P2)

**Где:** courses.html и index.html, карточка «Бариста с нуля». **Alt:** Бариста готовит эспрессо на профессиональной кофемашине.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. A barista preparing espresso at a professional espresso machine, focus on the group head and portafilter, a tidy workplace. Aspect ratio 4:3, keep the main subject away from the edges.
```

### `course-latte-art.webp` (1000×750, P2)

**Где:** courses.html и index.html, карточка «Латте-арт». **Alt:** Чашка с рисунком в форме сердца на молочной пене.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Close-up of a cup with a latte art heart held in two hands over a light oak counter. Aspect ratio 4:3, keep the main subject away from the edges.
```

### `course-alternative.webp` (1000×750, P2)

**Где:** courses.html и index.html, карточка «Альтернативное заваривание». **Alt:** Воронка, кемекс и аэропресс на деревянном подносе.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. A pour-over dripper with a gooseneck kettle, a glass Chemex and an AeroPress arranged on a wooden tray. Aspect ratio 4:3, keep the main subject away from the edges.
```

### `course-corporate.webp` (1000×750, P2)

**Где:** courses.html и index.html, карточка «Корпоративный мастер-класс». **Alt:** Команда из десяти человек на мастер-классе у барной стойки.

```
Photorealistic editorial photograph, 35mm lens, soft natural window light, warm cozy specialty coffee shop atmosphere, palette of warm coffee brown, cream and charcoal graphite, shallow depth of field, natural materials and skin texture. No text, no letters, no logos, no watermark. Setting: a bright coffee training room with a long light-oak counter, three professional two-group espresso machines in a row in a matte graphite finish, cream wall tiles, open shelves with plain white cups. People wear charcoal-grey aprons. A team of ten colleagues in aprons gathered around the counter at a workshop, each with a cup, smiling, teamwork atmosphere. Aspect ratio 4:3, keep the main subject away from the edges.
```

## Превью ссылок

### `og-latte-guide.jpg` (1200×630, P2)

**Где:** latte-guide.html (og:image). **Alt:** Капучино с рисунком в форме сердца, рядом питчер.

```
Photorealistic editorial photograph, soft natural light, cream background, warm coffee brown palette, no text, no letters, no logos. Top-down view of a white cup of cappuccino with a clean heart latte art, a small stainless steel milk pitcher beside it, the subject in the centre with calm space around it, wide composition. Aspect ratio 16:9, keep the main subject away from the edges.
```

### `og-beans.jpg` (1200×630, P2)

**Где:** beans.html (og:image). **Alt:** Кофейные зёрна в бумажном пакете и совок.

```
Photorealistic editorial photograph, soft natural light, warm coffee brown tones, no text, no letters, no logos. Coffee beans in a blank kraft paper bag with a metal scoop on a light oak table, the subject in the centre with calm space around it, wide composition. Aspect ratio 16:9, keep the main subject away from the edges.
```

Related: [images.md](images.md), [tasks.md](tasks.md), [prompts.md](prompts.md)
