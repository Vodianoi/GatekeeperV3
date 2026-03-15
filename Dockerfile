FROM python:3.11 AS base

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mv tokenstemplate.py tokens.py

ENTRYPOINT ["python", "start.py", "-super", "-dev"]
