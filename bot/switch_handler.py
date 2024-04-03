from aiogram import Router, F
from aiogram.types import CallbackQuery
from GLOBALS import CLIENT_ID
from rich import print as r_print
from database import AsyncDatabaseManager
from bot.start_handler import generate_main_menu

switches_router = Router()

@switches_router.callback_query(F.data == "switch_bot_status")
async def bot_status_switch(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]') 
    user = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    await AsyncDatabaseManager().update_client(client_id=CLIENT_ID, is_online=not user.is_online)
    updated_user = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    await callback_query.message.edit_reply_markup(reply_markup=generate_main_menu(client_auto_join=updated_user.auto_join,
                                                                                   client_is_online=updated_user.is_online))
    

@switches_router.callback_query(F.data == "switch_auto_join_status")
async def auto_join_status_switch(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]') 
    user = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    await AsyncDatabaseManager().update_client(client_id=CLIENT_ID, auto_join=not user.auto_join)
    updated_user = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    await callback_query.message.edit_reply_markup(reply_markup=generate_main_menu(client_auto_join=updated_user.auto_join,
                                                                                   client_is_online=updated_user.is_online))
    