from typing import Type, TypeVar

_T = TypeVar("_T")


class classdict:
    def __init__(self, *, defult_key: str):
        self.defult_key = defult_key

    def classdict(self, cls: Type) -> type[_T]:
        for i, j in cls.__dict__.items():
            if not isinstance(j, dict):
                continue
            value: dict = j.copy()

            class Meta(type):
                def __getitem__(cls, key):
                    if key not in value:
                        return value.get(self.defult_key)
                    return value.get(key)

            class Class(metaclass = Meta):
                ...

            setattr(cls, i, Class)

        return cls
