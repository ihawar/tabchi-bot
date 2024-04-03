from aiogram import Router, F
from aiogram.utils import formatting
from aiogram.types import (CallbackQuery,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton,
                            Message,
                            ReplyKeyboardRemove)
from GLOBALS import CLIENT_ID
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from rich import print as r_print
from bot.utils import generate_return_to_main_menu_markup
from database import AsyncDatabaseManager
from bot import messages

manage_bot_router = Router()
class UpdateSendEveryMinState(StatesGroup):
    new_every_mins = State()

@manage_bot_router.callback_query(F.data == "manage_bot")
async def manage_bot_menu(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    user = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    report_text = messages.BOT_OPTIONS_REPORTS.format(
        cliend_id=formatting.Code(user.client_id).as_html(),
        client_username=formatting.TextMention(user.client_username, user=callback_query.from_user).as_html(),
        client_full_name=user.client_full_name,
        online_status=messages.ON_EMOJI if user.is_online else messages.OFF_EMOJI,
        auto_join_status=messages.ON_EMOJI if user.auto_join else messages.OFF_EMOJI,
        every_mins=user.send_every_mins)
    
    await callback_query.message.edit_text(report_text, 
                                           reply_markup=generate_manage_bot_menu())

@manage_bot_router.callback_query(F.data == "update_bot_send_every_mins")
async def update_bot_every_mins(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    await state.set_state(UpdateSendEveryMinState.new_every_mins)
    await callback_query.message.delete()
    await callback_query.message.answer(messages.UPDATE_EVERY_MINS_TEXT, 
                                           reply_markup=generate_return_to_main_menu_markup())

@manage_bot_router.message(UpdateSendEveryMinState.new_every_mins, F.text)
async def update_bot_every_mins(message: Message, state: FSMContext):
    if message.from_user.id != CLIENT_ID:
        r_print(f'[blue]New update_bot_every_mins from not admin user! ID: {message.from_user.id}[/blue]') 
        return
    r_print(f'[blue]New update_bot_every_mins from admin![/blue]')
    if not message.text.isdigit():
        await message.reply('Invalid! Enter a number!!!')
        return
    await state.clear()
    await AsyncDatabaseManager().update_client(client_id=CLIENT_ID, send_every_mins=int(message.text))
    
    user = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    report_text = messages.BOT_OPTIONS_REPORTS.format(
        cliend_id=formatting.Code(user.client_id).as_html(),
        client_username=formatting.TextMention(user.client_username, user=message.from_user).as_html(),
        client_full_name=user.client_full_name,
        online_status=messages.ON_EMOJI if user.is_online else messages.OFF_EMOJI,
        auto_join_status=messages.ON_EMOJI if user.auto_join else messages.OFF_EMOJI,
        every_mins=user.send_every_mins)
    
    await message.answer(messages.UPDATED, reply_markup=ReplyKeyboardRemove())
    await message.answer(report_text, reply_markup=generate_manage_bot_menu())


def generate_manage_bot_menu():
    buttons = []
     # Add developer button
    buttons.append([InlineKeyboardButton(text=messages.DEVELOPER_BUTTON[0], url=messages.DEVELOPER_BUTTON[1])])
    # Add main options
    menu_buttons = messages.MANAGE_BOT_OPTIONS
    while len(menu_buttons) != 0:
        buttons.append([
            InlineKeyboardButton(text=button[0], callback_data=button[1]) for button in menu_buttons[0:2]])
        menu_buttons = menu_buttons[2:]

    # Add return home button
    buttons.append([InlineKeyboardButton(text=messages.RETURN_HOME_OPTION[0], callback_data=messages.RETURN_HOME_OPTION[1])])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
