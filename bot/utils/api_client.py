import aiohttp
import os
from typing import Dict


class APIError(Exception):
    pass

class APIClient:

    def __init__(
        self,
        base_url: str
    ):
        self.base_url = base_url

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        token: str = None,
        data: Dict = None
    ):
        headers = {}
        if token:
            headers['Authorization'] = f"Token {token}"

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                f"{self.base_url}{endpoint}",
                headers=headers,
                json=data
            ) as response:
                if response.status == 401:
                    raise APIError('Неверные учетные данные')
                elif response.status >= 400:
                    error_text = await response.text()
                    raise APIError(f"Ошибка API: {response.status} - {error_text}")

                if response.status == 204:
                    return None
                return await response.json()

    async def register(
        self,
        username: str,
        password: str,
        password_confirmation: str,
        telegram_id: int
    ):
        data = {
            'username': username,
            'password': password,
            'password_confirmation': password_confirmation,
            'telegram_id': telegram_id
        }
        return await self._make_request('POST', '/users/register/', data=data)

    async def login(
        self,
        username: str,
        password: str
    ):
        data = {
            'username': username,
            'password': password
        }
        return await self._make_request('POST', '/users/login/', data=data)

    async def get_tasks(
        self,
        token: str
    ):
        return await self._make_request('GET', '/todo/tasks/', token=token)

    async def create_task(
        self,
        token: str,
        data: Dict
    ):
        return await self._make_request('POST', '/todo/tasks/', token=token, data=data)

    async def get_categories(
        self,
        token: str
    ):
        return await self._make_request('GET', '/todo/categories/', token=token)

    async def create_category(
        self,
        token: str,
        name: str,
    ):
        data = {
            'name': name,
        }
        return await self._make_request('POST', '/todo/categories/', token=token, data=data)


api_client = APIClient(os.getenv('DJANGO_API_URL', 'http://web:8000/api'))
