from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime, timezone

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    client_id = Column(String(16), unique=True)
    client_username = Column(String(32), unique=True, nullable=True)
    client_full_name = Column(String(128), nullable=False)
    is_online = Column(Boolean, default=True)
    auto_join = Column(Boolean, default=True)
    send_every_mins = Column(Integer, default=5)
    banners_send_count = Column(Integer, default=0)
    last_sent = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"ClientData(id={self.id}, client_id={self.client_id}, client_username={self.client_username}, client_full_name={self.client_full_name}, is_online={self.is_online}, message_sec={self.message_sec})"

class LinkStorageChannels(Base):
    __tablename__ = 'link_storage_channels'
    id = Column(Integer, primary_key=True) 
    channel_id = Column(String(16), unique=True)
    channel_username = Column(String(32), nullable=True)
    channel_name = Column(String(128))
    
    def __repr__(self) -> str:
        return f"LinkStorageChannels(id={self.id}, channel_id={self.channel_id}, channel_username={self.channel_username}, channel_name={self.channel_name}, channel_name={self.channel_name})"

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True) 
    group_id = Column(String(16), unique=True)
    group_username = Column(String(32), nullable=True)
    group_name = Column(String(128))
    sent_banners = Column(Integer, default=0)
    
    def __repr__(self) -> str:
        return f"Group(id={self.id}, channel_id={self.group_id}, channel_username={self.group_username}, group_name={self.group_name})"

class Banner(Base):
    __tablename__ = 'banners'
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    text = Column(String(2048))
    sent_count = Column(Integer, default=0)

    def __repr__(self) -> str:
        return f"Banner(id={self.id}, text={self.text})"

class MessageSec(Base):
    __tablename__ = 'message_sec'
    id = Column(Integer, primary_key=True)
    response = Column(String(2048))
    is_active = Column(Boolean, default=True)
    pv_count = Column(Integer, default=0)

    def __repr__(self) -> str:
        return f"MessageSec(id={self.id}, response={self.response}, pv_count={self.pv_count})"
