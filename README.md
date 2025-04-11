# Классификатор банкнот

Проект представляет собой API-сервис для классификации банкнот на подлинные и поддельные с использованием машинного обучения. Сервис развернут в Docker-контейнере и включает в себя полный CI/CD пайплайн с использованием GitHub Actions.

## Основные возможности

- Классификация банкнот на подлинные/поддельные
- REST API с эндпоинтом для предсказаний
- Docker-контейнеризация
- Автоматизированное тестирование (unit и функциональные тесты)
- CI/CD пайплайн с автоматической публикацией в DockerHub
- Логирование и мониторинг

## Технологический стек

- Python 3.11
- FastAPI
- scikit-learn
- Docker
- GitHub Actions
- pytest
- uvicorn

## Структура проекта

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── model.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_model.py
│   ├── test_functional.py
│   └── scenarios.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/
    └── workflows/
        └── docker-publish.yml
```

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd banknote-classifier
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
.\venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

3. Запустите сервис:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Запуск через Docker

1. Соберите Docker-образ:
```bash
docker build -t banknote-classifier .
```

2. Запустите контейнер:
```bash
docker run -p 8080:8080 banknote-classifier
```

Или используйте docker-compose:
```bash
docker-compose up
```

## API Endpoints

### POST /predict
Эндпоинт для классификации банкнот.

Пример запроса:
```json
{
    "variance": 3.6216,
    "skewness": 8.6661,
    "curtosis": -2.8073,
    "entropy": -0.44699
}
```

Пример ответа:
```json
{
    "prediction": 0,
    "probability": 0.95
}
```

### GET /health
Эндпоинт для проверки работоспособности сервиса.

## Тестирование

### Unit-тесты
```bash
pytest tests/test_model.py
```

### Функциональные тесты
```bash
python tests/test_functional.py
```

## CI/CD

Проект использует GitHub Actions для автоматизации процессов разработки:

1. При создании Pull Request:
   - Сборка Docker-образа
   - Запуск unit-тестов
   - Запуск функциональных тестов
   - Публикация образа в DockerHub

## Модель

Используется модель машинного обучения, обученная на датасете банкнот. Модель принимает 4 признака:
- variance (дисперсия)
- skewness (асимметрия)
- curtosis (эксцесс)
- entropy (энтропия)

## Логирование

Сервис использует структурированное логирование с следующими уровнями:
- INFO: основная информация о работе сервиса
- WARNING: предупреждения
- ERROR: ошибки
- DEBUG: отладочная информация

## Безопасность

- Все API-запросы валидируются
- Используются переменные окружения для конфигурации
- Реализована базовая обработка ошибок

## Настройка GitHub Secrets

Для работы CI/CD пайплайна необходимо настроить следующие секреты в GitHub:

1. Перейдите в Settings -> Secrets and variables -> Actions
2. Добавьте следующие секреты:
   - `VAULT_TOKEN`: Токен для доступа к Vault
   - `DOCKERHUB_USERNAME`: Имя пользователя DockerHub
   - `DOCKERHUB_TOKEN`: Токен доступа к DockerHub

### Генерация токена Vault

1. Сгенерируйте токен:
```bash
python scripts/generate_vault_token.py
```

2. Скопируйте содержимое файла `vault/secrets/vault_token.txt`

3. Добавьте его как секрет `VAULT_TOKEN` в GitHub

### Настройка DockerHub

1. Создайте токен доступа в DockerHub:
   - Перейдите в Account Settings -> Security
   - Нажмите "New Access Token"
   - Выберите необходимые разрешения (read, write)

2. Добавьте токен как секрет `DOCKERHUB_TOKEN` в GitHub

## Развертывание в продакшн

### Подготовка секретов

1. Убедитесь, что все секреты настроены в GitHub

2. При пуше в ветку `main` автоматически запустится пайплайн:
   - Сборка Docker-образа
   - Запуск тестов
   - Инициализация Vault
   - Развертывание в продакшн

### Безопасность

- Токен Vault хранится в GitHub Secrets
- Секреты MongoDB хранятся в Vault
- Все контейнеры имеют доступ к секретам через переменные окружения

### Мониторинг

- Vault доступен по адресу: http://localhost:8200
- MongoDB доступен по адресу: mongodb://localhost:27017
- API доступен по адресу: http://localhost:8080