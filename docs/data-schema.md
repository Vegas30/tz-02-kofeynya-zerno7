---
title: Схема данных и события
date: 2026-11-08
tags: [data, analytics, zerno7]
---

# Схема данных и события

Готовые данные лежат в `js/data.js` (корень репозитория). Здесь описаны их форма и правила. Поведение и файлы — [architecture.md](architecture.md).

## 1. Сущности

Все данные — глобальный объект `window.ZERNO`.

| Поле | Тип | Источник | Примечание |
|---|---|---|---|
| `brand` | `{name, operator, legal{inn, kpp, ogrn}, schoolSince, cafeSeats, ownRoastery, hours, tagline, heroOffer, thanksNext}` | ТЗ: шапка, раздел 2, Приложение А | «Пн–Вс 08:00–22:00» |
| `school` | `{classMachines: 3, groupMax: 6}` | ТЗ | |
| `contacts` | `{phone, phoneHref, email, address, mapService, mapUrl, telegram, whatsapp}` | шапка ТЗ; `telegram` взят из контактов руководителя школы, `whatsapp` собран из основного номера | адрес вымышленный, карта его не найдёт |
| `social[]` | `{id, title, url}` | Instagram `zerno7_coffee` назван в ТЗ; VK и Telegram по тому же имени | заменить реальными ссылками на этапе 4 |
| `courses[]` | `{id, title, lessons, lessonHours, priceRub, maxPeople, subtitle?, program?}` | ТЗ; `program` — темы занятий | `id` ∈ `barista_basic`, `latte_art`, `alternative`, `corporate`; `null` = не указано |
| `startMonths[]` | `{id, title}` | ТЗ 6.1 | `dec_2026`, `jan_2027`, `feb_2027` |
| `intakes[]` | `{id, courseId, date, startMonth, capacity, seatsFree}` | даты ТЗ; `seatsFree` — условные числа | `id = <courseId>_<YYYY-MM-DD>` |
| `menuFilters[]` | `{id, title}` | ТЗ 3.2 | `coffee`, `tea`, `dessert`, `lactose-free` |
| `menu[]` | `{id, title, category, priceRub?, priceFromRub?, volumeMl, lactoseFree}` | 24 позиции: 12 кофе, 6 чая и матчи, 6 десертов | `lactoseFree` — `true` или `false`; фильтр «без лактозы» берёт `true` |
| `beans[]` | `{id, title, country, process, taste, roastLevel, weightG, priceFromRub}` | 6 сортов | `roastLevel` ∈ `light`, `medium`, `dark` → параметр `roast_level` |
| `teachers[]` | `{id, name, role, experience}` | 3 преподавателя | |
| `faq[]` | `{q, a}` | 5 вопросов | |
| `promo.latteArt` | `{code: "LATTE10", courseId}` | ТЗ | размер скидки не называть |
| `form` | `{endpoint}` | этап 3 | `null` = демо-режим |
| `analytics` | `{measurementId}` | этап 2 | `null` пока нет ресурса GA4 |
| `quiz` | `{tieBreak[], questions[{id, text, answers[{text, points{course: n}}]}]}` | [quiz.md](quiz.md) | |

Правила:

- **Цены.** Допустимы только суммы, которые есть в `js/data.js` (`priceRub`, `priceFromRub`). `tools/check.py` собирает их оттуда, ищет в HTML любые суммы с ₽ и ругается на остальные.
- **`null` и пустые массивы.** Если значения нет, блок не заполняется выдумкой: пробел записывается в README, раздел «Пробелы».
- **Места.** `seatsFree > 0` — поток открыт. Иначе «мест нет»: `aria-disabled="true"`, обработчик клика ничего не делает, ссылка не ведёт на форму.

## 2. Данные заявки (раздел 6 ТЗ)

Заявка уходит приёмнику (Apps Script, этап 3) как JSON. Лист «Zerno7 — Leads», лист `leads`, столбцы по порядку: `request_id`, `created_at`, `name`, `phone`, `email`, `course`, `start_month`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `status`. `created_at` и `status = new` ставит приёмник, значение `status` из браузера он игнорирует.

С сайта отправляются:

| Поле | Откуда | Правила |
|---|---|---|
| `request_id` | `form.js`: `REQ-` + UUID | обязательно |
| `name` | поле формы | 2–60 символов, обязательно |
| `phone` | поле формы | «+7 и 10 цифр», обязательно |
| `email` | поле формы | необязательно; если есть, формат адреса |
| `course` | поле формы | `barista_basic`, `latte_art`, `alternative`, `corporate` |
| `start_month` | поле формы | `dec_2026`, `jan_2027`, `feb_2027` |
| `utm_source` | `sessionStorage`, иначе `direct` | |
| `utm_medium` | `sessionStorage`, иначе `none` | |
| `utm_campaign` | `sessionStorage`, иначе `not_set` | |
| `utm_content` | `sessionStorage`, иначе `not_set` | |

Все строки не длиннее 200 символов. Согласие на обработку данных проверяется на сайте и в приёмник не передаётся как отдельный столбец. Объект заявки живёт в памяти страницы до отправки; на `thanks.html` передаётся только `request_id`.

