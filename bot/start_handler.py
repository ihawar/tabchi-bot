from aiogram import Router, F
from aiogram.types import (Message, CallbackQuery, ReplyKeyboardRemove)
from GLOBALS import CLIENT_ID
from bot import messages
from aiogram.fsm.context import FSMContext
from rich import print as r_print
from bot.utils import generate_main_menu
from database import AsyncDatabaseManager

start_router = Router()

@start_router.message(F.text == "/start")
async def handle_start(message: Message):
    if message.from_user.id != CLIENT_ID:
        r_print(f'[blue]Start from not admin user! ID: {message.from_user.id}[/blue]') 
        return
    r_print(f'[blue]New Start from admin![/blue]') 
    client = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    await message.answer(messages.BOT_START_COMMAND, reply_markup=generate_main_menu(client_is_online=client.is_online,
                                                                                     client_auto_join=client.auto_join))

@start_router.message(F.text == "🏠 بازگشت به منوی اصلی")
async def handle_return_to_main_menu_message(message: Message, state: FSMContext):
    if message.from_user.id != CLIENT_ID:
        return
    await state.clear()
    await message.answer('🏠', reply_markup=ReplyKeyboardRemove())
    await handle_start(message)

@start_router.callback_query(F.data== "return_to_main_menu")
async def handle_return_to_main_menu_callback(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    await state.clear()
    client = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    await callback_query.message.edit_text(messages.BOT_START_COMMAND,
                                           reply_markup=generate_main_menu(client_is_online=client.is_online,
                                                                            client_auto_join=client.auto_join))
