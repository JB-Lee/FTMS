import bson


class ProtocolBuilder:
    __method: str
    __session: str
    __params: dict
    __result: dict

    def __init__(self):
        self.__method = None
        self.__session = None
        self.__params = None
        self.__result = None

    def set_method(self, method: str):
        self.__method = method
        return self

    def set_session(self, session: str):
        self.__session = session
        return self

    def set_params(self, params: dict):
        self.__params = params
        return self

    def set_result(self, result: dict):
        self.__result = result
        return self

    def build(self) -> bytes:
        res = dict()

        if self.__method:
            res["method"] = self.__method

        if self.__session:
            res["session"] = self.__session

        if self.__params:
            res["params"] = self.__params

        if self.__result:
            res["result"] = self.__result

        return bson.dumps(res)
