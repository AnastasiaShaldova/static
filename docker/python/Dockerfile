FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry install --no-root

COPY . /usr/src/app/

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]
