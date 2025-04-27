#!/bin/bash

set -e

echo "Контейнер стартует"

echo "Применяем миграцию..."
python manage.py makemigrations
python manage.py migrate
echo "Миграции успешно применены!"

echo "Запуск компиляцию переводов"
python manage.py compilemessages -l en -l ru
echo "Успешный компиляцию переводов"

echo "Собираем static файлы"
python manage.py collectstatic --no-input
echo "Static файлы успешно созданы!"

echo "Создание супер пользователя"
python manage.py init_superuser
echo "Супер пользователь успешно создан"

echo "-------Запуск приложения-------"
exec gunicorn --bind 0.0.0.0:8000 backend.wsgi