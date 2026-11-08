---
title: Схема данных и события
date: 2026-11-08
tags: [data, analytics, zerno7]
---

# Схема данных и события

Готовые данные лежат в `js/data.js` (корень репозитория). Здесь описаны их форма и правила. Страницы и поведение — [architecture.md](architecture.md).

## 1. Сущности

Все данные — глобальный объект `window.ZERNO`.

| Поле | Тип | Источник | Примечание |
|---|---|---|---|
| `brand` | `{name, schoolSince, cafeSeats, ownRoastery, hours{days, open, close}}` | ТЗ, раздел 2 | «Пн–Вс 08:00–22:00» |
| `school` | `{classMachines: 3, groupMax: 6}` | ТЗ | |
| `courses[]` | `{id, title, lessons, lessonHours, priceRub, maxPeople, subtitle?}` | ТЗ | `null` = в ТЗ не указано; **не заменять догадкой** |
| `intakes[]` | `{id, courseId, date, capacity, seatsFree}` | даты — ТЗ; `seatsFree` — **демо** | `id = <courseId>-<YYYY-MM-DD>` |
| `menuFilters[]` | `{id, title}` | ТЗ 3.2 | `coffee`, `tea`, `dessert`, `lactose-free` |
| `menu[]` | `{id, title, category, priceRub?, priceFromRub?, volumeMl, lactoseFree}` | ТЗ | `lactoseFree: null` = неизвестно |
| `beans[]` | `{id, title, weightG, priceFromRub}` | ТЗ | сорта придумывать нельзя |
| `contacts` | `{phone, email, telegram, whatsapp, address, mapUrl}` | **заполнить (T0.1)** | |
| `social[]` | `{id, title, url}` | **заполнить (T0.1)** | |
| `teachers[]` | `{id, name, role, about}` | **заполнить (T0.1)** | |
| `promo.latteArt` | `{code: "LATTE10", courseId}` | ТЗ | размер скидки не называть |
| `quiz` | `{tieBreak[], questions[{id, text, answers[{text, points{courseId: n}}]}]}` | [quiz.md](quiz.md) | |

Правила:

- **Цены.** Единственные допустимые суммы на сайте: 140, 180, 190, 240, 260, 280, 690 (меню и зерно), 5 900, 8 900, 14 900, 24 000 ₽ (курсы). `tools/check.py` ищет в HTML любые суммы с ₽ и ругается на остальные.
- **`null` и пустые массивы.** Если контакт `null`, блок не заполняется выдумкой: либо автор ТЗ заполнил данные до запуска, либо агент записывает пробел в README, раздел «Пробелы».
- **Места.** Состояние потока: `seatsFree > 0` — «открыт», иначе «мест нет». У закрытого потока в разметке `aria-disabled="true"`, в обработчике клика проверка, ссылка не ведёт на форму.

## 2. Заявка (не хранится)

```
Lead {
  id:        "Z7-" + ГГММДД + "-" + 4 случайные цифры     // Z7-261108-4821
  name:      string, обязательное
  phone:     string, обязательное
  email:     string | ""
  courseId:  id из courses, обязательное
  intakeId:  id из intakes | ""            // обязательно, если у курса есть потоки
  promo:     string | ""
  comment:   string | ""
  consent:   true                          // без true отправка невозможна
}
```

Объект живёт только в памяти страницы до перехода на `thanks.html?id=<Lead.id>`. Номер заявки — единственное, что передаётся дальше.

## 3. Каталог событий

Каждое событие: `Z7.track(name, params)`. Имена **ровно такие**, как в таблице 3.2 ТЗ.

| Событие | Когда срабатывает | Параметры | Страницы |
|---|---|---|---|
| `contact_click` | клик по `tel:` или `mailto:` | `method` (`phone`/`email`), `place` (`header`/`footer`/`contacts`) | index, contacts |
| `cta_click` | клик по кнопке призыва | `cta_id` (`hero-enroll`, `repeat-enroll`, `beans-order`, `guide-enroll`), `page` | index, beans, latte-guide |
| `view_course` | клик «Подробнее» у курса | `course_id` | index, courses |
| `quiz_complete` | показан результат теста | `result_course_id`, `answers` (например `"0,2,1,3"`) | index |
| `gallery_view` | открыт или перелистнут снимок | `index` | index |
| `social_click` | клик по соцсети | `network` | index, thanks |
| `select_course_date` | выбран поток | `course_id`, `intake_id` | courses |
| `file_download` | клик по PDF | `file_name` | courses, latte-guide |
| `menu_filter` | смена фильтра | `filter_id` | menu |
| `map_open` | клик по ссылке на карту | — | menu |
| `bean_view` | открыта карточка зерна | `bean_id` | beans |
| `promo_copy` | код скопирован | `code` | latte-guide |
| `generate_lead` | форма успешно отправлена | `course_id`, `intake_id`, `lead_id` | contacts |
| `messenger_click` | клик Telegram или WhatsApp | `messenger` (`telegram`/`whatsapp`) | contacts |

Как проверить вручную: открыть страницу с `?debug=1`, в консоли смотреть строки `[track]`, либо ввести `dataLayer` и посмотреть массив.

Related: [spec.md](spec.md), [architecture.md](architecture.md), [quiz.md](quiz.md), [tasks.md](tasks.md)
