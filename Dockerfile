# Image for build packages
FROM python:3.9-alpine3.14 as build-python

ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/opt/poetry"

RUN apk update \
    && apk add --no-cache --virtual .build-deps \
    build-base \
    curl \
    postgresql-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - \
    && cd /usr/local/bin \
    &&  ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

WORKDIR /app/

# Allow installing dev dependencies to run tests
ARG DEV
ENV DEV ${DEV:-true}
RUN /bin/sh -c "poetry install --no-root"


# use alpline image. final image
FROM python:3.9-alpine3.14

WORKDIR /app/

RUN addgroup --system fastapi \
    && adduser --no-create-home --system --ingroup fastapi fastapi

# copy dependens from build images
COPY --from=build-python /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
COPY --from=build-python /usr/lib/libldap_r-2.4.so.2 \
                        /usr/lib/liblber-2.4.so.2 \
                        /usr/lib/libpq.so.5 \
                        /usr/lib/libsasl2.so.3 \
                        /usr/lib/libxslt.so.1 \
                        /usr/lib/libexslt.so.0 \
                        /usr/lib/libxml2.so.2 \
                        /usr/lib/libgcrypt.so.20 \
                        /usr/lib/libgpg-error.so.0 /usr/lib/

ARG PORT
ENV PORT ${PORT:-8000}

ENV TZ ${TZ:-Asia/Almaty}
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY --chown=fastapi:fastapi . /app
USER fastapi

COPY --chown=fastapi:fastapi docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app:$PYTHONPATH

CMD ["/docker-entrypoint.sh"]
EXPOSE ${PORT}
