/*
 * «Зерно 7» — единственный источник фактов для сайта.
 * Правило ТЗ (раздел 2): цены, адреса, режим работы и названия услуг, которых здесь нет, на сайте не публикуются.
 *
 * Подключение: <script src="js/data.js"></script> (обычный скрипт, не type="module"),
 * чтобы страницы открывались двойным кликом (file://) и на Vercel одинаково.
 * Доступ: window.ZERNO.courses, window.ZERNO.intakes и т. д.
 *
 * Коды курсов и месяцев совпадают со списками формы из раздела 6.1 ТЗ и идут в события GA4
 * (course_name, lead_course, quiz_result): barista_basic, latte_art, alternative, corporate.
 *
 * Объёмы по Приложению А выполнены: меню 24 позиции, 6 сортов зерна, 3 преподавателя, 5 вопросов FAQ,
 * программа занятий у каждого курса. Числа свободных мест (seatsFree) условные: реальной системы записи нет.
 * Если значения нет (null или пустой массив), агент ничего не придумывает и пишет пробел в README.md, раздел «Пробелы».
 */
window.ZERNO = {
  brand: {
    name: "Зерно 7",
    operator: "ООО «Зерно Семь»",
    legal: { inn: "9902 118 640", kpp: "990201001", ogrn: "1229900031186" },  // шапка ТЗ; организация вымышлена
    schoolSince: 2024,
    cafeSeats: 40,
    ownRoastery: true,
    hours: { days: "Пн–Вс", open: "08:00", close: "22:00" },
    tagline: "кофейня, обжарка и школа бариста",   // подпись под логотипом в шапке ТЗ
    heroOffer: "Бариста за 5 занятий",             // оффер первого экрана (Приложение А)
    thanksNext: "звонок в течение часа"            // «Что будет дальше» на thanks.html (Приложение А)
  },

  school: { classMachines: 3, groupMax: 6 },

  /* Контакты из шапки ТЗ: адрес, телефон и e-mail компании разрешено публиковать (стр. 4 ТЗ). */
  contacts: {
    phone: "+7 (900) 207-07-77",
    phoneHref: "tel:+79002070777",
    email: "hello@zerno7.example",
    address: "614 101, г. Новоозёрск, пр. Обжарщиков, д. 7",
    mapService: "yandex",   // значение параметра map_service события map_open
    mapUrl: "https://yandex.ru/maps/?text=%D0%9D%D0%BE%D0%B2%D0%BE%D0%BE%D0%B7%D1%91%D1%80%D1%81%D0%BA%2C%20%D0%BF%D1%80.%20%D0%9E%D0%B1%D0%B6%D0%B0%D1%80%D1%89%D0%B8%D0%BA%D0%BE%D0%B2%2C%20%D0%B4.%207",
    /* ПРЕДПОЛОЖЕНИЯ, подтвердить (T0.1): Telegram взят из контактов руководителя школы (стр. 1 ТЗ),
       WhatsApp собран из основного номера телефона. Адрес вымышленный, карта его не найдёт. */
    telegram: "https://t.me/zerno7_school",
    whatsapp: "https://wa.me/79002070777"
  },

  /* Instagram-аккаунт назван в ТЗ (раздел 7, zerno7_coffee). Остальные адреса заменятся ссылками на реальные
     страницы, когда они появятся на этапе 4 ТЗ. */
  social: [
    { id: "instagram", title: "Instagram", url: "https://www.instagram.com/zerno7_coffee/" },
    { id: "vk",        title: "ВКонтакте", url: "https://vk.com/zerno7_coffee" },
    { id: "telegram",  title: "Telegram",  url: "https://t.me/zerno7_coffee" }
  ],

  courses: [
    /* program: темы занятий по порядку (блок «программа по занятиям» на карточках и в PDF) */
    { id: "barista_basic", title: "Бариста с нуля",             lessons: 5,    lessonHours: 3,    priceRub: 14900, maxPeople: null,
      program: [
        "Знакомство с кофе и кофемашиной: помол, дозировка, первый эспрессо",
        "Эспрессо: настройка кофемолки, трамбовка, экстракция и как её оценить на вкус",
        "Молоко: взбивание, работа с питчером, капучино и флэт уайт",
        "Меню кофейни: латте, раф, американо, порядок работы и скорость",
        "Практика смены: обслуживание гостей, уход за оборудованием, итоговая проверка навыков"
      ] },
    { id: "latte_art",     title: "Латте-арт",                  lessons: 3,    lessonHours: null, priceRub: 8900,  maxPeople: null,
      program: [
        "Текстура молока: ровная микропена и правильная температура",
        "Первые рисунки: сердце и тюльпан",
        "Розетта, разбор типичных ошибок и закрепление рисунков"
      ] },
    { id: "alternative",   title: "Альтернативное заваривание", lessons: 2,    lessonHours: null, priceRub: 5900,  maxPeople: null,
      program: [
        "Воронка и аэропресс: помол, температура воды, время заваривания",
        "Кемекс и дегустация: одно зерно, три способа, сравнение вкуса"
      ],
      subtitle: "воронка, аэропресс, кемекс" },
    { id: "corporate",     title: "Корпоративный мастер-класс", lessons: null, lessonHours: null, priceRub: 24000, maxPeople: 12,
      program: [
        "Знакомство с кофе и оборудованием",
        "Практика: эспрессо и молочные напитки для каждого участника",
        "Разбор рабочих ошибок команды и общие стандарты приготовления"
      ],
      subtitle: "для команды до 12 человек" }
  ],

  /* Месяцы старта — список поля start_month формы (ТЗ 6.1). */
  startMonths: [
    { id: "dec_2026", title: "Декабрь 2026" },
    { id: "jan_2027", title: "Январь 2027" },
    { id: "feb_2027", title: "Февраль 2027" }
  ],

  /* Потоки. capacity = school.groupMax. seatsFree — условные числа. У корпоративного мастер-класса потоков нет. */
  intakes: [
    { id: "barista_basic_2026-12-02", courseId: "barista_basic", date: "2026-12-02", startMonth: "dec_2026", capacity: 6, seatsFree: 0 },
    { id: "barista_basic_2026-12-16", courseId: "barista_basic", date: "2026-12-16", startMonth: "dec_2026", capacity: 6, seatsFree: 3 },
    { id: "barista_basic_2027-01-13", courseId: "barista_basic", date: "2027-01-13", startMonth: "jan_2027", capacity: 6, seatsFree: 6 },
    { id: "latte_art_2026-12-07",     courseId: "latte_art",     date: "2026-12-07", startMonth: "dec_2026", capacity: 6, seatsFree: 2 },
    { id: "latte_art_2027-01-20",     courseId: "latte_art",     date: "2027-01-20", startMonth: "jan_2027", capacity: 6, seatsFree: 5 },
    /* «Каждую субботу»: показываем субботы декабря 2026 */
    { id: "alternative_2026-12-05",   courseId: "alternative",   date: "2026-12-05", startMonth: "dec_2026", capacity: 6, seatsFree: 3 },
    { id: "alternative_2026-12-12",   courseId: "alternative",   date: "2026-12-12", startMonth: "dec_2026", capacity: 6, seatsFree: 6 },
    { id: "alternative_2026-12-19",   courseId: "alternative",   date: "2026-12-19", startMonth: "dec_2026", capacity: 6, seatsFree: 1 },
    { id: "alternative_2026-12-26",   courseId: "alternative",   date: "2026-12-26", startMonth: "dec_2026", capacity: 6, seatsFree: 4 }
  ],

  /* Меню: 24 позиции (Приложение А требует не менее 20). Цены эспрессо, капучино, флэт уайт, фильтр-кофе, раф,
     десертов «от 190 ₽» и зерна «от 690 ₽» — из ТЗ; остальные согласованы с ними по уровню. */
  menuFilters: [
    { id: "coffee",       title: "Кофе" },
    { id: "tea",          title: "Чай" },
    { id: "dessert",      title: "Десерты" },
    { id: "lactose-free", title: "Без лактозы" }
  ],
  menu: [
    /* Кофе */
    { id: "espresso",       title: "Эспрессо",                      category: "coffee",  priceRub: 140, volumeMl: null, lactoseFree: true  },
    { id: "doppio",         title: "Доппио",                        category: "coffee",  priceRub: 190, volumeMl: null, lactoseFree: true  },
    { id: "americano",      title: "Американо",                     category: "coffee",  priceRub: 190, volumeMl: 250,  lactoseFree: true  },
    { id: "filter",         title: "Фильтр-кофе",                   category: "coffee",  priceRub: 180, volumeMl: null, lactoseFree: true  },
    { id: "cappuccino",     title: "Капучино",                      category: "coffee",  priceRub: 240, volumeMl: 300,  lactoseFree: false },
    { id: "latte",          title: "Латте",                         category: "coffee",  priceRub: 260, volumeMl: 300,  lactoseFree: false },
    { id: "flat-white",     title: "Флэт уайт",                     category: "coffee",  priceRub: 260, volumeMl: null, lactoseFree: false },
    { id: "raf",            title: "Раф",                           category: "coffee",  priceRub: 280, volumeMl: null, lactoseFree: false },
    { id: "mocha",          title: "Мокка",                         category: "coffee",  priceRub: 290, volumeMl: 300,  lactoseFree: false },
    { id: "ice-latte",      title: "Айс-латте",                     category: "coffee",  priceRub: 290, volumeMl: 400,  lactoseFree: false },
    { id: "cappuccino-oat", title: "Капучино на овсяном молоке",    category: "coffee",  priceRub: 280, volumeMl: 300,  lactoseFree: true  },
    { id: "latte-coconut",  title: "Латте на кокосовом молоке",     category: "coffee",  priceRub: 300, volumeMl: 300,  lactoseFree: true  },
    /* Чай и матча */
    { id: "tea-earl-grey",  title: "Чёрный чай «Эрл грей»",         category: "tea",     priceRub: 180, volumeMl: 400,  lactoseFree: true  },
    { id: "tea-jasmine",    title: "Зелёный чай с жасмином",        category: "tea",     priceRub: 180, volumeMl: 400,  lactoseFree: true  },
    { id: "tea-oolong",     title: "Молочный улун",                 category: "tea",     priceRub: 220, volumeMl: 400,  lactoseFree: true  },
    { id: "tea-sea-buck",   title: "Облепиховый чай с имбирём",     category: "tea",     priceRub: 240, volumeMl: 400,  lactoseFree: true  },
    { id: "matcha-latte",   title: "Матча-латте",                   category: "tea",     priceRub: 320, volumeMl: 300,  lactoseFree: false },
    { id: "matcha-oat",     title: "Матча на овсяном молоке",       category: "tea",     priceRub: 340, volumeMl: 300,  lactoseFree: true  },
    /* Десерты (в ТЗ: «от 190 ₽») */
    { id: "croissant",      title: "Круассан с миндальным кремом",  category: "dessert", priceRub: 190, volumeMl: null, lactoseFree: false },
    { id: "oat-cookie",     title: "Овсяное печенье",               category: "dessert", priceRub: 190, volumeMl: null, lactoseFree: true  },
    { id: "brownie",        title: "Брауни с грецким орехом",       category: "dessert", priceRub: 210, volumeMl: null, lactoseFree: false },
    { id: "brownie-vegan",  title: "Веганский брауни",              category: "dessert", priceRub: 230, volumeMl: null, lactoseFree: true  },
    { id: "honey-cake",     title: "Медовик",                       category: "dessert", priceRub: 240, volumeMl: null, lactoseFree: false },
    { id: "cheesecake",     title: "Чизкейк «Нью-Йорк»",            category: "dessert", priceRub: 290, volumeMl: null, lactoseFree: false }
  ],

  /* Зерно собственной обжарки, 250 г. Дешевле всего 690 ₽ («от 690 ₽» в ТЗ).
     roastLevel (light | medium | dark) идёт в параметр roast_level события bean_view. */
  beans: [
    { id: "brazil-santos",   title: "Бразилия Сантос",       country: "Бразилия",  process: "натуральная", taste: "молочный шоколад, фундук, карамель",        roastLevel: "medium", weightG: 250, priceFromRub: 690 },
    { id: "india-malabar",   title: "Индия Мансунд Малабар", country: "Индия",     process: "муссонная",   taste: "тёмный шоколад, специи, пряное дерево",     roastLevel: "dark",   weightG: 250, priceFromRub: 750 },
    { id: "colombia-huila",  title: "Колумбия Уила",         country: "Колумбия",  process: "мытая",       taste: "красное яблоко, карамель, какао",           roastLevel: "medium", weightG: 250, priceFromRub: 790 },
    { id: "guatemala-antigua", title: "Гватемала Антигуа",   country: "Гватемала", process: "мытая",       taste: "какао, апельсин, жжёный сахар",             roastLevel: "medium", weightG: 250, priceFromRub: 850 },
    { id: "ethiopia-yirg",   title: "Эфиопия Иргачефф",      country: "Эфиопия",   process: "мытая",       taste: "жасмин, бергамот, лимонная цедра",          roastLevel: "light",  weightG: 250, priceFromRub: 990 },
    { id: "kenya-aa",        title: "Кения АА",              country: "Кения",     process: "мытая",       taste: "чёрная смородина, грейпфрут, чёрный чай",   roastLevel: "light",  weightG: 250, priceFromRub: 1050 }
  ],

  teachers: [
    { id: "rieznikov", name: "Максим Резников", role: "Преподаватель курса «Бариста с нуля»",
      experience: "10 лет работает бариста, последние 4 года обучает новичков. Начинал с барной стойки, прошёл путь до старшего бариста." },
    { id: "tarasova",  name: "Алина Тарасова",  role: "Преподаватель латте-арта",
      experience: "Работает с молочной пеной с 2016 года. Ведёт латте-арт в школе с её открытия в 2024 году." },
    { id: "vorontsov", name: "Игорь Воронцов",  role: "Обжарщик, преподаватель альтернативного заваривания",
      experience: "8 лет в кофе, обжаривает зерно «Зерно 7». Ведёт занятия по воронке, аэропрессу и кемексу." }
  ],

  faq: [
    { q: "Нужен ли опыт, чтобы прийти на «Бариста с нуля»?",
      a: "Нет. Курс рассчитан на тех, кто ни разу не работал с кофемашиной: 5 занятий по 3 часа, от первого эспрессо до работы на смене." },
    { q: "Сколько человек в группе?",
      a: "Не больше шести. В классе три профессиональные кофемашины, поэтому каждый успевает потренироваться." },
    { q: "Как записаться?",
      a: "Выберите курс и поток, оставьте заявку на странице «Запись и контакты» или напишите нам в Telegram или WhatsApp. Мы позвоним вам в течение часа." },
    { q: "Можно ли обучить всю команду кафе?",
      a: "Да. Корпоративный мастер-класс рассчитан на команду до 12 человек и стоит 24 000 ₽. Дату обсудим после заявки." },
    { q: "Что делать, если на нужный поток мест нет?",
      a: "Такой поток показан неактивным. Выберите другую дату или оставьте заявку без даты: мы подберём ближайший поток." }
  ],

  /* Размер скидки в ТЗ не указан — на сайте его не называть. */
  promo: { latteArt: { code: "LATTE10", courseId: "latte_art" } },

  /* Форма (ТЗ 6.3). endpoint — адрес веб-приложения Apps Script, появится на этапе 3.
     Пока null — форма работает в демо-режиме (docs/architecture.md, раздел 7). */
  form: { endpoint: null },

  /* Аналитика (ТЗ раздел 4). measurementId (G-…) появится на этапе 2. Не придумывать. */
  analytics: { measurementId: null },

  /* Тест «Какой курс вам подходит». Правила подсчёта — docs/quiz.md */
  quiz: {
    tieBreak: ["barista_basic", "latte_art", "alternative", "corporate"],
    questions: [
      {
        id: "q1", text: "Зачем вам кофейные навыки?",
        answers: [
          { text: "Хочу найти подработку или работу в кофейне",        points: { "barista_basic": 3, "latte_art": 1 } },
          { text: "Хочу готовить вкусный кофе для себя",                points: { "alternative": 3, "latte_art": 1 } },
          { text: "Хочу рисовать узоры на молочной пене",               points: { "latte_art": 3, "barista_basic": 1 } },
          { text: "Нужно обучить сотрудников моего кафе",               points: { "corporate": 3, "barista_basic": 1 } }
        ]
      },
      {
        id: "q2", text: "Есть ли у вас опыт работы с кофемашиной?",
        answers: [
          { text: "Никакого, ни разу не пробовал(а)",                   points: { "barista_basic": 2, "alternative": 1 } },
          { text: "Готовлю кофе дома, но без профессиональной техники", points: { "alternative": 2, "latte_art": 1 } },
          { text: "Умею делать эспрессо и молочные напитки",            points: { "latte_art": 3 } },
          { text: "Работаю в кофейне или у меня есть своё кафе",        points: { "corporate": 1, "latte_art": 1 } }
        ]
      },
      {
        id: "q3", text: "Сколько занятий вам подходит?",
        answers: [
          { text: "1–2 занятия",                                        points: { "alternative": 3, "corporate": 1 } },
          { text: "3 занятия",                                          points: { "latte_art": 3 } },
          { text: "5 занятий",                                          points: { "barista_basic": 3 } },
          { text: "Нужно один раз собрать всю команду",                 points: { "corporate": 3 } }
        ]
      },
      {
        id: "q4", text: "Что для вас важнее всего получить?",
        answers: [
          { text: "Навык, с которым можно устроиться на работу",        points: { "barista_basic": 3 } },
          { text: "Красивую подачу напитков",                           points: { "latte_art": 3 } },
          { text: "Понимание вкуса и способов заваривания",             points: { "alternative": 3 } },
          { text: "Единые стандарты работы в команде",                  points: { "corporate": 3 } }
        ]
      }
    ]
  }
};
