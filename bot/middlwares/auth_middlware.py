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
        if hasattr(event, 'from_user') and event.from_user:
            user_id = event.from_user.id
            token = await self.redis_client.get(f"user_token:{user_id}")

            data['user_id'] = user_id
            data['user_token'] = token

        return await handler(event, data)
