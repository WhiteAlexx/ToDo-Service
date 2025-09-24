#!/bin/sh

if [ "$POSTGRES_DB" = "todolist" ]
then
    echo "Waiting postgres db..."

    while ! nc -z "db" $POSTGRES_PORT; do
      sleep 1
    done

    echo "PostgreSQL db launched"
fi

python manage.py makemigrations

python manage.py migrate
echo "migrate --database=default"

if [ "$DEBUG" = "1" ]; then
    echo "DEBUG=1, skip collecting static files."
else
    python manage.py collectstatic --noinput
fi

# Создаем суперпользователя в основной базе (если не существует)
echo "Installing a superuser in the default database..."
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'super')
telegram_id = os.getenv('DJANGO_SUPERUSER_TELEGRAM_ID', 9876543210)
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'puper')

if not User.objects.using('default').filter(username=username).exists():
    user = User(
        username=username,
        telegram_id=telegram_id,
        is_staff=True,
        is_superuser=True
    )
    user.set_password(password)
    user.save(using='default')
    print("Superuser is set in the default database")
else:
    print("The superuser already exists in the default database")
EOF


exec "$@"