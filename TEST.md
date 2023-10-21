

# Требования к запуску проекта:

##### Убедитесь что установлены следующие 3 пункта:

- docker v.20.10.21
- docker-compose v.2.13.0
- python 3.8.2

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
- `POSTGRES_DB`: **db01**
- `PGDATA`: **/var/lib/postgresql/data/pgdata**
- `POSTGRES_INITDB_ARGS`: **"-A md5"**

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
 с названием по default-у: `backupdb`

# Построение контейнера и запуск проекта:

- Создайте локальную папку с проектом (в моём случае это папка с названием "testToolApiService")
- Склонируйте репозиторий по адресу: https://github.com/atk5549/testToolApiService.git
- Перейдите в папку с проектом:  `cd testToolApiService`
- Запустите следующую команду в терминале: `docker-compose -f docker-compose.yaml up -d`

# Запуск проекта после установки PostgreSQL:15

- Создайте локальную папку с проектом (в моём случае это папка с названием "testToolApiService")
- Склонируйте репозиторий по адресу: https://github.com/atk5549/testToolApiService.git
- Перейдите в папку с проектом:  `cd testToolApiService`
- Запустите следующую команду в терминале: `docker-compose -f docker-compose.yaml up -d`

## Доступ к PostgreSQL: 
- `localhost:54321`
- **Username:** soaqa 
- **Password:** 123123

## Доступ к контейнеру с PostgreSQL с использованием терминала:

```
docker exec -it postgres psql -U postgres
```



