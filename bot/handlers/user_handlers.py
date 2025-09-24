from datetime import date

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.input import TextInput

from database.redis_cli import redis_client
from filters.chat_types import ChatTypeFilter
from states.auth_states import AuthStates
from states.task_states import TaskStates
from utils.api_client import api_client, APIError


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_command(message: Message, dialog_manager: DialogManager):

    token = redis_client.get(f"user_token:{message.from_user.id}")

    if token:
        await message.answer('Welcome to your ToDo List! Use the menu to manage your tasks.')
        await dialog_manager.start(TaskStates.main_menu, mode=StartMode.RESET_STACK)
    else:
        await message.answer('Welcome! You need to log in to get started.')
        await dialog_manager.start(AuthStates.select_action, mode=StartMode.RESET_STACK)


async def on_registration_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    await dialog_manager.switch_to(AuthStates.registration_username)


async def on_login_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    await dialog_manager.switch_to(AuthStates.login_username)


async def process_registration_username(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):

    dialog_manager.dialog_data['username'] = text
    await dialog_manager.next()


async def process_registration_password(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):

    dialog_manager.dialog_data['password'] = text
    await dialog_manager.next()


async def process_registration_confirm(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):

    dialog_manager.dialog_data['password_confirmation'] = text

    try:
        result = await api_client.register(
            username=dialog_manager.dialog_data['username'],
            password=dialog_manager.dialog_data['password'],
            password_confirmation=dialog_manager.dialog_data['password_confirmation'],
            telegram_id=dialog_manager.event.from_user.id
        )

        redis_client.set(f"user_token:{dialog_manager.event.from_user.id}", result['token'])
        await message.answer('✅ Registration is successful! Now you can manage your tasks.')
        await dialog_manager.start(TaskStates.main_menu, mode=StartMode.RESET_STACK)

    except APIError as e:
        await message.answer(f"❌ Registration error: {str(e)}")
        await dialog_manager.start(AuthStates.select_action, mode=StartMode.RESET_STACK)


async def process_login_username(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):

    dialog_manager.dialog_data['username'] = text
    await dialog_manager.next()


async def process_login_password(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):

    username = dialog_manager.dialog_data['username']
    password = text

    try:
        result = await api_client.login(username, password)

        redis_client.set(f"user_token:{dialog_manager.event.from_user.id}", result['token'])
        await message.answer('✅ Login successful!')
        await dialog_manager.start(TaskStates.main_menu, mode=StartMode.RESET_STACK)

    except APIError as e:
        await message.answer(f"❌ Login error: {str(e)}")
        await dialog_manager.start(AuthStates.select_action, mode=StartMode.RESET_STACK)


############################################ T A S K S ############################################
async def get_tasks_data(dialog_manager: DialogManager, **kwargs):

    token = redis_client.get(f"user_token:{dialog_manager.event.from_user.id}")

    try:
        tasks = await api_client.get_tasks(token)
        if tasks:
            tasks_text = ''
            for task in tasks:
                created_at = task.get('created_at')
                if 'T' in created_at:
                    created_at = created_at.split('T')[0]
                tasks_text += f"📌 {task['title']}\n"
                tasks_text += f"   📅 Created: {created_at}\n"
                if task.get('category'):
                    tasks_text += f"   📁 Category: {task['category_name']}\n"
                tasks_text += f"   📄 Description: {task['description']}\n"
                tasks_text += f"   ✅ Status: {'Completed' if task['completed'] else 'Active'}\n\n"
            return {'tasks': tasks_text}
        else:
            return {'tasks': "You don't have any tasks yet.."}
    except APIError as e:
        await dialog_manager.event.answer(f"❌ Error loading tasks: {str(e)}")
        return {'tasks': []}


async def get_categories_data(dialog_manager: DialogManager, **kwargs):

    token = redis_client.get(f"user_token:{dialog_manager.event.from_user.id}")

    try:
        categories = await api_client.get_categories(token)
        dialog_manager.dialog_data['categories'] = categories or []
        category_items = []
        if categories:
            for category in categories:
                category_items.append((category['name'], int(category['id'])))
        return {'categories': category_items}
    except APIError as e:
        await dialog_manager.event.answer(f"❌ Error loading categories: {str(e)}")
        return {'categories': []}


async def get_confirm_data(dialog_manager: DialogManager, **kwargs):

    title = dialog_manager.dialog_data.get('title')
    description = dialog_manager.dialog_data.get('description')
    category_id = dialog_manager.dialog_data.get('category_id')
    due_date = dialog_manager.dialog_data.get('due_date')

    return {
        'title': title,
        'description': description if description != '-' else '',
        'category': category_id,
        'due_date': due_date,
    }


async def on_view_tasks(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    await dialog_manager.switch_to(TaskStates.view_tasks)


async def on_add_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    await dialog_manager.switch_to(TaskStates.add_task_title)


async def process_task_title(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):

    dialog_manager.dialog_data['title'] = text
    await dialog_manager.next()


async def process_task_description(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):

    dialog_manager.dialog_data['description'] = text
    await dialog_manager.next()


async def process_task_due_date(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):

    due_date_text = text
    if due_date_text != '-':
        try:
            day, month, year = map(int, due_date_text.split('.'))
            due_date = date(year, month, day)

            if due_date < date.today():
                await message.answer('❌ The date cannot be in the past! Please enter a valid date.')
                return

            dialog_manager.dialog_data['due_date'] = due_date.isoformat()
        except (ValueError, AttributeError):
            await message.answer('❌ Invalid date format! Use DD.MM.YYYY')
            return
    else:
        dialog_manager.dialog_data['due_date'] = None

    await dialog_manager.next()


async def on_category_selected(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):

    dialog_manager.dialog_data['category_id'] = int(item_id)
    await dialog_manager.next()


async def on_no_category(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    dialog_manager.dialog_data['category_id'] = None
    await dialog_manager.next()


async def on_confirm_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    token = redis_client.get(f"user_token:{dialog_manager.event.from_user.id}")

    try:
        data = {
            'title': dialog_manager.dialog_data['title'],
            'description': dialog_manager.dialog_data.get('description', ''),
            'category': dialog_manager.dialog_data.get('category_id'),
            'due_date': dialog_manager.dialog_data.get('due_date')}
        await api_client.create_task(token, data)
        await callback.message.answer('✅ The task was created successfully!')
        await dialog_manager.start(TaskStates.main_menu, mode=StartMode.RESET_STACK)
    except APIError as e:
        await callback.message.answer(f"❌ Error creating task: {str(e)}")
        await dialog_manager.start(TaskStates.main_menu, mode=StartMode.RESET_STACK)
