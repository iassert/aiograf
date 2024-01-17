from aiogram.types import Message

from ..bot.noraiseclass import noraiseclass

from typing import Union

no_rise = noraiseclass()
@no_rise.noraiseclass
class Message_(Message):
    def __init__(self: 'Message_', message: Union[Message, 'Message_']) -> None:
        self.__dict__ = message.__dict__.copy()
