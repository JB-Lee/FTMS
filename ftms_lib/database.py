from abc import ABCMeta, abstractmethod
from typing import Any


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
    def get_select_database(self, query: str) -> Any:
        pass

    @abstractmethod
    def get_insert_database(self, query: str) -> bool:
        pass

    @abstractmethod
    def get_delete_database(self, query: str) -> bool:
        pass

    def get_update_database(self, query: str) -> bool:
        pass