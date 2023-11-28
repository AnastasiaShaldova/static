# StaticDistributor
## GOD Static 
Репозиторий с разработкой модуля Static для проекта GoD Школы IT.

### Installation
1. Клонировать репозиторий проекта и зайти в директорию проекта.
2. Создать для проекта виртуальное окружение через poetry.
3. Установить зависимости
   ```shell
   poetry shell
   ```
   ```shell
   poetry install
   ```
4. Создать локальную базу данных и  выполнить скрипт из файла DB.sql
5. Скопировать файл `.env.example` в файл `.env` и настроить его под БД.
6. Для запуска приложения необходимо ввести команду:
   ```shell
   uvicorn app:create_app --reload
   ```
7. Или воспользуйтесь Докером
   ```shell
   docker-compose up --build
   ```
---