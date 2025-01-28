# Pet project: Task Tracker

> Проект реализующий функционал сервиса для управления задачами
> 
> Основные сущности - Пользователь, 
> Проект(к проекту может быть прикреплены пользователи), 
> Задача(Задача связана с проектом, у неё есть статус и связанный с ней пользователь)

#  В финальной версии ожидается:
## Stack
- FastApi
- PostgreSQL (Основная бд)
- Redis (Бд для кэширования)
- Docker (Сборка и развертывание приложения)

## Фичи
- JWT авторизация
- Конфиг реализован через pydantic_settings
- Настроенный CI/CD


## Описание реализованного апи
...

# Развертывание / Установка:
## JWT
> cd /api/auth/certs
1. Генерация приватного ключа
    > openssl genrsa -out private.pem 2048
2. Выпуск публичного ключа
    > openssl rsa -in private.pem -outform PEM -pubout -out public.pem

## Файл переменного окружения
```.env
ENVIRONMENT="TEST"

PROJECT_HOST="127.0.0.1"
PROJECT_PORT="8000"
PROJECT_NAME="My pet project [TEST]"

PG__USER=backend
PG__PASSWORD=backend
PG__HOST="127.0.0.1"
PG__PORT=5432
PG__DB=task_tracker

```