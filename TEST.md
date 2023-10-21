

# Требования к запуску проекта:

##### Убедитесь что установлены следующие 3 пункта:

- **docker**         (*версия: 20.10.21*)
- **docker-compose** (*версия: 2.13.0*)
- **python**         (*версия: 3.8.2*)
- **pip**         (*версия: 23.3*)

# Подьем контейнера с PostgreSQL версии:15 с помощью docker-compose с подключением папки для сохранения данных, во избежании потери данных при перезагрузке контейнера.

## Переменные окружения docker-compose.yaml для PostgreSQL

- `POSTGRES_USER`:  **soaqa**
- `POSTGRES_PASSWORD`: **123123**
- `POSTGRES_DB`: **db01**
- `PGDATA`: **/var/lib/postgresql/data/pgdata**
- `POSTGRES_INITDB_ARGS`: **"-A md5"**

## Переменные окружения для файла .env для успешного запуска проекта на микрофреймворке FLASK

- `FLASK_APP`:  **flsite**
- `FLASK_ENV`: **development**
- `DATABASE_URL`: **postgresql://soaqa:123123@localhost:54321/db01**

## Код из файла docker-compose.yaml

```
version: '3.1'
services:
  db:
    image: postgres:15
    container_name: my_docker_postgres
    restart: unless-stopped
    ports:
      - "54321:5432"
    environment:
      POSTGRES_PASSWORD: 123123
      POSTGRES_USER: soaqa
      POSTGRES_DB: db01
      PGDATA: /var/lib/postgresql/data/pgdata
      POSTGRES_INITDB_ARGS: "-A md5"
    volumes:
      - ./backupdb:/var/lib/postgresql/data     
```

##  Касаемо Presistent Data (Volume) и PpostgreSQL данных
- Папка сохраняемых данных из PostgreSQL находится в корневой папке проекта testToolApiService,
 с названием: `backupdb`


 ## Зависимости из файла requirements.txt:
```
alembic==1.12.0
aniso8601==9.0.1
apispec==6.3.0
blinker==1.6.3
build==1.0.3
certifi==2023.7.22
charset-normalizer==3.3.0
click==8.1.7
Flask==3.0.0
flask-apispec==0.11.4
Flask-Migrate==3.1.0
Flask-RESTful==0.3.10
Flask-SQLAlchemy==3.1.1
greenlet==2.0.2
idna==3.4
importlib-metadata==6.8.0
importlib-resources==6.1.0
itsdangerous==2.1.2
Jinja2==3.1.2
Mako==1.2.4
MarkupSafe==2.1.3
marshmallow==3.20.1
packaging==23.2
psycopg2-binary==2.9.9
pyproject_hooks==1.0.0
python-dotenv==1.0.0
pytz==2023.3.post1
requests==2.31.0
six==1.16.0
SQLAlchemy==2.0.22
tomli==2.0.1
typing_extensions==4.8.0
urllib3==2.0.6
webargs==8.3.0
Werkzeug==3.0.0
zipp==3.17.0
```


# Быстрый запуск проекта:

*Команды представлены для операционной системы: **"MacOS"***
- Склонируйте следующий репозиторий: https://github.com/atk5549/testToolApiService.git
- Перейдите в папку с проектом:  `cd testToolApiService`
- В корне проекта создайте файл ".env" и запишите туда переменные окружения (см. выше)
- В корне проекта создайте папку с названием **"backupdb"** для сохранения данных из СУБД (PostgreSQL) в случае падения контейнера
- Создайте виртуальное окружение с помощью команды в терминале: `python3 -m venv venv`
- Установите зависисимости из файла requirements.txt c помощью команды в терминале: `pip3 install -r requirements.txt`
- Активируйте виртуальное окружение c помощью команды в терминале: `source venv/bin/activate`

*Теперь построим и запустим контейнер c базой данных PostgreSQL с помощью **docker-compose***
- Находясь в корневой папке проекта, следующую команду в терминале: `docker-compose -f docker-compose.yaml up --build`

## Доступ к PostgreSQL: 
- `localhost:54321` или `127.0.0.1:54321`
- **Username:** soaqa 
- **Password:** 123123

# Миграция созданной Модели во Flask в PostgreSQL

*При успешно установленных зависимостях,*
*находясь в корневой папке проекта, для миграции модели*
*небходимо в терминале ввести следующие команды:*

- `flask db init`
- `flask db migrate`
- `flask db upgrade`


# Запуск проекта

*Убедитесь что контейнер с PostgreSQL запущен*
*введите в терминале следующую команду:*

- `python3 flsite.py`




## Доступ к PostgreSQL: 
- `localhost:54321`
- **Username:** soaqa 
- **Password:** 123123

## Доступ к контейнеру с PostgreSQL с использованием терминала:

```
docker exec -it postgres psql -U postgres
```



