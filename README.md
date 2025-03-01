# Booking API:

### Подготовка к запуску приложения
Выполните команду, находясь в директории, куда хотите скачать проект:
```
git clone git@github.com:s0wll/HotelsAPI.git
```

В директории проекта создайте файл .env и установите следующие значения переменным окружения:
```
MODE=LOCAL

DB_HOST=booking_db
DB_PORT=5432
DB_USER=booking_user
DB_PASS=booking_password
DB_NAME=booking

REDIS_HOST=booking_cache
REDIS_PORT=6379

JWT_SECRET_KEY=89d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Запуск приложения:
Выполните команду для запуска приложения:
```
docker compose up --build -d
```

После этого выполните следующую команду для вывода логов API:
```
docker logs --follow booking_back
```