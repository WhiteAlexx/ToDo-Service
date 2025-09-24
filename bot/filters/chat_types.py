from aiogram import types
from aiogram.filters import Filter


class ChatTypeFilter(Filter):
    '''
    Compares the transmitted chat type with the chat type obtained from the received message.\n
    Passes the comparison result to the router filter.
    '''

    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types
