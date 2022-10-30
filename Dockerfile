ARG PYTHON_VERSION=3.9
ARG DJANGO_SUPERUSER_USERNAME
ARG DJANGO_SUPERUSER_PASSWORD
ARG DJANGO_SUPERUSER_EMAIL
FROM python:${PYTHON_VERSION}

RUN apt-get update -q && apt-get install -yqq \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    libpq-dev \
    gcc g++ make \
    musl-dev
RUN apt-get clean -y
RUN pip install --upgrade pip 

# create directory for the app user
ENV APP_HOME=/home/app
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

# create the app user
RUN adduser --system --group app

# create the appropriate directories
RUN mkdir $APP_HOME/staticfiles $APP_HOME/mediafiles $APP_HOME/logs
RUN chmod 777 -R $APP_HOME/logs

COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
RUN python manage.py collectstatic --noinput --clear
RUN python manage.py createsuperuser --noinput

EXPOSE 8080
RUN chown -R app:app ${APP_HOME}
USER app

# run cmd
# CMD ["gunicorn", "--bind", "unix:/tmp/gunicorn.sock", "--workers", "2", "--log-level", "info", "--log-file", "/home/app/web/logs/gunicorn.log", "--error-logfile", "/home/app/web/logs/gunicorn.error.log", "--access-logfile", "/home/app/web/logs/gunicorn.access.log", "--timeout", "300", "--graceful-timeout", "300", "--reload", "app.wsgi:application"]
# CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "--log-level", "info", "--log-file", "/home/app/web/logs/gunicorn.log", "--error-logfile", "/home/app/web/logs/gunicorn.error.log", "--access-logfile", "/home/app/web/logs/gunicorn.access.log", "--timeout", "3000", "--graceful-timeout", "3000", "--reload", "superduperdrf.wsgi:application"]
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "superduperdrf.wsgi:application"]
