FROM python:3.11-slim

WORKDIR /usr/src/backend

RUN apt-get update && apt-get install -y netcat-openbsd

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN sed -i 's/\r$//g' /usr/src/backend/entrypoint.sh
RUN chmod +x /usr/src/backend/entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]