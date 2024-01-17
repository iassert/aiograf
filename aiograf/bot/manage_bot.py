import logging

from aiogram            import Bot
from aiogram.bot.api    import TelegramAPIServer
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.handler          import Handler
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory  import MemoryStorage

from .bot import Bot_

from ..utils import executor

from typing import Optional, List, Callable


class ManageBot:
    def __init__(self, 
        bot: Bot_       = None, 
        dp:  Dispatcher = None
    ) -> None:
        self.bot: Bot_       = bot
        self.dp:  Dispatcher = dp


    def init(self, 
        token: str, 
        *, 
        server: TelegramAPIServer = None,
        message_handlers: Handler = None
    ) -> None:
        bot: Bot       = Bot(token = token, server = server)
        self.bot: Bot_ = Bot_(bot)

        self.dp: Dispatcher = Dispatcher(bot, storage = MemoryStorage())
        self.dp.middleware.setup(LoggingMiddleware())

        if message_handlers is not None:
            self.dp.message_handlers = message_handlers


    @staticmethod
    def on_startup(chat_id: int = None) -> Callable:
        async def _on_startup(dp: Dispatcher):
            if chat_id is not None:
                bot_ = Bot_(dp.bot)
                await bot_.send_message(chat_id, "Бот запущен")

        return _on_startup

    @staticmethod
    def on_shutdown(chat_id: int = None) -> Callable:
        async def _on_shutdown(dp: Dispatcher):
            logging.warning('Shutting down..')

            if chat_id is not None:
                bot_ = Bot_(dp.bot)
                await bot_.send_message(chat_id, "Бот Выключен")

            logging.warning('Bye!')

        return _on_shutdown


    def start_polling(self,
        *, 
        skip_updates:  bool    = True, 
        reset_webhook: bool    = True,
        on_startup_:  Callable = None, 
        on_shutdown_: Callable = None, 
        timeout: int = 300, 
        relax: float = 0.1, 
        fast:   bool = True,
        allowed_updates: Optional[List[str]] = None,
        wait: bool = False
    ) -> bool:
        try:
            executor.start_polling(
                dispatcher    = self.dp,
                skip_updates  = skip_updates, 
                reset_webhook = reset_webhook,
                on_startup    = on_startup_, 
                on_shutdown   = on_shutdown_, 
                timeout = timeout, 
                relax   = relax, 
                fast    = fast,
                allowed_updates = allowed_updates,
                wait = wait
            )
            return True
        except BaseException as ex:
            logging.error(f"{ex.__class__.__name__}: {ex}")
        return False
    
