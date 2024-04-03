from aiogram import Router, F
from aiogram.types import (CallbackQuery,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.utils import formatting
from GLOBALS import CLIENT_ID
from rich import print as r_print
from database import AsyncDatabaseManager, Group
from bot import messages

manage_groups_router = Router()

@manage_groups_router.callback_query(F.data.startswith("manage_groups::"))
async def handle_manage_groups(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    page = int(callback_query.data.split('::')[-1]) - 1
    all_groups = await AsyncDatabaseManager().get_all_groups()
    groups = all_groups[0 + (page * 20):20+ (page * 20)]
    if page != 0 and len(groups) == 0:
        await callback_query.answer('Nothing available!!!')
        return
    report = messages.MANAGE_ALL_LINK_GROUPS_REPORT.format(
        groups_count=len(all_groups)
    )
    await callback_query.answer('✅')
    await callback_query.message.edit_text(report, reply_markup=generate_manage_all_groups(groups, page+1))

@manage_groups_router.callback_query(F.data.startswith("manage_group::"))
async def handle_manage_group(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')

    group_id = callback_query.data.split('::')[-1]
    group = await AsyncDatabaseManager().get_group(id=int(group_id))
    if not group:
        await callback_query.message.delete()
        await callback_query.answer(messages.ERROR_MESSAGE)
        await handle_manage_groups(callback_query)
        return
    report = messages.MANAGE_GROUP_REPORT.format(
        group_id=formatting.Code(group.group_id).as_html(),
        group_username=group.group_username,
        group_name=group.group_name,
        group_count_sent_banners=group.sent_banners)
    
    await callback_query.message.edit_text(report, reply_markup=generate_manage_group_keyboard(group))  

@manage_groups_router.callback_query(F.data.startswith("delete_group::"))
async def handle_delete_group(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    group_id = callback_query.data.split('::')[-1]
    await AsyncDatabaseManager().delete_group(id=group_id)
    await callback_query.answer('Deleted!')
    await handle_manage_groups(callback_query)

def generate_manage_group_keyboard(group: Group):
    buttons = []
     # Add developer button
    buttons.append([InlineKeyboardButton(text=messages.DEVELOPER_BUTTON[0], url=messages.DEVELOPER_BUTTON[1])])
    # Add delete option
    buttons.append([InlineKeyboardButton(text=messages.DELETE_GROUP_OPTION[0], callback_data=messages.DELETE_GROUP_OPTION[1].format(id=group.id))])
    # Add return home button
    buttons.append([InlineKeyboardButton(text=messages.RETURN_HOME_OPTION[0], callback_data=messages.RETURN_HOME_OPTION[1])])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def generate_manage_all_groups(groups: list[Group], page: int):
    buttons = []
     # Add developer button
    buttons.append([InlineKeyboardButton(text=messages.DEVELOPER_BUTTON[0], url=messages.DEVELOPER_BUTTON[1])])
    # Add main options
    all_groups = groups
    while len(all_groups) != 0:
        buttons.append([
            InlineKeyboardButton(text=f'🔹 {group.group_name}', callback_data=f'manage_group::{group.id}') for group in all_groups[0:2]])
        all_groups = all_groups[2:]
    # Add return home button
    buttons.append([InlineKeyboardButton(text=messages.RETURN_HOME_OPTION[0], callback_data=messages.RETURN_HOME_OPTION[1])])
    # Add page buttons
    buttons.append([
        InlineKeyboardButton(text=messages.GROUPS__PER_PAGE_BUTTON[0], callback_data=messages.GROUPS__PER_PAGE_BUTTON[1].format(page=1 if page == 1 else page - 1)),
        InlineKeyboardButton(text=messages.GROUPS_NEXT_PAGE_BUTTON[0], callback_data=messages.GROUPS_NEXT_PAGE_BUTTON[1].format(page=page + 1))
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

