from python:3.7.3-alpine3.8

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    FLASK_ENV=development \
    FLASK_APP=store \
    POETRY_VERSION=0.12.16

RUN apk update && apk add --no-cache --update postgresql-dev python3-dev  gcc build-base musl-dev

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN pip install "poetry==$POETRY_VERSION" && poetry config settings.virtualenvs.create false && poetry install

COPY . /app

EXPOSE 5000

#ENTRYPOINT ["python"]
CMD flask run
