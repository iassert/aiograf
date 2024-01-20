import os
import logging
import traceback

from aiogram.types import Message

from logging  import Logger
from datetime import datetime

logging.basicConfig(level = logging.INFO)


class log:
    LOG_DIR: str = os.path.join(os.getcwd(), "log")
    EX:      str = "log"


    def __init__(self, 
        name: str | int | float | Message = None, 
        *, 
        base_name: str = "root"
    ) -> None:
        self.__name:      str = self.__set_name(name)
        self.__base_name: str = base_name

    @staticmethod
    def init(_file_: str, *, ex: str = "log"):
        log.LOG_DIR = os.path.abspath(_file_).replace(os.path.basename(_file_), "log")
        log.EX = ex


    def error(self, 
        ex: BaseException | str, 
        caption: str = ""
    ) -> None:
        logger = self.__get_error_logger()

        te = ""
        if isinstance(ex, BaseException):
            for tb in traceback.extract_tb(ex.__traceback__):
                te += ERROR_FORMAT.format(
                    class_name_ = ex.__class__.__name__, 
                    ex    = ex, 
                    file  = tb.filename, 
                    line  = tb.lineno, 
                    f     = tb.name, 
                    code  = tb.line
                )
                #break
        else:
            te = ex

        logger.error(te + caption)

    def info(self,
        text: str
    ): self.__write("INFO",  text)


    @staticmethod
    def __set_name(name: str | int | float | Message = None) -> str | None:
        if isinstance(name, Message):
            message: Message = name
    
            return f"{message.chat.id}-{message.from_user.id}"
        
        if isinstance(name, str | int | float):
            return name.__str__()

    def __get_error_logger(self) -> Logger:
        name: str = self.__name
        if self.__name is None:
            name: str = self.__base_name

        logger = logging.getLogger(name)
        formatter = logging.Formatter('%(levelname)s' + f":{name}\n" + '%(message)s\n%(asctime)s')

        if self.__name is not None:
            file_handler = logging.FileHandler(self.__path(), encoding = "utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        file_error_handler = logging.FileHandler(self.__path("errors"), encoding = "utf-8")
        file_error_handler.setFormatter(formatter)
        logger.addHandler(file_error_handler)

        return logger

    def __path(self, 
        name: str = None
    ) -> str | None:
        if name is None:
            name = self.__name

        if (
            not os.path.exists(log.LOG_DIR) or 
            not os.path.isdir(log.LOG_DIR)
        ):
            os.mkdir(log.LOG_DIR)

        return os.path.join(log.LOG_DIR, f"{name}.{log.EX}")

    def __write(self, 
        lvl_name: str, 
        text: str
    ) -> None:
        ti = INFO_FORMAT.format(
            lvl_name = lvl_name,
            name = self.__name,
            text = text,
            datetime = datetime.now().strftime(r"%d.%m.%Y %H:%M")
        )

        try:
            with open(self.__path(), "a", encoding = "utf-8") as f:
                f.write(ti)
            f.close()
        except BaseException as ex:
            self.error(ex)


ERROR_FORMAT: str = """
{class_name_}: {ex}
File: {file}
Line: {line}
Func: {f}
Cod:  {code}
"""

INFO_FORMAT: str = """
{lvl_name}:{name}
{text}
{datetime}
"""