import asyncio
from GLOBALS import SAFE_MODE
from telethon import events
from client.tel_client import tel_client
from client import messages
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.contacts import AddContactRequest
from telethon import events, errors
from rich import print as r_print
from database import AsyncDatabaseManager, Group
from client.utils import join_chat
from client.tasks import auto_join_manager

@tel_client.on(events.NewMessage(pattern=r'^/w$', outgoing=True))
async def handle_start(event):
    await event.edit(messages.START_MESSAGE, parse_mode='html')

@tel_client.on(events.NewMessage(pattern=r'^/w new channel (.+)$', outgoing=True))
async def handle_new_channel(event):
    channel_address = event.pattern_match.group(1)
    channel = await join_chat(tel_client, channel_address)
    if channel:
        if channel.usernames:
            username = channel.usernames[-1].username
        elif hasattr(channel, 'username'):
            username = channel.username
        else:
            username = ''
        await AsyncDatabaseManager().create_link_storage_channel(
            channel_id=str(channel.id),
            channel_name=channel.title,
            channel_username=username)
        await event.edit(messages.JOIN_SUCCESS_MESSAGE)
    else:
        await event.edit(messages.JOIN_FAIL_MESSAGE)

@tel_client.on(events.NewMessage(pattern=r'^/w delete channel (.+)$', outgoing=True))
async def handle_leave_channel(event):
    channel_address = event.pattern_match.group(1)
    try:
        channel = await tel_client.get_entity(channel_address)
        await tel_client(LeaveChannelRequest(channel))
    except errors.UserPrivacyRestrictedError:
        await event.edit(messages.LEAVE_FAIL_MESSAGE)
        r_print("[red bold]Can't access this channel due to the user's privacy settings.[/red bold]")
    except errors.ChannelPrivateError:
        await event.edit(messages.LEAVE_FAIL_MESSAGE)
        r_print("[red bold]This is a private channel. Can't leave without being a member.[/red bold]")
    except Exception as e:
        await event.edit(messages.LEAVE_FAIL_MESSAGE)
        r_print(f"[red bold]An error occurred: {e}[/red bold]")
    else:
        # Assuming you have a method in your database manager to remove a channel
        await AsyncDatabaseManager().delete_link_storage_channel(channel_id=str(channel.id))

        r_print(f"[green bold]Successfully removed {channel.title} from the database.[/green bold]")
        await event.edit(messages.LEAVE_SUCCESS_MESSAGE)

@tel_client.on(events.NewMessage(pattern=r'^/w new group (.+)$', outgoing=True))
async def handle_new_group(event):
    group_address: str = event.pattern_match.group(1)
    group = await join_chat(tel_client, group_address)
    if group:
        if group.usernames:
            username = group.usernames[-1].username
        elif hasattr(group, 'username'):
            username = group.username
        else:
            username = ''
        await AsyncDatabaseManager().create_group(
            group_id=str(group.id),
            group_name=group.title,
            group_username=username)
        await event.edit(messages.JOIN_SUCCESS_MESSAGE)
    else:
        await event.edit(messages.JOIN_FAIL_MESSAGE)

@tel_client.on(events.NewMessage(pattern=r'^/w delete group (.+)$', outgoing=True))
async def handle_delete_group(event):
    group_address = event.pattern_match.group(1)
    try:
        group = await tel_client.get_entity(group_address)
        await tel_client(LeaveChannelRequest(group))
    except errors.UserPrivacyRestrictedError:
        await event.edit(messages.LEAVE_FAIL_MESSAGE)
        r_print("[red bold]Can't access this group due to the user's privacy settings.[/red bold]")
    except errors.ChannelPrivateError:
        await event.edit(messages.LEAVE_FAIL_MESSAGE)
        r_print("[red bold]This is a private group. Can't leave without being a member.[/red bold]")
    except Exception as e:
        await event.edit(messages.LEAVE_FAIL_MESSAGE)
        r_print(f"[red bold]An error occurred: {e}[/red bold]")
    else:
        # Assuming you have a similar method for groups in your AsyncDatabaseManager
        await AsyncDatabaseManager().delete_group(group_id=str(group.id))

        r_print(f"[green bold]Successfully removed {group.title} from the database.[/green bold]")
        await event.edit(messages.LEAVE_SUCCESS_MESSAGE)

@tel_client.on(events.NewMessage(pattern=r'^/w alert (.+)$', outgoing=True, func=lambda e: e.is_private))
async def handle_alert(event):
    message = event.pattern_match.group(1)
    await event.edit('🔄️ درحال ارسال...')
    groups = await AsyncDatabaseManager().get_all_groups()
    counter = 0
    for group in groups:
        try:
            if SAFE_MODE['active']: await asyncio.sleep(SAFE_MODE['sleep'])
            await tel_client.send_message(int(group.group_id), message)
            await AsyncDatabaseManager().update_group(group_id=group.group_id, sent_banners=Group.sent_banners + 1)
        except errors.FloodWaitError as e:
            r_print(f"[red bold]FloodWaitError: Try again after {e.seconds} seconds for group {group.group_name}[/red bold]")
            continue
        except errors.UserPrivacyRestrictedError:
            r_print(f"[red bold]UserPrivacyRestrictedError: Cannot send message due to privacy settings in {group.group_name}[/red bold]")
            continue
        except errors.ChannelPrivateError:
            r_print(f"[red bold]ChannelPrivateError: Cannot access private group {group.group_name} without an invite.[/red bold]")
            continue
        except Exception as e:
            r_print(f"[red bold]Unexpected error occurred while sending alert to {group.group_name}: {str(e)}[/red bold]")
            continue
        else:
            r_print(f"[red green]Successfully sent alert to {group.group_name}[/red green]")
            counter += 1

    await event.edit(messages.SENT_ALERTS.format(count=counter))

@tel_client.on(events.NewMessage(pattern=r'^/w auto join$', outgoing=True))
async def handle_auto_join(event):
    await event.edit('🔄️ درحال ارسال...')
    await auto_join_manager()
    await event.edit("✅ Done.")

@tel_client.on(events.NewMessage(incoming=True))
async def handle_private_incoming(event):
    user = await event.get_sender()
    if event.is_private:
        user = await event.get_sender()
        if not user.bot: 
            auto_secs = await AsyncDatabaseManager().get_all_message_secs()
            auto_sec = auto_secs[-1]
            if not auto_sec.is_active: return
            await event.reply(auto_sec.response)
            # Add to contact
            await tel_client(AddContactRequest(id=user.id, first_name=user.first_name or 'None', last_name=user.last_name or 'None', phone=user.phone if user.phone else ''))
            
            await AsyncDatabaseManager().increase_message_sec_pv_count(id=auto_sec.id)
