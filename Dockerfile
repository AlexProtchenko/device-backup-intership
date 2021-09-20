FROM python:3.9

WORKDIR /app
COPY pyproject.toml poetry.lock .env /app/
COPY src/  /app/src

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "'src.app:create_app()'"]

EXPOSE 8080