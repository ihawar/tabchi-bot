import asyncio
import logging 
import sys
from client.tel_client import tel_client
from client import handlers
from client.utils import initialize_database, validate_client_id, initialize_client, join_developer
from rich import print as r_print
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from client.tasks import auto_join_manager, send_banners_manager
from GLOBALS import SAFE_MODE

async def main():
    client = tel_client
    await client.start()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_banners_manager, 'interval', 
                      seconds=SAFE_MODE['send_banner_every'] * 60)
    scheduler.add_job(auto_join_manager, 'interval', 
                      seconds=SAFE_MODE['auto_join_every'] * 60)

    is_valid = await validate_client_id(tel_client)
    if not is_valid:
        r_print('[red bold]Client Id is not correct!')
        return
    await initialize_database()
    await initialize_client(tel_client)
    await join_developer(tel_client)
    scheduler.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
