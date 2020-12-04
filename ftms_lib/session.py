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

    @abstractmethod
    def on_session_expired(self):
        pass

    @abstractmethod
    def on_session_invalid(self):
        pass

    @abstractmethod
    def on_session_ok(self):
        pass


class NullSessionHandler(SessionHandler):

    def get_session_state(self, session: str) -> SessionStatus:
        return SessionStatus.OK

    def on_session_expired(self):
        return super().on_session_expired()

    def on_session_invalid(self):
        return super().on_session_invalid()

    def on_session_ok(self):
        return super().on_session_ok()
