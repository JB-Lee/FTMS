from abc import ABCMeta, abstractmethod
from typing import Any


class DatabaseContext(metaclass=ABCMeta):
    
    def __enter__(self):
        pass
    
    def __exit__(self):
        pass



class DatabaseHandler(metaclass=ABCMeta):

    @abstractmethod
    def get_select_database(cls, query: str) -> Any:
        pass

    @abstractmethod
    def get_insert_database(cls, query: str) -> bool:
        pass

    @abstractmethod
    def get_delete_database(cls, query: str) -> bool:
        pass

    def get_update_database(cls, query: str) -> bool:
        pass