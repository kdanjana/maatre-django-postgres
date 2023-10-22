FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./ecommerce /app
COPY ./scripts /scripts
RUN chmod +x /scripts/run.sh

WORKDIR /app
EXPOSE 8000


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
            build-base postgresql-dev musl-dev zlib zlib-dev linux-headers  && \
    /py/bin/pip install --no-cache-dir   -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir /staticfiles && \
    chown -R django-user:django-user /staticfiles && \
    chmod -R 755 /staticfiles && \
    mkdir /mediafiles && \
    chown -R django-user:django-user /mediafiles && \
    chmod -R 755 /mediafiles

ENV PATH="/scripts:/py/bin:$PATH"

# USER django-user

CMD ["/scripts/run.sh"]
