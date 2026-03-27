
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
5.Установить Poetry (выполнить в терминале IDE):
```
pip install poetry
```
6.Установить зависимости:
```
poetry install
```
7. Настроить файл .env по шаблону из .env.example

8. Запуск тестов:
```
poetry run pytest --alluredir=allure-results --clean-alluredir
```
7.Запуск тестов в многопоточном режиме:
```
poetry run pytest -n 2 --dist loadgroup --alluredir=allure-results --clean-alluredir
```
8.Визуализация результатов тестирования:
```
allure serve allure-results
```

## Мокирование GRPC

### Для мокирования GRPC на проекте используется Wiremock
Чтобы поднять контейнер выполните команду:
```
docker compose -f docker-compose.grpc_mock.yml up
```
Далее в /niffler-e-2-e-tests-python запустить тесты:

```
poetry run pytest tests/grpc_tests --mock
```