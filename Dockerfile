FROM python:3.9

ARG IP


WORKDIR /app
COPY pyproject.toml poetry.lock .env /app/
COPY src/  /app/src

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

RUN export IP=${IP}

CMD ["python", "-m", "src"]

EXPOSE 9097