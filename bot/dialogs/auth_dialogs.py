from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Row, Back
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from states.auth_states import AuthStates

from handlers.user_handlers import (
                                on_registration_selected,
                                on_login_selected,
                                process_login_password,
                                process_login_username,
                                process_registration_confirm,
                                process_registration_password,
                                process_registration_username,
                            )


auth_dialog = Dialog(
    Window(
        Const('🔐 Select an action:'),
        Row(
            Button(Const('📝 Registration'), id='register', on_click=on_registration_selected),
            Button(Const('🔑 Log in'), id='login', on_click=on_login_selected),
        ),
        state=AuthStates.select_action,
    ),
    Window(
        Const('Enter your username:'),
        TextInput(
            id='username_input',
            on_success=process_registration_username,
        ),
        Back(Const('◀️ Back')),
        state=AuthStates.registration_username,
    ),
    Window(
        Const('Enter your password:'),
        TextInput(
            id='password_input',
            on_success=process_registration_password,
        ),
        Back(Const('◀️ Back')),
        state=AuthStates.registration_password,
    ),
    Window(
        Const('Confirm your password:'),
        TextInput(
            id='password_confirm_input',
            on_success=process_registration_confirm,
        ),
        Back(Const('◀️ Back')),
        state=AuthStates.registration_confirm,
    ),
    Window(
        Const('Enter your username:'),
        TextInput(
            id='login_username_input',
            on_success=process_login_username,
        ),
        Back(Const('◀️ Back')),
        state=AuthStates.login_username,
    ),
    Window(
        Const('Enter your password:'),
        TextInput(
            id='login_password_input',
            on_success=process_login_password,
        ),
        Back(Const('◀️ Back')),
        state=AuthStates.login_password,
    ),
)
