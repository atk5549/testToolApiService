

## Требования к запуску проекта:

##### Убедитесь что установлены следующие 3 пункта:

- docker v.20.10.21
- docker-compose v.2.13.0
- python 3.8.2

# Разворачиваю PostgreSQL версии:15 с помощью docker-compose.

## docker-compose.yaml со следующими настройками:

## Переменные окружения docker-compose.yaml для PostgreSQL

- `POSTGRES_USER`:  **soaqa**
- `POSTGRES_PASSWORD`: **123123**
- `POSTGRES_DB`: **db01**
- `PGDATA`: **/var/lib/postgresql/data/pgdata**
- `POSTGRES_INITDB_ARGS`: **"-A md5"**




## Настройки для файла docker-compose.yaml

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





##  Presistent Data (Volume) / Папка с данными из PpostgreSQL
- Папка с Volume находится в корневой папке проекта testToolApiService: `./backupdb`
- Копируемые данные в контейнере postgresql находятся

`volumes`:
      - ./backupdb:/var/lib/postgresql/data

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



