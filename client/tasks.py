from telethon.errors import ChannelPrivateError, ChatWriteForbiddenError, FloodWaitError, UserPrivacyRestrictedError
from rich import print as r_print
from client.utils import join_chat
from database import AsyncDatabaseManager, Group
from client.tel_client import tel_client
import re
import asyncio
from GLOBALS import CLIENT_ID, SAFE_MODE
import random
from datetime import datetime

async def auto_join_manager():
    client = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    if client.auto_join:
        r_print('[bold blue]Starting the auto join process.[/bold blue]')
        links = await fetch_all_channels()
        await join_group_links(links)
        r_print('[bold blue]Ended the auto join process.[/bold blue]')

async def send_banners_manager():
    client = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    now = datetime.now(client.last_sent.tzinfo)
    minutes_ago = round(((now - client.last_sent).total_seconds() / 60))
    if minutes_ago > client.send_every_mins:
        await AsyncDatabaseManager().update_client(client_id=client.client_id, last_sent=now)
        r_print('[bold blue]Banner sending started...[/bold blue]')
        count = await send_banners()
        r_print(f'[green bold]{count} banners were sent!')  
 
async def send_banners():
    groups = await AsyncDatabaseManager().get_all_groups()
    banners = await AsyncDatabaseManager().get_all_banners()
    counter = 0
    for group in groups:
        if SAFE_MODE['active']: await asyncio.sleep(SAFE_MODE['sleep'])
        banner = random.choice(banners)
        try:
            await tel_client.send_message(int(group.group_id), banner.text)
        except FloodWaitError as e:
            r_print(f"[red bold]FloodWaitError: Try again after {e.seconds} seconds for group {group.group_name}[/red bold]")
            continue
        except UserPrivacyRestrictedError:
            r_print(f"[red bold]UserPrivacyRestrictedError: Cannot send message due to privacy settings in {group.group_name}[/red bold]")
            continue
        except ChannelPrivateError:
            r_print(f"[red bold]ChannelPrivateError: Cannot access private group {group.group_name} without an invite.[/red bold]")
            continue
        except Exception as e:
            r_print(f"[red bold]Unexpected error occurred while sending banner to {group.group_name}: {str(e)}[/red bold]")
            continue
        else:
            r_print(f"[red green]Successfully sent banner to {group.group_name}[/red green]")
            await AsyncDatabaseManager().increase_banner_sent_count(id=banner.id)
            await AsyncDatabaseManager().update_group(group_id=group.group_id, sent_banners=Group.sent_banners + 1)
            counter += 1
    return counter

async def fetch_all_channels():
    channels = await AsyncDatabaseManager().get_all_link_storage_channels()
    links = []

    link_pattern = re.compile(r'(https?://)?(www\.)?(t\.me|telegram\.me)/([^\s]+)')

    for channel in channels:
        if SAFE_MODE['active']: await asyncio.sleep(SAFE_MODE['sleep'])
        try:
            async for message in tel_client.iter_messages(int(channel.channel_id), limit=5):
                found_links = link_pattern.findall(message.text or "")
                for link_tuple in found_links:
                        # Decompose the tuple
                        scheme, www, domain, path = link_tuple
                        # Ensure the scheme is present
                        if not scheme:
                            scheme = 'https://'
                        elif not scheme.endswith('://'):
                            scheme += '://'
                        full_link = f"{scheme}{domain}/{path}" if path else f"{scheme}{domain}"
                        if full_link not in links: 
                            links.append(full_link)
        except ChannelPrivateError:
            r_print(f"[red]Cannot access the channel {channel.channel_name} due to privacy settings.[/red]")
            continue
        except ChatWriteForbiddenError:
            r_print(f"[red]Do not have permission to write in the channel {channel.channel_name}.[/red]")
            continue
        except FloodWaitError as e:
            r_print(f"[yellow]Flood wait error encountered. Try again after {e.seconds} seconds.[/yellow]")
            continue
        except Exception as e:
            r_print(f"[red]An unexpected error occurred: {str(e)}.[/red]")
            continue

    r_print(f"[green]Collected {len(links)} links from unread messages in subscribed channels.[/green]")
    return links

async def join_group_links(links: list[str]):
    for link in links:
        if SAFE_MODE['active']: await asyncio.sleep(SAFE_MODE['sleep'])
        r_print(f'[blue bold]Trying to join {link}[/blue bold]')
        result = await join_chat(client=tel_client, link=link)
        if not result: continue
        r_print(f"[green bold]Successfully joined {result.title}.[/green bold]")
        try:
            if result.usernames:
                username = result.usernames[-1].username
            elif result.username:
                username = result.username
            else:
                username = ''
            await AsyncDatabaseManager().create_group(
                group_id=str(result.id),
                group_name=result.title,
                group_username=username)
            r_print(f"[green bold]Successfully joined the group {result.title} and added to the database.[/green bold]")
        except Exception as e:
            r_print(f"[red bold]Fail to add {result.title} to database: {e}.[/red bold]")
