from aiogram.fsm.state import State, StatesGroup


class AuthStates(StatesGroup):

    select_action = State()
    registration_username = State()
    registration_password = State()
    registration_confirm = State()
    login_username = State()
    login_password = State()
