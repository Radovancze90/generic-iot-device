FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add --no-cache mariadb-dev

RUN pip install --no-cache-dir mysqlclient Django graphene-django>=3 django-filter>=2 django-recaptcha #tady je důležité dodržet správné verze jinak to celé přestane fungovat a myslím že jsem sem zapoměl nějaké dopsat.

CMD [ "python", "/usr/src/app/manage.py", "runserver", "0.0.0.0:8080" ]
