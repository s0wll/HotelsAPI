# Создание докер сети
docker network create my_network

# Запуск БД
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=booking_user \
    -e POSTGRES_PASSWORD=booking_password \
    -e POSTGRES_DB=booking \
    --network=my_network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:17.2

# Запуск редис кэша
docker run --name booking_cache \
    -p 7379:6379 \
    --network=my_network \
    -d redis:7

# Запуск Nginx
docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=my_network \
    --rm -p 80:80 nginx

# Все это через docker compose
docker run --name booking_back \
    -p 7777:8000 \
    --network=my_network \
    booking_app_image

docker run --name booking_celery_worker \
    --network=my_network \
    booking_app_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat \
    --network=my_network \
    booking_app_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker build -t booking_app_image .

docker rm booking_back  # remove the container

# Команды для Docker compose
docker compose up --build
docker compose up -d --build
docker logs --follow booking_back