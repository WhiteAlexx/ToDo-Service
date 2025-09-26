Запуск проекта

Предварительные требования:
Установленные Docker и Docker Compose
Telegram Bot Token (получить у @BotFather)

Шаги для запуска
1. Клонируйте репозиторий

2. Создайте файлы .env в директориях backend и bot:
  backend/.env:
  SECRET_KEY=your_django_secret_key
  POSTGRES_DB=
  POSTGRES_USER=
  POSTGRES_PASSWORD=
  POSTGRES_PORT=
  REDIS_URL=redis://redis:6379/0
  CELERY_BROKER=redis://redis:6379/1
  BOT_TOKEN=your_bot_token

  bot/.env:
  TOKEN=your_bot_token
  DJANGO_API_URL=http://web:8000/api
  REDIS_URL=redis://redis:6379/0

3. Запустите проект с помощью Docker Compose:
  docker-compose up --build
  
