from aiogram import Router, F
from aiogram.types import (CallbackQuery,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.utils import formatting
from GLOBALS import CLIENT_ID
from rich import print as r_print
from database import AsyncDatabaseManager, LinkStorageChannels
from bot import messages

manage_link_channels_router = Router()

@manage_link_channels_router.callback_query(F.data.startswith("manage_link_storages::"))
async def handle_manage_link_channels(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    page = int(callback_query.data.split('::')[-1]) - 1
    all_channels = await AsyncDatabaseManager().get_all_link_storage_channels()
    channels = all_channels[0 + (page * 20):20+ (page * 20)]
    if page != 0 and len(channels) == 0:
        await callback_query.answer('Nothing available!!!')
        return
    report = messages.MANAGE_ALL_LINK_CHANNELS_REPORT.format(
        channel_count=len(all_channels)
    )
    await callback_query.answer('✅')
    await callback_query.message.edit_text(report, reply_markup=generate_manage_all_link_channels(channels, page+1))

@manage_link_channels_router.callback_query(F.data.startswith("manage_link_channel::"))
async def handle_manage_channel(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')

    channel_id = callback_query.data.split('::')[-1]
    channel = await AsyncDatabaseManager().get_link_storage_channel(id=int(channel_id))
    if not channel:
        await callback_query.message.delete()
        await callback_query.answer(messages.ERROR_MESSAGE)
        await handle_manage_link_channels(callback_query)
        return
    report = messages.MANAGE_LINK_CHANNEL_REPORT.format(
        channel_id=formatting.Code(channel.channel_id).as_html(),
        channel_username=channel.channel_username,
        channel_name=channel.channel_name)
    
    await callback_query.message.edit_text(report, reply_markup=generate_manage_channel_keyboard(channel))  

@manage_link_channels_router.callback_query(F.data.startswith("delete_link_channel::"))
async def handle_delete_channel(callback_query: CallbackQuery):
    if callback_query.from_user.id != CLIENT_ID:
        r_print(f'[blue]Callback {callback_query.data} from not admin account! ID: {callback_query.from_user.id}[/blue]') 
        return
    r_print(f'[blue]Callback {callback_query.data} form admin![/blue]')
    channel_id = callback_query.data.split('::')[-1]
    await AsyncDatabaseManager().delete_link_storage_channel(id=channel_id)
    await callback_query.answer('Deleted!')
    await handle_manage_link_channels(callback_query)

def generate_manage_channel_keyboard(channel: LinkStorageChannels):
    buttons = []
     # Add developer button
    buttons.append([InlineKeyboardButton(text=messages.DEVELOPER_BUTTON[0], url=messages.DEVELOPER_BUTTON[1])])
    # Add delete option
    buttons.append([InlineKeyboardButton(text=messages.DELETE_LINK_CHANNEL_OPTION[0], callback_data=messages.DELETE_LINK_CHANNEL_OPTION[1].format(id=channel.id))])
    # Add return home button
    buttons.append([InlineKeyboardButton(text=messages.RETURN_HOME_OPTION[0], callback_data=messages.RETURN_HOME_OPTION[1])])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def generate_manage_all_link_channels(channels: list[LinkStorageChannels], page: int):
    buttons = []
     # Add developer button
    buttons.append([InlineKeyboardButton(text=messages.DEVELOPER_BUTTON[0], url=messages.DEVELOPER_BUTTON[1])])
    # Add main options
    all_channels = channels
    while len(all_channels) != 0:
        buttons.append([
            InlineKeyboardButton(text=f'🔹 {channel.channel_name}', callback_data=f'manage_link_channel::{channel.id}') for channel in all_channels[0:2]])
        all_channels = all_channels[2:]
    # Add return home button
    buttons.append([InlineKeyboardButton(text=messages.RETURN_HOME_OPTION[0], callback_data=messages.RETURN_HOME_OPTION[1])])
    # Add page buttons
    buttons.append([
        InlineKeyboardButton(text=messages.CHANNELS_LINK_PER_PAGE_BUTTON[0], callback_data=messages.CHANNELS_LINK_PER_PAGE_BUTTON[1].format(page=1 if page == 1 else page - 1)),
        InlineKeyboardButton(text=messages.CHANNELS_LINK_NEXT_PAGE_BUTTON[0], callback_data=messages.CHANNELS_LINK_NEXT_PAGE_BUTTON[1].format(page=page + 1))
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