Ответ приёмника: `{"ok": true}` или `{"ok": false, "error": "…"}`.

## 3. Каталог событий (ТЗ 4.2)

Сайт отправляет 20 событий: 6 собирает расширенная статистика GA4 без кода, 14 программирует исполнитель; обязательны 18, события «по выбору» дают дополнительные баллы. Все вызовы `gtag('event', …)` находятся в `js/analytics.js` ([architecture.md](architecture.md), раздел 6).

| № | Событие | Тип | Когда отправляется | Параметры | Как |
|---|---|---|---|---|---|
| 1 | `page_view` | авто | открытие любой страницы | `page_location`, `page_title` | GA4 |
| 2 | `scroll` | авто | прокрутка до 90 % | `percent_scrolled` | GA4 |
| 3 | `click` | авто | переход по ссылке на внешний сайт | `link_url`, `outbound` | GA4 |
| 4 | `file_download` | авто | скачивание PDF | `file_name`, `file_extension` | GA4 |
| 5 | `form_start` | авто | первое взаимодействие с формой | `form_id` | GA4 |
| 6 | `form_submit` | авто | отправка формы | `form_id` | GA4 |
| 7 | `generate_lead` (ключевое) | рекоменд. | приёмник ответил `ok: true` | `lead_course`, `lead_source` | `Z7.track` в `form.js` |
| 8 | `cta_click` | своё | клик по любой кнопке заявки | `button_name`, `page_section` | `data-event` |
| 9 | `view_course` | своё | клик по карточке курса | `course_name` | `data-event` |
| 10 | `select_course_date` | своё | кнопка «Выбрать поток» | `course_name`, `start_date` | `data-event` |
| 11 | `quiz_complete` | своё | завершение теста | `quiz_result` | `Z7.track` в `quiz.js` |
| 12 | `menu_filter` | своё | изменение фильтра меню | `filter_value` | `data-event` |
| 13 | `bean_view` | своё | клик по карточке сорта | `bean_name`, `roast_level` | `data-event` |
| 14 | `promo_copy` | своё | копирование промокода | `promo_code` | `data-event` |
| 15 | `contact_click` (ключевое) | своё | клик по телефону или e-mail | `contact_type` | `data-event` |
| 16 | `messenger_click` (ключевое) | своё | клик Telegram или WhatsApp | `messenger` | `data-event` |
| 17 | `social_click` | своё | клик по иконке соцсети в подвале или на `thanks.html` | `network`, `page_section` | `data-event` |
| 18 | `form_error` | своё | форма не отправлена из-за ошибки поля | `field_name`, `error_type` | `Z7.track` в `form.js` |
| 19 | `map_open` (по выбору) | своё | клик по ссылке на карту | `map_service` | `data-event` |
| 20 | `gallery_view` (по выбору) | своё | открытие фото в галерее | `photo_index` | `data-event` |

Значения параметров:

| Параметр | Значения |
|---|---|
| `course_name`, `lead_course`, `quiz_result` | код курса: `barista_basic`, `latte_art`, `alternative`, `corporate` |
| `start_date` | дата потока `YYYY-MM-DD` |
| `lead_source` | значение `utm_source` из `sessionStorage`, иначе `direct` |
| `button_name` | `header_enroll`, `hero_trial`, `quiz_enroll`, `repeat_enroll`, `beans_order`, `guide_enroll` и подобные в `snake_case` |
| `page_section` | `header`, `hero`, `courses`, `quiz`, `repeat_cta`, `footer`, `beans`, `guide`, `thanks` и подобные |
| `filter_value` | `coffee`, `tea`, `dessert`, `lactose-free`; дефис в значении допустим, правило `snake_case` касается имён, не значений |
| `bean_name`, `roast_level` | `id` сорта из `data.js`; `light`, `medium`, `dark` |
| `contact_type` | `phone`, `email` |
| `messenger` | `telegram`, `whatsapp` |
| `network` | `id` соцсети из `data.js` (`instagram` и т. п.) |
| `error_type`, `field_name` | `empty`, `format`, `consent`, `server`; `name` поля формы |
| `map_service` | `yandex` |
| `photo_index` | номер фото в галерее, с 1 |

Правила (ТЗ 4.3): имена в `snake_case`, не длиннее 40 символов; значения не длиннее 100; **имя, телефон и e-mail посетителя в GA4 не передаются ни в параметрах, ни в адресе страницы**; `generate_lead` отправляется только после ответа `ok: true`.

Следующий этап (GA4, раздел 4.4) регистрирует 7 пользовательских параметров: `button_name`, `page_section`, `course_name`, `quiz_result`, `lead_course`, `bean_name`, `messenger`. Они обязаны присутствовать в событиях уже сейчас.

Журнал `docs/events.md`: по строке на событие, поля — имя, где отправляется (файл и строка), параметры с примерами значений. Ведёт исполнитель.

Related: [spec.md](spec.md), [architecture.md](architecture.md), [quiz.md](quiz.md), [scope-site.md](scope-site.md), [tasks.md](tasks.md)
