# api4# 📘 API Тестирование — DemoQA и Пользовательский API

## 📌 Описание

Проект включает в себя:
1. **Тесты для публичного API** `https://demoqa.com/swagger`:
   - Создание, удаление, получение пользователя и генерация токена.
2. **Моки и тесты для пользовательского API** `https://api.example.com/users/:id`:
   - Проверка структуры успешного и ошибочного ответа.
   - Обработка кодов 200, 204, 403, 404, 502.

---

## 📁 Структура проекта

```bash
.
├── tests/
│   ├── test_demoqa_api.py
│   └── test_mock_user_api.py
├── requirements.txt
└── README.md
