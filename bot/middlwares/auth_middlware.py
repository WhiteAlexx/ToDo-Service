from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class AuthMiddleware(BaseMiddleware):

    def __init__(self, redis_client) -> None:
        self.redis_client = redis_client

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        if data.get('event_from_user').id:
            user_id = data.get('event_from_user').id
            token = self.redis_client.get(f"user_token:{user_id}")

            data['token'] = token

        return await handler(event, data)
