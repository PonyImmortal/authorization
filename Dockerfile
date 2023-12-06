FROM python:3.11.4-slim-bullseye

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 5002

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5002"]
