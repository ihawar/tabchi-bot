from sqlalchemy import select, delete, update, func
from database.models import Client, LinkStorageChannels, Group, MessageSec, Banner, UserPv
from sqlalchemy.ext.asyncio import AsyncSession

class AsyncDatabaseManager:
    _instance = None
    _is_initialized = False

    def __new__(cls, async_session=None, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AsyncDatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, async_session: AsyncSession = None, *args, **kwargs):
        if not self._is_initialized:
            if not async_session:
                raise ValueError('AsyncDatabaseManager must be initialized with an async session first.')
            self.async_session = async_session
            self._is_initialized = True

    # Client Methods
    async def create_client(self, client_id: str, client_username: str, client_full_name: str, is_online: bool = True, auto_join: bool = True, send_every_mins: int = 5) -> Client:
        async with self.async_session() as session:
            client = Client(client_id=client_id, client_username=client_username, client_full_name=client_full_name, is_online=is_online, auto_join=auto_join, send_every_mins=send_every_mins)
            session.add(client)
            await session.commit()
            await session.refresh(client)
            return client

    async def get_client(self, id: int = None, client_id: str = None) -> Client:
        async with self.async_session() as session:
            query = select(Client)
            if id:
                query = query.filter(Client.id == id)
            elif client_id:
                query = query.filter(Client.client_id == client_id)
            else:
                return None
            result = await session.execute(query)
            return result.scalars().first()

    async def delete_client(self, id: int) -> bool:
        async with self.async_session() as session:
            result = await session.execute(delete(Client).where(Client.id == id))
            await session.commit()
            return bool(result.rowcount)

    async def update_client(self, client_id: str, **kwargs) -> bool:
        async with self.async_session() as session:
            result = await session.execute(update(Client).where(Client.client_id == client_id).values(**kwargs))
            await session.commit()
            return bool(result.rowcount)

    # LinkStorageChannels Methods
    async def create_link_storage_channel(self, channel_id: str, channel_username: str, channel_name: str) -> LinkStorageChannels:
        async with self.async_session() as session:
            channel = LinkStorageChannels(channel_id=channel_id, channel_username=channel_username, channel_name=channel_name)
            session.add(channel)
            await session.commit()
            await session.refresh(channel)
            return channel

    async def get_link_storage_channel(self, id: int = None, channel_id: str = None) -> LinkStorageChannels:
        async with self.async_session() as session:
            query = select(LinkStorageChannels)
            if id:
                query = query.filter(LinkStorageChannels.id == id)
            elif channel_id:
                query = query.filter(LinkStorageChannels.channel_id == channel_id)
            else:
                return None
            result = await session.execute(query)
            return result.scalars().first()

    async def get_all_link_storage_channels(self) -> list[LinkStorageChannels]:
        async with self.async_session() as session:
            result = await session.execute(select(LinkStorageChannels))
            return result.scalars().all()

    async def delete_link_storage_channel(self, id: int=None, channel_id: str=None) -> bool:
        async with self.async_session() as session:
            query = delete(LinkStorageChannels)
            if id:
                query = query.where(LinkStorageChannels.id == id)
            elif channel_id:
                query = query.where(LinkStorageChannels.channel_id == channel_id)
            result = await session.execute(query)
            await session.commit()
            return bool(result.rowcount)
        
    # Group Methods
    async def create_group(self, group_id: str, group_username: str, group_name: str) -> Group:
        async with self.async_session() as session:
            group = Group(group_id=group_id, group_username=group_username, group_name=group_name)
            session.add(group)
            await session.commit()
            await session.refresh(group)
            return group

    async def get_group(self, id: int = None, group_id: str = None) -> Group:
        async with self.async_session() as session:
            query = select(Group)
            if id:
                query = query.filter(Group.id == id)
            elif group_id:
                query = query.filter(Group.group_id == group_id)
            else:
                return None
            result = await session.execute(query)
            return result.scalars().first()

    async def get_all_groups(self) -> list[Group]:
        async with self.async_session() as session:
            result = await session.execute(select(Group))
            return result.scalars().all()

    async def delete_group(self, id: int=None, group_id: str=None) -> bool:
        async with self.async_session() as session:
            query = delete(Group)
            if id:
                query = query.where(Group.id == id)
            elif group_id:
                query = query.where(Group.group_id == group_id)
            result = await session.execute(query)
            await session.commit()
            return bool(result.rowcount)
    
    async def update_group(self, group_id: str, **kwargs) -> bool:
        async with self.async_session() as session:
            result = await session.execute(update(Group).where(Group.group_id == group_id).values(**kwargs))
            await session.commit()
            return bool(result.rowcount)

    # Banner Methods
    async def create_banner(self, title: str, text: str) -> Banner:
        async with self.async_session() as session:
            banner = Banner(text=text, title=title)
            session.add(banner)
            await session.commit()
            await session.refresh(banner)
            return banner

    async def get_banner(self, id: int) -> Banner:
        async with self.async_session() as session:
            result = await session.execute(select(Banner).where(Banner.id == id))
            return result.scalars().first()

    async def get_all_banners(self) -> list[Banner]:
        async with self.async_session() as session:
            result = await session.execute(select(Banner))
            return result.scalars().all()

    async def delete_banner(self, id: int) -> bool:
        async with self.async_session() as session:
            result = await session.execute(delete(Banner).where(Banner.id == id))
            await session.commit()
            return bool(result.rowcount)

    async def increase_banner_sent_count(self, id: int) -> bool:
        async with self.async_session() as session:
            result = await session.execute(update(Banner).where(Banner.id == id).values(sent_count=Banner.sent_count + 1))
            await session.commit()
            return bool(result.rowcount)

    # MessageSec Methods
    async def create_message_sec(self, response: str) -> MessageSec:
        async with self.async_session() as session:
            message_sec = MessageSec(response=response)
            session.add(message_sec)
            await session.commit()
            await session.refresh(message_sec)
            return message_sec
    
    async def update_message_sec(self, id: int, **kwargs) -> bool:
        async with self.async_session() as session:
            result = await session.execute(update(MessageSec).where(MessageSec.id == id).values(**kwargs))
            await session.commit()
            return bool(result.rowcount)

    async def get_message_sec(self, id: int) -> MessageSec:
        async with self.async_session() as session:
            result = await session.execute(select(MessageSec).where(MessageSec.id == id))
            return result.scalars().first()

    async def get_all_message_secs(self) -> list[MessageSec]:
        async with self.async_session() as session:
            result = await session.execute(select(MessageSec))
            return result.scalars().all()

    async def delete_message_sec(self, id: int) -> bool:
        async with self.async_session() as session:
            result = await session.execute(delete(MessageSec).where(MessageSec.id == id))
            await session.commit()
            return bool(result.rowcount)

    async def increase_message_sec_pv_count(self, id: int) -> bool:
        async with self.async_session() as session:
            result = await session.execute(update(MessageSec).where(MessageSec.id == id).values(pv_count=MessageSec.pv_count + 1))
            await session.commit()
            return bool(result.rowcount)

    # User pv
    async def create_user_pv(self, user_id: str) -> UserPv:
        async with self.async_session() as session:
            user = UserPv(user_id=user_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    
    async def get_user_pv(self, user_id: str) -> UserPv:
        async with self.async_session() as session:
            result = await session.execute(select(UserPv).where(UserPv.user_id == user_id))
            return result.scalars().first()
        