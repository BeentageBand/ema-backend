FROM library/python:3.8-alpine
MAINTAINER BeentageBand

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk --update --no-cache --virtual .tmp-build-deps add python3-dev \
      gcc \
      libc-dev \
      libffi-dev
COPY ./requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip \
      && python3 -m pip install -r requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
COPY ./ema /app/ema
COPY ./restserver /app/restserver
COPY ./setup.cfg /app/setup.cfg
COPY ./manage.py /app/manage.py

FROM scratch
WORKDIR /app
COPY --from=0 / /
ENTRYPOINT [ "python3" ]
CMD [ "manage.py", "runserver" , "0.0.0.0:8000"]
