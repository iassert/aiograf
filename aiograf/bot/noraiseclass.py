import asyncio
import inspect

from aiogram.utils.exceptions import BotBlocked, RetryAfter

from .api import log

from enum   import Enum, auto
from typing import Type, TypeVar, Callable, Coroutine, Generator, AsyncGenerator

_T = TypeVar("_T")


class NoRiseStatus(Enum):
    break_    = auto()
    continue_ = auto()


class noraiseclass:
    IS_RISE: bool = False


    def __init__(self, 
        exception_handle:  Callable[[BaseException], NoRiseStatus] = None,
        aexception_handle: Callable[[BaseException], NoRiseStatus] = None
    ):
        self.exception_handle:  Callable[[BaseException], NoRiseStatus] = exception_handle
        self.aexception_handle: Callable[[BaseException], NoRiseStatus] = aexception_handle

    @staticmethod
    def init(*, is_rise: bool = False) -> None:
        noraiseclass.IS_RISE = is_rise


    def noraiseclass(self,
        cls: Type, 
    ) -> type[_T]:
        if noraiseclass.IS_RISE:
            return cls
    
        for key, value in cls.__dict__.items():
            if not isinstance(value, Callable):
                continue

            method = self.wrap_method(cls, key)
            if method is not None:
                setattr(cls, key, method)

        return cls


    def _exception_handle(self: 'noraiseclass', 
        ex: BaseException,
        self_cls: Type | str
    ) -> NoRiseStatus:
        from ..types import Message

        if isinstance(self.exception_handle, Callable):
            status = self.exception_handle(ex, self_cls)

            if isinstance(status, NoRiseStatus):
                return status

        #if isinstance(ex, RetryAfter):
        #    await asyncio.sleep(ex.timeout)
        #    return NoRiseStatus.continue_

        if isinstance(ex, BotBlocked):
            return NoRiseStatus.break_

        if isinstance(ex, BaseException):
            if isinstance(self_cls, Message):
                log(self_cls).error(ex)
                return NoRiseStatus.break_

            log(self_cls).error(ex)
            return NoRiseStatus.break_

        return NoRiseStatus.break_

    async def _aexception_handle(self: 'noraiseclass', 
        ex: BaseException,
        self_cls: Type
    ) -> NoRiseStatus:
        from ..types import Message

        if isinstance(self.aexception_handle, Coroutine):
            status = await self.aexception_handle(ex, self_cls)

            if isinstance(status, NoRiseStatus):
                return status
        
        if isinstance(ex, RetryAfter):
            await asyncio.sleep(ex.timeout)
            return NoRiseStatus.continue_

        if isinstance(ex, BotBlocked):
            return NoRiseStatus.break_

        if isinstance(self_cls, Type):
            self_cls = self_cls.__name__
        elif (
            isinstance(self_cls, object) and 
            not isinstance(self_cls, Message)
        ):
            self_cls = self_cls.__class__.__name__

        log(self_cls).error(ex)
        return NoRiseStatus.break_


    def wrap_method(self, cls: Type, method_name: str) -> Callable | Coroutine | Generator | AsyncGenerator:
        original_method: Callable = getattr(cls, method_name)


        def wrapped_sync_method(self_cls, *args, **kwargs):
            while True:
                try:
                    return original_method(self_cls, *args, **kwargs)
                except BaseException as ex:
                    status = self._exception_handle(ex, self_cls)

                    if status is NoRiseStatus.continue_:
                        continue
                return

        def wrapped_generator_method(self_cls, *args, **kwargs):
            while True:
                try:
                    for i in original_method(self_cls, *args, **kwargs):
                        yield i
                except BaseException as ex:
                    status = self._exception_handle(ex, self_cls)

                    if status is NoRiseStatus.continue_:
                        continue
                return

        async def wrapped_async_method(self_cls, *args, **kwargs):
            while True:
                try:
                    return await original_method(self_cls, *args, **kwargs)
                except BaseException as ex:
                    status = await self._aexception_handle(ex, self_cls)

                    if status is NoRiseStatus.continue_:
                        continue
                return

        async def wrapped_asyncgenerator_method(self_cls, *args, **kwargs):
            while True:
                try:
                    async for i in original_method(self_cls, *args, **kwargs):
                        yield i
                except BaseException as ex:
                    status = await self._aexception_handle(ex, self_cls)

                    if status is NoRiseStatus.continue_:
                        continue
                return

        def wrapped_descriptor_method(self_cls, *args, **kwargs):
            if not isinstance(self_cls, cls):
                args = (self_cls,) + args

            while True:
                try:
                    return original_method(*args, **kwargs)
                except BaseException as ex:
                    status = self._exception_handle(ex, self_cls)

                    if status is NoRiseStatus.continue_:
                        continue
                return


        if inspect.iscoroutinefunction(original_method):
            return wrapped_async_method

        if inspect.isasyncgenfunction(original_method):
            return wrapped_asyncgenerator_method

        if inspect.isgeneratorfunction(original_method):
            return wrapped_generator_method

        if inspect.ismethod(original_method):
            return wrapped_sync_method
        
        if inspect.ismethoddescriptor(original_method):
            return wrapped_descriptor_method

