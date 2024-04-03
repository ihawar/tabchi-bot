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

auto_sec_router = Router()
class AutoSecUpdateState(StatesGroup):
    update_message = State()

@auto_sec_router.callback_query(F.data == "manage_message_sec")
async def manage_auto_sec_manage_handler(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    auto_secs = await AsyncDatabaseManager().get_all_message_secs()
    auto_sec = auto_secs[-1]

    report_message = messages.AUTO_SEC_REPORT.format(
        count_message_secs=1,
        response_text=formatting.Code(auto_sec.response).as_html(),
        pv_count=auto_sec.pv_count
    )
    await callback_query.message.edit_text(report_message, reply_markup=generate_manage_auto_sec_keyboard(auto_sec.is_active))

@auto_sec_router.callback_query(F.data == "change_auto_message")
async def handle_change_auto_message(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    await state.set_state(AutoSecUpdateState.update_message)
    await callback_query.message.delete()
    await callback_query.message.answer(messages.UPDATE_MESSAGE_SEC_TEXT, 
                                        reply_markup=generate_return_to_main_menu_markup())

@auto_sec_router.message(AutoSecUpdateState.update_message, F.text)
async def update_auto_sec_message(message: Message, state: FSMContext):
    if message.from_user.id != CLIENT_ID:
        r_print(f'[blue]New update_auto_sec_message  from not admin user! ID: {message.from_user.id}[/blue]') 
        return
    r_print(f'[blue]New update_auto_sec_message from admin![/blue]')
    await state.clear()
    auto_secs = await AsyncDatabaseManager().get_all_message_secs()
    auto_sec = auto_secs[-1]
    await AsyncDatabaseManager().update_message_sec(id=auto_sec.id, response=message.text)
    auto_sec = await AsyncDatabaseManager().get_message_sec(id=auto_sec.id)
    report_message = messages.AUTO_SEC_REPORT.format(
        count_message_secs=1,
        response_text=formatting.Code(auto_sec.response).as_html(),
        pv_count=auto_sec.pv_count
    )
    await message.answer(messages.UPDATED, reply_markup=ReplyKeyboardRemove())
    await message.answer(report_message, reply_markup=generate_manage_auto_sec_keyboard(auto_sec.is_active))

@auto_sec_router.callback_query(F.data == "switch_auto_sec_status")
async def switch_auto_sec_status(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    auto_secs = await AsyncDatabaseManager().get_all_message_secs()
    auto_sec = auto_secs[-1]
    await AsyncDatabaseManager().update_message_sec(id=auto_sec.id, is_active=not auto_sec.is_active)
    auto_secs = await AsyncDatabaseManager().get_all_message_secs()
    auto_sec = auto_secs[-1]
    report_message = messages.AUTO_SEC_REPORT.format(
        count_message_secs=1,
        response_text=formatting.Code(auto_sec.response).as_html(),
        pv_count=auto_sec.pv_count
    )
    await callback_query.message.edit_text(report_message, reply_markup=generate_manage_auto_sec_keyboard(auto_sec.is_active))

def generate_manage_auto_sec_keyboard(is_active: bool):
    buttons = []
     # Add developer button
    buttons.append([InlineKeyboardButton(text=messages.DEVELOPER_BUTTON[0], url=messages.DEVELOPER_BUTTON[1])])
    # Add main options
    menu_buttons = messages.AUTO_SEC_OPTIONS
    while len(menu_buttons) != 0:
        buttons.append([
            InlineKeyboardButton(text=button[0], callback_data=button[1]) for button in menu_buttons[0:2]])
        menu_buttons = menu_buttons[2:]
    # Add switcher button
    buttons.append([InlineKeyboardButton(text=f'{messages.ON_EMOJI if is_active else messages.OFF_EMOJI} {messages.AUTO_SEC_STATUS_SWITCH[0]}', callback_data=messages.AUTO_SEC_STATUS_SWITCH[1])])
    # Add return home button
    buttons.append([InlineKeyboardButton(text=messages.RETURN_HOME_OPTION[0], callback_data=messages.RETURN_HOME_OPTION[1])])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
