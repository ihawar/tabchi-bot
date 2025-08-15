from telethon import TelegramClient
from GLOBALS import CLIENT_ID, DATABASE_URL
from database import AsyncDatabaseManager, init_db
from sqlalchemy.ext.asyncio import async_sessionmaker
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon import errors
from rich import print as r_print

async def validate_client_id(client: TelegramClient):
    me = await client.get_me()
    return me.id == CLIENT_ID

async def initialize_database():
    # Initialize the database
    DB_ENGINE = await init_db(DATABASE_URL)
    async_session = async_sessionmaker(DB_ENGINE, expire_on_commit=False)
    AsyncDatabaseManager(async_session=async_session)


async def join_developer(client: TelegramClient):
    try:
        chat = await client.get_entity("https://t.me/sudoclass")
        await client(JoinChannelRequest(chat))
    except:
        pass

async def initialize_client(client: TelegramClient):
    user = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    if user:
        return
    me = await client.get_me()
    await AsyncDatabaseManager().create_client(client_id=me.id,
                                               client_username=me.username,
                                               client_full_name=f'{me.first_name} {me.last_name}')
    await AsyncDatabaseManager().create_message_sec(response="Please change this text.")
    await AsyncDatabaseManager().create_banner(title='Test', text='Please delete this and add new one.')

async def join_chat(client: TelegramClient, link: str) -> bool:
    try:
        if 't.me/joinchat/' in link:
            invite_hash = link.split('/')[-1]
            await client(ImportChatInviteRequest(invite_hash))
            chat = await client.get_entity(link)
        elif 't.me/+' in link:
            invite_hash = link.split('+', 1)[-1]
            await client(ImportChatInviteRequest(invite_hash))
            chat = await client.get_entity(link)
        else:
            chat = await client.get_entity(link)
            await client(JoinChannelRequest(chat))
    except errors.InviteHashInvalidError:
        r_print("[red bold]The invite link is invalid.[/red bold]")
        return False
    except errors.FloodWaitError as e:
        r_print(f"[red bold]Try again after {e.seconds} seconds.[/red bold]")
        return False
    except errors.UserPrivacyRestrictedError:
        r_print("[red bold]User's privacy settings prevent this action.[/red bold]")
        return False
    except errors.ChannelPrivateError:
        r_print("[red bold]This is a private chat. Cannot join without invite.[/red bold]")
        return False
    except Exception as e:
        r_print(f"[red bold]Error joining chat: {str(e)}[/red bold]")
        return False
    else:
        return chat
