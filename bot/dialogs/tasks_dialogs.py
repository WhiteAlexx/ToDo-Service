from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Select, Button, Row, Back, Cancel
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format

from handlers.user_handlers import (
                                get_categories_data,
                                get_confirm_data,
                                get_tasks_data,
                                on_add_task,
                                on_category_selected,
                                on_confirm_task,
                                on_no_category,
                                on_view_tasks,
                                process_task_description,
                                process_task_due_date,
                                process_task_title
                            )
from states.task_states import TaskStates


tasks_dialog = Dialog(
    Window(
        Const('📋 Main task menu:'),
        Row(
            Button(Const('📝 To-do list'), id='view_tasks', on_click=on_view_tasks),
            Button(Const('➕ Add a task'), id='add_task', on_click=on_add_task),
        ),
        Cancel(Const('🚪 Exit')),
        state=TaskStates.main_menu,
    ),
    Window(
        Format('📋 Your tasks:\n\n{tasks}'),
        Back(Const('◀️ Back')),
        getter=get_tasks_data,
        state=TaskStates.view_tasks,
    ),
    Window(
        Const('Enter the task title:'),
        TextInput(
            id='title_input',
            on_success=process_task_title,
        ),
        Back(Const('◀️ Back')),
        state=TaskStates.add_task_title,
    ),
    Window(
        Const('Enter a description of the task (or type "-" to skip):'),
        TextInput(
            id='description_input',
            on_success=process_task_description,
        ),
        Back(Const('◀️ Back')),
        state=TaskStates.add_task_description,
    ),
    Window(
        Const('Select a category:'),
        Select(
        Format('{item[0]}'),
        id='s_category',
        item_id_getter=lambda item: item[1],
        items='categories',
        on_click=on_category_selected,
        ),
        Button(Const('❌ Uncategorized'), id='no_category', on_click=on_no_category),
        Back(Const('◀️ Back')),
        getter=get_categories_data,
        state=TaskStates.add_task_category,
    ),
    Window(
        Const('Enter the due date (in DD.MM.YYYY format or send "-" to skip):'),
        TextInput(
            id='due_date_input',
            on_success=process_task_due_date,
        ),
        Back(Const('◀️ Back')),
        state=TaskStates.add_task_due_date,
    ),
    Window(
        Format('Confirm task creation:\n\n'
               '📝 Title: {title}\n'
               '📄 Description: {description}\n'
               '📁 Category: {category}\n'
               '📅 Due Date {due_date}'),
        Button(Const('✅ Confirm'), id='confirm', on_click=on_confirm_task),
        Back(Const('◀️ Back')),
        getter=get_confirm_data,
        state=TaskStates.add_task_confirm,
    ),
)
