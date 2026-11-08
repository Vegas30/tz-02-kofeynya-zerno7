/*
 * «Зерно 7» — единственный источник фактов для сайта.
 * Правило ТЗ: цены, адреса, режим работы и названия услуг, которых здесь нет, на сайте не публикуются.
 *
 * Подключение: <script src="js/data.js"></script> (обычный скрипт, не type="module"),
 * чтобы страницы открывались двойным кликом (file://) и на Vercel одинаково.
 * Доступ: window.ZERNO.courses, window.ZERNO.intakes и т. д.
 *
 * Места (seatsFree) — ДЕМО-данные: реальной системы записи нет. Эти числа не факты о кофейне,
 * в README сайта нужно написать, что они демонстрационные.
 *
 * Поля с пометкой TODO(заказчик) заполняет автор ТЗ до запуска агентов (см. docs/tasks.md, задача T0.1).
 * Пока значение null — агент не придумывает его и фиксирует пробел в README.md, раздел «Пробелы».
 */
window.ZERNO = {
  brand: {
    name: "Зерно 7",
    schoolSince: 2024,
    cafeSeats: 40,
    ownRoastery: true,
    hours: { days: "Пн–Вс", open: "08:00", close: "22:00" }
  },

  school: {
    classMachines: 3,
    groupMax: 6
  },

  courses: [
    { id: "barista",     title: "Бариста с нуля",             lessons: 5,    lessonHours: 3,    priceRub: 14900, maxPeople: null },
    { id: "latte-art",   title: "Латте-арт",                  lessons: 3,    lessonHours: null, priceRub: 8900,  maxPeople: null },
    { id: "alt-brewing", title: "Альтернативное заваривание", lessons: 2,    lessonHours: null, priceRub: 5900,  maxPeople: null,
      subtitle: "воронка, аэропресс, кемекс" },
    { id: "corporate",   title: "Корпоративный мастер-класс", lessons: null, lessonHours: null, priceRub: 24000, maxPeople: 12,
      subtitle: "для команды до 12 человек" }
  ],

  /* Потоки. capacity = ZERNO.school.groupMax. seatsFree — демо. У корпоративного мастер-класса потоков нет. */
  intakes: [
    { id: "barista-2026-12-02",     courseId: "barista",     date: "2026-12-02", capacity: 6, seatsFree: 0 },
    { id: "barista-2026-12-16",     courseId: "barista",     date: "2026-12-16", capacity: 6, seatsFree: 3 },
    { id: "barista-2027-01-13",     courseId: "barista",     date: "2027-01-13", capacity: 6, seatsFree: 6 },
    { id: "latte-art-2026-12-07",   courseId: "latte-art",   date: "2026-12-07", capacity: 6, seatsFree: 2 },
    { id: "latte-art-2027-01-20",   courseId: "latte-art",   date: "2027-01-20", capacity: 6, seatsFree: 5 },
    /* «Каждую субботу»: показываем субботы декабря 2026 */
    { id: "alt-brewing-2026-12-05", courseId: "alt-brewing", date: "2026-12-05", capacity: 6, seatsFree: 3 },
    { id: "alt-brewing-2026-12-12", courseId: "alt-brewing", date: "2026-12-12", capacity: 6, seatsFree: 6 },
    { id: "alt-brewing-2026-12-19", courseId: "alt-brewing", date: "2026-12-19", capacity: 6, seatsFree: 1 },
    { id: "alt-brewing-2026-12-26", courseId: "alt-brewing", date: "2026-12-26", capacity: 6, seatsFree: 4 }
  ],

  /* Меню. priceFromRub — «от». lactoseFree: null = неизвестно (в ТЗ не сказано). */
  menuFilters: [
    { id: "coffee",       title: "Кофе" },
    { id: "tea",          title: "Чай" },
    { id: "dessert",      title: "Десерты" },
    { id: "lactose-free", title: "Без лактозы" }
  ],
  menu: [
    { id: "espresso",   title: "Эспрессо",    category: "coffee",  priceRub: 140,     volumeMl: null, lactoseFree: null },
    { id: "cappuccino", title: "Капучино",    category: "coffee",  priceRub: 240,     volumeMl: 300,  lactoseFree: null },
    { id: "flat-white", title: "Флэт уайт",   category: "coffee",  priceRub: 260,     volumeMl: null, lactoseFree: null },
    { id: "filter",     title: "Фильтр-кофе", category: "coffee",  priceRub: 180,     volumeMl: null, lactoseFree: null },
    { id: "raf",        title: "Раф",         category: "coffee",  priceRub: 280,     volumeMl: null, lactoseFree: null },
    { id: "desserts",   title: "Десерты",     category: "dessert", priceFromRub: 190, volumeMl: null, lactoseFree: null }
    /* TODO(заказчик): позиции чая и список напитков/десертов без лактозы. Пока их нет — фильтры
       «Чай» и «Без лактозы» показывают состояние «В этой категории пока нет позиций». */
  ],

  beans: [
    { id: "own-roast", title: "Зерно собственной обжарки", weightG: 250, priceFromRub: 690 }
    /* TODO(заказчик): названия сортов, если нужны отдельные карточки. Сорта не придумывать. */
  ],

  /* TODO(заказчик): заполнить, иначе обязательные блоки «Телефон, e-mail», «Telegram и WhatsApp», «Карта и адрес»
     останутся пустыми. Для учебного ТЗ можно придумать демо-значения, но один раз и одинаковые для всех агентов. */
  contacts: {
    phone: null,     // "+7 ..."
    email: null,     // "name@domain"
    telegram: null,  // "https://t.me/..."
    whatsapp: null,  // "https://wa.me/..."
    address: null,   // строка адреса
    mapUrl: null     // ссылка на карту (Яндекс / 2ГИС / OpenStreetMap)
  },

  /* TODO(заказчик): соцсети для подвала и thanks.html. Известно только, что есть Instagram
     (автоответ в нём ведёт на latte-guide.html). */
  social: [
    // { id: "instagram", title: "Instagram", url: "https://..." }
  ],

  /* TODO(заказчик): преподаватели. Выдуманные люди без пометки «демо» не допускаются. */
  teachers: [
    // { id: "...", name: "...", role: "...", about: "..." }
  ],

  /* Размер скидки в ТЗ не указан — на сайте его не называть. */
  promo: { latteArt: { code: "LATTE10", courseId: "latte-art" } },

  /* Тест «Какой курс вам подходит». Правила подсчёта — docs/quiz.md */
  quiz: {
    tieBreak: ["barista", "latte-art", "alt-brewing", "corporate"],
    questions: [
      {
        id: "q1", text: "Зачем вам кофейные навыки?",
        answers: [
          { text: "Хочу найти подработку или работу в кофейне",        points: { "barista": 3, "latte-art": 1 } },
          { text: "Хочу готовить вкусный кофе для себя",                points: { "alt-brewing": 3, "latte-art": 1 } },
          { text: "Хочу рисовать узоры на молочной пене",               points: { "latte-art": 3, "barista": 1 } },
          { text: "Нужно обучить сотрудников моего кафе",               points: { "corporate": 3, "barista": 1 } }
        ]
      },
      {
        id: "q2", text: "Есть ли у вас опыт работы с кофемашиной?",
        answers: [
          { text: "Никакого, ни разу не пробовал(а)",                   points: { "barista": 2, "alt-brewing": 1 } },
          { text: "Готовлю кофе дома, но без профессиональной техники", points: { "alt-brewing": 2, "latte-art": 1 } },
          { text: "Умею делать эспрессо и молочные напитки",            points: { "latte-art": 3 } },
          { text: "Работаю в кофейне или у меня есть своё кафе",        points: { "corporate": 1, "latte-art": 1 } }
        ]
      },
      {
        id: "q3", text: "Сколько занятий вам подходит?",
        answers: [
          { text: "1–2 занятия",                                        points: { "alt-brewing": 3, "corporate": 1 } },
          { text: "3 занятия",                                          points: { "latte-art": 3 } },
          { text: "5 занятий",                                          points: { "barista": 3 } },
          { text: "Нужно один раз собрать всю команду",                 points: { "corporate": 3 } }
        ]
      },
      {
        id: "q4", text: "Что для вас важнее всего получить?",
        answers: [
          { text: "Навык, с которым можно устроиться на работу",        points: { "barista": 3 } },
          { text: "Красивую подачу напитков",                           points: { "latte-art": 3 } },
          { text: "Понимание вкуса и способов заваривания",             points: { "alt-brewing": 3 } },
          { text: "Единые стандарты работы в команде",                  points: { "corporate": 3 } }
        ]
      }
    ]
  }
};
