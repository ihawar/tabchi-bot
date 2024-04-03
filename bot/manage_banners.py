from aiogram import Router, F
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
from database import AsyncDatabaseManager, Banner
from bot import messages

manage_banners_router = Router()
class CreateBannerState(StatesGroup):
    banner_title = State()
    banner_content = State()

@manage_banners_router.callback_query(F.data == "manage_banners")
async def handle_manage_banners(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    banners = await AsyncDatabaseManager().get_all_banners()
    count_sent_banners = sum([banner.sent_count for banner in banners])

    report = messages.MANAGE_ALL_BANNERS_REPORT.format(
        count_banners=len(banners),
        count_all_sent_banners=count_sent_banners)
    await callback_query.message.edit_text(report, 
                                           reply_markup=generate_manage_all_banners_keyboard(banners))

@manage_banners_router.callback_query(F.data == "create_new_banner")
async def create_new_banner(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    await state.set_state(CreateBannerState.banner_title)
    await callback_query.message.delete()
    await callback_query.message.answer(messages.CREATE_BANNER_TITLE_INPUT,
                                reply_markup=generate_return_to_main_menu_markup())

@manage_banners_router.message(CreateBannerState.banner_title, F.text)
async def handle_title_input(message: Message, state: FSMContext):
    if message.from_user.id != CLIENT_ID:
        r_print(f'[blue]New handle_title_input  from not admin user! ID: {message.from_user.id}[/blue]') 
        return
    r_print(f'[blue]New handle_title_input from admin![/blue]')
    await state.update_data(banner_title=message.text)
    await state.set_state(CreateBannerState.banner_content)
    await message.answer(messages.CREAT_BANNER_CONTENT_INPUT,
                        reply_markup=generate_return_to_main_menu_markup())

@manage_banners_router.message(CreateBannerState.banner_content, F.text)
async def handle_content_input(message: Message, state: FSMContext):
    if message.from_user.id != CLIENT_ID:
        r_print(f'[blue]New handle_content_input  from not admin user! ID: {message.from_user.id}[/blue]') 
        return
    r_print(f'[blue]New handle_content_input from admin![/blue]')
    data = await state.update_data(banner_content=message.text)
    await AsyncDatabaseManager().create_banner(title=data['banner_title'], text=data['banner_content'])
    await state.clear()
    await message.answer(messages.UPDATED, reply_markup=ReplyKeyboardRemove())

    banners = await AsyncDatabaseManager().get_all_banners()
    count_sent_banners = sum([banner.sent_count for banner in banners])
    report = messages.MANAGE_ALL_BANNERS_REPORT.format(
        count_banners=len(banners),
        count_all_sent_banners=count_sent_banners)
    await message.answer(report, reply_markup=generate_manage_all_banners_keyboard(banners)) 

@manage_banners_router.callback_query(F.data.startswith("manage_banner::"))
async def handle_manage_banner(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    banner_id = callback_query.data.split('::')[-1]
    banner = await AsyncDatabaseManager().get_banner(id=int(banner_id))
    if not banner:
        await callback_query.message.delete()
        await callback_query.answer(messages.ERROR_MESSAGE)
        await handle_manage_banners(callback_query)
        return
    report = messages.MANAGE_BANNER_REPORT.format(
        banner_title=banner.title,
        banner_text=banner.text,
        sent_count=banner.sent_count)
    await callback_query.message.edit_text(report, reply_markup=generate_manage_banner_keyboard(banner))  

@manage_banners_router.callback_query(F.data.startswith("delete_banner::"))
async def handle_delete_banner(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    banner_id = callback_query.data.split('::')[-1]
    await AsyncDatabaseManager().delete_banner(id=int(banner_id))
    await callback_query.answer('Deleted!')
    await handle_manage_banners(callback_query)

def generate_manage_banner_keyboard(banner: Banner):
    buttons = []
     # Add developer button
    buttons.append([InlineKeyboardButton(text=messages.DEVELOPER_BUTTON[0], url=messages.DEVELOPER_BUTTON[1])])
    # Add delete option
    buttons.append([InlineKeyboardButton(text=messages.DELETE_BANNER_OPTION[0], callback_data=messages.DELETE_BANNER_OPTION[1].format(banner_id=banner.id))])
    # Add return home button
    buttons.append([InlineKeyboardButton(text=messages.RETURN_HOME_OPTION[0], callback_data=messages.RETURN_HOME_OPTION[1])])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def generate_manage_all_banners_keyboard(banners: list[Banner]):
    buttons = []
     # Add developer button
    buttons.append([InlineKeyboardButton(text=messages.DEVELOPER_BUTTON[0], url=messages.DEVELOPER_BUTTON[1])])
    # Add main options
    all_banners = banners
    while len(all_banners) != 0:
        buttons.append([
            InlineKeyboardButton(text=f'🔹 {banner.title}', callback_data=f'manage_banner::{banner.id}') for banner in all_banners[0:2]])
        all_banners = all_banners[2:]
    # Add new banner button
    buttons.append([InlineKeyboardButton(text=messages.ADD_NEW_BANNER_BUTTON[0], callback_data=messages.ADD_NEW_BANNER_BUTTON[1])])
    # Add return home button
    buttons.append([InlineKeyboardButton(text=messages.RETURN_HOME_OPTION[0], callback_data=messages.RETURN_HOME_OPTION[1])])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
