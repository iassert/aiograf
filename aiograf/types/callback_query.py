from aiogram.types import CallbackQuery

from .message import Message_

from ..bot.noraiseclass import noraiseclass

from typing import Union

no_rise = noraiseclass()
@no_rise.noraiseclass
class CallbackQuery_(CallbackQuery):
    def __init__(self: 'CallbackQuery', call: Union[CallbackQuery, 'CallbackQuery_']) -> None:
        self.__dict__ = call.__dict__.copy()
        self.message  = Message_(self.message)
