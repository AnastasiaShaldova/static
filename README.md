## Начало работы

1. Запускаем оболочку poetry
```commandline
poetry shell
```

2. Устанавливаем зависимости
```commandline
poetry install
```

3. Создаем локальную БД и файл с переменными .env


4. Обновляем БД с помощью миграций
```commandline
alembic upgrade head
```


## Запуск локального проекта

```commandline
uvicorn app:create_app --reload --host 0.0.0.0 --port 8080
```


## Создание новых миграций

- Создание автоматически сгенерированной миграции
```commandline
alembic revision --autogenerate -m "migration message"
```
P.S. Можно изменить миграцию, если это необходимо

- Создание пустой миграции
```commandline
alembic revision -m "migration message"
```
P.P.S. Нужно обновить БД после создания миграций
