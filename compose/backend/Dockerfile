FROM python:3.12-slim

RUN apt-get update -qy && apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY requirements-dev.txt ./

RUN pip install -r requirements-dev.txt

COPY ./alembic ./
COPY alembic.ini ./

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--log-level", "debug"]

EXPOSE 8000
