from aiogram import Bot

from ..bot.noraiseclass import noraiseclass

from typing import Union

no_rise = noraiseclass()
@no_rise.noraiseclass
class Bot_(Bot):
    def __init__(self: 'Bot_', bot: Union[Bot, 'Bot_']) -> 'Bot_':
        self.__dict__ = bot.__dict__.copy()
