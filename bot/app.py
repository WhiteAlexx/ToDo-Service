import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from aiogram_dialog import setup_dialogs

from database.redis_cli import redis_client
from dialogs.auth_dialogs import auth_dialog
from dialogs.tasks_dialogs import tasks_dialog
from handlers.user_handlers import user_private_router
from middlwares.auth_middlware import AuthMiddleware


bot = Bot(token=os.getenv('BOT_TOKEN'),
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
          )
dp = Dispatcher()


dp.include_router(auth_dialog)
dp.include_router(tasks_dialog)
dp.include_router(user_private_router)
setup_dialogs(dp)


async def on_startup(bot):
    print('BOT HAS STARTED')


async def on_shutdown(bot):
    print('BOT STOPPED')


async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(AuthMiddleware(redis_client=redis_client))

    await dp.start_polling(bot)


asyncio.run(main())
