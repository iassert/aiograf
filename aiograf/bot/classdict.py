from typing import Type, TypeVar

_T = TypeVar("_T")


class ClassDict:
    def __init__(self, value: dict, defult_key: str) -> None:
        self.value:     dict = value
        self.defult_key: str = defult_key

    def __getitem__(self, key):
        if key not in self.value:
            return self.value.get(self.defult_key)
        return self.value.get(key)
                
class classdict:
    def __init__(self, *, defult_key: str):
        self.defult_key = defult_key

    def classdict(self, cls: Type) -> type[_T]:
        for i, j in cls.__dict__.items():
            if not isinstance(j, dict):
                continue

            value = ClassDict(
                j.copy(), 
                self.defult_key
            )
            setattr(cls, i, value)

        return cls
