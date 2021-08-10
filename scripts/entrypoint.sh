#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
# TODO "Make these commands optional or an IF statement"
#python manage.py flush --no-input
#python manage.py makemigrations
#python manage.py migrate
#python manage.py collectstatic --noinput
#python manage.py loaddata scripts/db_seed_data.json

exec "$@"