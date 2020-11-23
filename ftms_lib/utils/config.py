import json
import os

from abc import ABCMeta, abstractmethod
from typing import Any


class Configuration(metaclass=ABCMeta):

    @abstractmethod
    def __contains__(self, item):
        pass

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: Any):
        pass

    @abstractmethod
    def set_default(self, default: dict):
        pass


class FileConfiguration(Configuration):
    _map: dict
    _filename: str

    def __init__(self, filename: str):
        super(FileConfiguration, self).__init__()
        self._map = dict()
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    def __contains__(self, item):
        return item in self._map

    def get(self, key: str, default: Any = None):
        paths = key.split(".")
        res = self._map

        for x in paths:
            if x not in res:
                return default
            else:
                res = res[x]

        return res

    def set(self, key: str, value: Any):
        paths = key.split(".")
        res = self._map

        for x in range(len(paths) - 1):
            if paths[x] not in res:
                res[paths[x]] = dict()
            res = res[paths[x]]

        res[paths[-1]] = value

    def set_default(self, default: dict):
        for k, v in default.items():
            if k not in self._map:
                self._map[k] = v

    def save(self):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError


class JsonConfiguration(FileConfiguration):

    def __init__(self, filename: str):
        super(JsonConfiguration, self).__init__(filename=filename)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self._map, f, indent=4)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self._map = json.load(f)
