###########
# BUILDER #
###########

# pull official base image
FROM python:3.9-slim as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update -q \
    && apt-get install libpq-dev \
    gcc g++ make \
    python3-dev python-dev musl-dev -yqq

RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#######################
#  SUPER DUPER FINAL  #
#######################


# pull official base image
FROM python:3.9-slim

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles $APP_HOME/mediafiles $APP_HOME/logs
RUN chmod 777 -R $APP_HOME/logs
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update -q \
    && apt-get install libpq-dev ncat -yqq
RUN apt-get clean -y

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*
RUN rm /wheels -rf

# copy entrypoint.prod.sh
COPY ./entrypoint.prod.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
RUN chmod +x  $APP_HOME/entrypoint.prod.sh

# copy project
COPY . $APP_HOME
RUN python manage.py collectstatic --noinput --clear

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run cmd
# CMD ["gunicorn", "--bind", "unix:/tmp/gunicorn.sock", "--workers", "2", "--log-level", "info", "--log-file", "/home/app/web/logs/gunicorn.log", "--error-logfile", "/home/app/web/logs/gunicorn.error.log", "--access-logfile", "/home/app/web/logs/gunicorn.access.log", "--timeout", "300", "--graceful-timeout", "300", "--reload", "app.wsgi:application"]
CMD gunicorn --workers 2 --log-level info --log-file /home/app/web/logs/gunicorn.log --error-logfile /home/app/web/logs/gunicorn.error.log --access-logfile /home/app/web/logs/gunicorn.access.log --timeout 300 --graceful-timeout 300 --reload superduperdrf.wsgi:application
