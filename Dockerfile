FROM python:3.8

RUN pip install poetry==1.0.9

RUN mkdir /app
WORKDIR /app/

COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY crawler /app/crawler
COPY nlpengine /app/nlpengine
COPY pdfparser /app/pdfparser
COPY scheduler /app/scheduler
COPY translator /app/translator

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app"
ENV RUNNING_IN_DOCKER 1

ENTRYPOINT ["celery", "-A", "scheduler", "worker", "-l", "info"]
