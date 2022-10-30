#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py collectstatic --no-input --clear
# Below command is normally using from docker-compose.
# So if you(me) use the Dockerfile with compose, command out the below line.
# As docker compose's `command` arg is already set.
gunicorn --bind :8080 --workers 2 superduperdrf.wsgi:application
exec "$@"
