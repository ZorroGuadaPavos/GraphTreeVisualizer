FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY wait-for-it.sh .
RUN chmod +x ./wait-for-it.sh

COPY . .
RUN chmod +x ./prestart.sh