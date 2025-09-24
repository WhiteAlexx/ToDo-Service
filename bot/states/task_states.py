from aiogram.fsm.state import State, StatesGroup


class TaskStates(StatesGroup):

    main_menu = State()
    view_tasks = State()
    add_task_title = State()
    add_task_description = State()
    add_task_category = State()
    add_task_due_date = State()
    add_task_confirm = State()
