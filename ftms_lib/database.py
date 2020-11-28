from abc import ABCMeta, abstractmethod
from typing import Any
from enum import Enum

class DatabaseStatus(Enum):
    ERROR = 0
    OK = 1

class DatabaseContextHandler(metaclass=ABCMeta):
    
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self):
        pass



class DatabaseHandler(metaclass=ABCMeta):

    # ClassMethod Recommended

    @abstractmethod
    def get_select_database(self, cursor, query: str) -> Any:
        pass

    @abstractmethod
    def get_insert_database(self, cursor ,query: str) -> DatabaseStatus:
        pass

    @abstractmethod
    def get_delete_database(self, cursor ,query: str) -> DatabaseStatus:
        pass

    def get_update_database(cls, cursor, query: str) -> DatabaseStatus:        
        pass