from abc import ABCMeta, abstractmethod
from enum import Enum


class SessionStatus(Enum):
    OK = 0
    INVALID = 1
    EXPIRED = 2


class SessionHandler(metaclass=ABCMeta):

    @abstractmethod
    def get_session_state(self, session: str) -> SessionStatus:
        pass


class NullSessionHandler(SessionHandler):

    def get_session_state(self, session: str) -> SessionStatus:
        return SessionStatus.OK
