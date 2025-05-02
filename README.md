# TEST WORK

Цей проект реалізує REST API сервіс для роботи із задачами (Tasks) з аутентифікацією через JWT на базі FastAPI.

## Технологічний стек

* **Python 3.10+**
* **FastAPI** для побудови API
* **PostgreSQL** як база даних
* **Docker & Docker Compose** для контейнеризації
* **Pytest** для тестів

## Структура проекту

```
task_service/
├── .env                 # Файл з налаштуваннями середовища
├── docker-compose.yml   # Конфігурація Docker Compose
├── Dockerfile           # Інструкції для створення Docker образу
├── app/                 
│   ├── main.py          # Старт Uvicorn, реєстрація роутерів, створення таблиць
│   ├── database.py      # Підключення до БД
│   ├── models.py        # моделі (User, Task)
│   ├── schemas.py       # Pydantic-схеми для запитів/відповідей
│   ├── auth.py          # JWT-утиліти і залежності
│   └── routers/         # Роутери (auth.py, tasks.py)
├── tests/               # Pytest тести для auth та tasks
└── requirements.txt    
```

## Перед початком

1. Встановіть Docker та Docker Compose.
2. Склонуйте репозиторій:

   ```bash
   git clone https://github.com/your-username/task_service.git
   cd task_service
   ```
3. Створіть файл `.env` у корені проекту та заповніть:

   ```ini
   # Database settings
   db_user=postgres
   db_password=postgres
   db_host=db
   db_port=5432
   db_name=taskdb

   # JWT settings
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_MINUTES=1440
   ```

## Запуск через Docker Compose

1. Побудова та запуск контейнерів:

   ```bash
   docker-compose up --build
   ```
3. API доступне за адресою:

   * Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Основні ендпоінти

* **POST /auth/register** – реєстрація користувача (name, email, password)
* **POST /auth/login** – логін (form-data: username=email, password) → видача access & refresh токенів
* **POST /auth/refresh** – оновлення access токена (JSON: { refresh\_token })
* **POST /tasks/** – створення задачі (JSON)
* **GET /tasks/** – отримання списку із фільтрацією
* **GET /tasks/search?q=…** – пошук по назві/опису
* **PUT /tasks/{task\_id}** – оновлення задачі

> Усі `/tasks` маршрути вимагають заголовок:
>
> ```text
> Authorization: Bearer <access_token>
> ```

## Запуск тестів

1. Виконайте команду всередині контейнера web:

   ```bash
   docker-compose exec web pytest --maxfail=1 --disable-warnings -q
   ```
2. Ви побачите звіт про проходження тестів для auth та tasks.

## Локальна розробка без Docker

1. Створіть та активуйте віртуальне середовище:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Встановіть залежності:

   ```bash
   pip install -r requirements.txt
   ```
3. Створіть `.env` як у секції вище.
4. Запустіть БД PostgreSQL локально та переконайтеся, що змінні в `.env` вірні.
5. Запустіть додаток:

   ```bash
   uvicorn app.main:app --reload
   ```
6. Відкрийте Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Корисні поради

* Для зміни секретного ключа — відредагуйте змінну `SECRET_KEY` у `.env`.
* Зміни в коді підхоплюються автоматично в режимі розробки (Docker Compose з `--reload`).

---

*Перекладено українською.*
