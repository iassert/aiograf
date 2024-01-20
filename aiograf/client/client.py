import inspect

from pyrogram       import Client
from pyrogram.types import Message

from ..bot.noraiseclass import noraiseclass

from typing  import Union, Any, Callable
from asyncio import Lock


no_rise = noraiseclass()
@no_rise.noraiseclass
class Client_(Client):
    def __init__(self: 'Client_', сlient: Union[Client, 'Client_']) -> None:
        self.__dict__ = сlient.__dict__.copy()


class SingletonObjMeta(type):
    _instances_key: set[str] = set()
    _instances: dict[str, dict[Any, type]] = {
        i: {}
        for i in _instances_key
    }

    def __call__(cls, *args, **kwargs):
        if SingletonObjMeta._instances_key == set():
            return super().__call__(*args, **kwargs)

        # > получаем все переданные аргументы, как dict
        ukwargs = {}
        constructor_signature = inspect.signature(cls.__init__)
        for key, value in zip(constructor_signature.parameters.keys(), (cls,) + args):
            ukwargs[key] = value
        ukwargs.update(kwargs)
        # <

        obj = None
        # > создаём список из ключей _instances_key и значений ukwargs
        # > проверяем есть ли у нас obj по одному из ключей _instances_key
        _instances_dict = {}
        for key in SingletonObjMeta._instances_key:
            if key not in ukwargs:
                continue
            
            value = ukwargs[key]
            if obj is None and value in SingletonObjMeta._instances[key]:
                obj = SingletonObjMeta._instances[key][value]

            _instances_dict[key] = value
        # <
        
        if _instances_dict == {}:
            return super().__call__(*args, **kwargs)

        if obj is not None:
            return obj
        obj = super().__call__(*args, **kwargs)

        for key, value in _instances_dict.items():
            SingletonObjMeta._instances[key][value] = obj

        return obj


class SingletonObjBase(metaclass = SingletonObjMeta):
    ...


no_rise = noraiseclass()
@no_rise.noraiseclass
class SingleClient(SingletonObjBase, Client):
    __doc__ = Client.__doc__

    def single_obj(self):
        for key, value in SingletonObjMeta._instances.copy().items():
            for key_, value_ in value.copy().items():
                if self is value_:
                    del SingletonObjMeta._instances[key][key_]

    @staticmethod
    def add_key(*args) -> None:
        args_set = {*args}
        _new_instances_key = args_set - SingletonObjMeta._instances_key
        SingletonObjMeta._instances_key |= args_set

        if _new_instances_key == set():
            return

        for i in _new_instances_key:
            SingletonObjMeta._instances[i] = {}


def media_group_handler(f: Callable):
    lock: Lock = Lock()
    processed_media_groups_ids: list[int] = []

    async def wrapper(client: Client, message: Message, *args, **kwargs) -> None:
        async with lock:
            if message.media_group_id in processed_media_groups_ids:
                return
            processed_media_groups_ids.append(message.media_group_id)
        await f(client, message, *args, **kwargs)

    return wrapper
