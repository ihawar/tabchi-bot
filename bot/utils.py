from bot import messages
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButton)

def generate_main_menu(client_is_online: bool, client_auto_join: bool):
    buttons = []
    # Add bot info button
    buttons.append([InlineKeyboardButton(text=messages.BOT_STATUS_OPTION[0], callback_data=messages.BOT_STATUS_OPTION[1])])
    # Add main options
    menu_buttons = messages.MAIN_MENU_OPTIONS
    while len(menu_buttons) != 0:
        buttons.append([
            InlineKeyboardButton(text=button[0], callback_data=button[1]) for button in menu_buttons[0:2]])
        menu_buttons = menu_buttons[2:]
    # Add switches
    buttons.append(
        [InlineKeyboardButton(text=f'{messages.ON_EMOJI if client_is_online else messages.OFF_EMOJI} {messages.BOT_STATUS_SWITCH[0]}', callback_data=messages.BOT_STATUS_SWITCH[1]), 
        InlineKeyboardButton(text=f'{messages.ON_EMOJI if client_auto_join else messages.OFF_EMOJI} {messages.AUTO_JOIN_SWITCH[0]}', callback_data=messages.AUTO_JOIN_SWITCH[1])
        ])

    # Add developer button
    buttons.append([InlineKeyboardButton(text=messages.DEVELOPER_BUTTON[0], url=messages.DEVELOPER_BUTTON[1])])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def generate_return_to_main_menu_markup():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=messages.RETURN_HOME_KEYBOARD)]],resize_keyboard=True)
