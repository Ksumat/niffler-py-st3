
##  Niffler E2E Tests — Python Framework 
### Создан в рамках курса по автоматизации тестирования: 
https://qa.guru/python_advanced

> Комплексный фреймворк для автоматизированного тестирования микросервисного приложения **Niffler**.  
> Поддерживает тестирование полного цикла: **UI → API → gRPC → SOAP → Kafka → Database**.

## ⚙️ Технологии и инструменты

| Категория | Инструменты |
|-----------|-------------|
| **Язык** | Python 3.11+ |
| **Тестирование** | Pytest, Pytest-xdist (параллелизация) |
| **UI автоматизация** | Playwright, Page Object Model |
| **API тестирование** | Requests, gRPC (grpcio-tools), SOAP |
| **Работа с БД** | PostgreSQL, SQLAlchemy, psycopg2 |
| **Валидация данных** | Pydantic |
| **Генерация данных** | Faker |
| **Отчётность** | Allure Reports, Jinja2 (шаблонизация) |
| **Управление зависимостями** | Poetry |
| **CI/CD** | GitHub Actions, GitHub Pages |
| **Контейнеризация** | Docker, Docker Compose |
| **Message Broker** | Apache Kafka |

---
## 📁 Структура проекта
```
📦 niffler-e-2-e-tests-python/
├── 📁 clients/ # HTTP/gRPC клиенты для сервисов Niffler
│ ├── api.py # BaseHttpClient, Category/Spend API clients
│ └── currency_client.py # gRPC клиент
├── 📁 database/ # Модели SQLAlchemy и работа с БД
├── 📁 fixtures/ # Pytest-фикстуры (session/function scope)
├── 📁 internal/pb/ # Сгенерированный gRPC код (pbreflect)
├── 📁 models/ # Pydantic-модели для валидации ответов
├── 📁 pages/ # Page Objects для Playwright (UI-тесты)
├── 📁 protos/ # .proto файлы для gRPC генерации
├── 📁 resources/ # Jinja2-шаблоны для кастомизации Allure
├── 📁 settings/ # Настройки окружения (pydantic-settings)
├── 📁 tests/ # Тестовые сценарии
│ ├── ui/ # UI-тесты Playwright
│ ├── api/ # REST API тесты
│ ├── grpc_tests/ # gRPC тесты с моками
│ ├── soap/ # SOAP тесты userdata
│ └── integration/ # Интеграционные тесты (Kafka, DB)
├── 📁 tools/ # Вспомогательные утилиты
├── .env.example # Шаблон переменных окружения
├── conftest.py # Глобальные фикстуры и хуки pytest
├── marks.py # Кастомные маркеры для фильтрации тестов
├── pyproject.toml # Зависимости Poetry
└── README.md
```
---

### Локальный запуск
 
Для запуска авто-тестов необходимо: 
1. Клонировать репозиторий
2. Поднять стенд проекта niffler согласно README.md проекта
4. Настроить интерпретатор Python 3.11+
5. Настроить виртуальное окружение:
```
python -m venv .venv
source .venv/bin/activate
```
6. Установить Poetry (выполнить в терминале IDE):
```
pip install poetry
```
7. Установить зависимости:
```
poetry install
```
8. Настроить файл .env по шаблону из .env.example

9. Запуск тестов:
```
poetry run pytest --alluredir=allure-results --clean-alluredir
```
10. Запуск тестов в многопоточном режиме:
```
poetry run pytest -n 2 --dist loadgroup --alluredir=allure-results --clean-alluredir
```
11. Визуализация результатов тестирования:
```
allure serve allure-results
```

## Мокирование gRPC

### Для мокирования GRPC на проекте используется Wiremock
Чтобы поднять контейнер выполните команду:
```
docker compose -f docker-compose.grpc_mock.yml up
```
Далее в /niffler-e-2-e-tests-python запустить тесты:

```
poetry run pytest tests/grpc_tests --mock
```

## 🔄 CI/CD (GitHub Actions)

### 📊 Воркфлоу
Файл: `.github/workflows/python-tests.yml`

**Триггеры:**
- `push` в ветку `main`
- `pull_request` в `main`
- Ручной запуск (`workflow_dispatch`)

**Этапы пайплайна:**
1. 📦 Checkout кода
2. ☕ Установка JDK 21
3. 🐳 Запуск Docker-сервисов (2-5 мин)
4. 🌐 Настройка /etc/hosts
5. ⚙️ Установка Python 3.11 + Poetry
6. 🗃 Кэширование зависимостей
7. 🌐 Установка браузеров Playwright
8. 📥 Установка зависимостей проекта
9. 🚀 Запуск тестов (параллельно, `-n auto`)
10. 📊 Генерация Allure-отчёта
11. 🌐 Публикация отчёта на GitHub Pages
12. 📦 Загрузка отчёта в артефакты

📊 [Allure Report](https://ksumat.github.io/niffler-py-st3/) 

[![Pages](https://img.shields.io/badge/pages-{status}-blue.svg)](https://ksumat.github.io/niffler-py-st3/)

