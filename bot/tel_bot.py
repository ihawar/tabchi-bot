from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession

class TBot(Bot):
    """
    A singleton class that extends the functionality of aiogram's Bot class.
    Ensures that only a single instance of this bot is created throughout the
    application lifecycle.
    """
    _instance = None  
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If the instance doesn't exist, create it by calling the parent class's __new__ method.
            cls._instance = super().__new__(cls)
        # Return the created instance.
        return cls._instance

    def __init__(self, 
                 token: str, 
                 session: BaseSession | None = None, 
                 parse_mode: str | None = None, 
                 disable_web_page_preview: bool | None = None, 
                 protect_content: bool | None = None, 
                 default: DefaultBotProperties | None = None
                 ) -> None:
        if not self._is_initialized:
            # If the instance hasn't been initialized, call the parent class's __init__ method.
            super().__init__(token, session, parse_mode, disable_web_page_preview, protect_content, default)
            # Mark the instance as initialized to prevent re-initialization.
            self._is_initialized = True
    