FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN apk add tzdata && cp /usr/share/zoneinfo/Europe/Prague /etc/localtime && echo "Europe/Prague" > /etc/timezone

RUN pip install --no-cache-dir mysql-connector-python

RUN echo '* * * * *    python /usr/src/app/main.py' > /etc/crontabs/root
RUN echo '*/5 * * * *    python /usr/src/app/outage.py' >> /etc/crontabs/root

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
