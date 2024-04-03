import asyncio
import sys
import logging
from rich import print as r_print
from bot.tel_bot import TBot
from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker
from aiogram.enums import ParseMode
from database import init_db, AsyncDatabaseManager
from bot.start_handler import start_router
from bot.switch_handler import switches_router
from bot.manage_bot_handler import manage_bot_router
from bot.auto_sec_handler import auto_sec_router
from bot.manage_banners import manage_banners_router
from bot.manage_link_channels import manage_link_channels_router
from bot.manage_groups import manage_groups_router
from GLOBALS import *

async def start_bot():
    DP = Dispatcher()
    BOT = TBot(BOT_TOKEN,
               parse_mode=ParseMode.HTML)
    # Initialize the database
    DB_ENGINE = await init_db(DATABASE_URL)
    async_session = async_sessionmaker(DB_ENGINE, expire_on_commit=False)
    AsyncDatabaseManager(async_session=async_session)
    
    client = await AsyncDatabaseManager().get_client(client_id=CLIENT_ID)
    if not client:
        r_print(f'[red bold]Please first start the client source![/red bold]')
        return

    DP.include_routers(start_router,
                       switches_router,
                       manage_bot_router,
                       auto_sec_router,
                       manage_banners_router,
                       manage_link_channels_router,
                       manage_groups_router)
    await DP.start_polling(BOT)

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())
