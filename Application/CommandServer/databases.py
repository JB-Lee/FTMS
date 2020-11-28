from ftms_lib import DatabaseContextHandler, DatabaseHandler, DatabaseStatus
from pymysqlpool.pool import Pool
from typing import Any


kwargs_database_info = {
    "user" : "root",
    "password" : "mysql1234",
    "host" : "127.0.0.1",
    "db" : "translationfile",
    "autocommit" : True
}



class DatabaseController(DatabaseHandler):

    @classmethod
    def get_select_database(cls, cursor, query: str) -> Any:
        _cursor = cursor
        _cursor.execute(query)

        return _cursor.fetchone()
    
    @classmethod
    def get_insert_database(cls, cursor ,query: str) -> DatabaseStatus:
        _cursor = cursor
        
        try:
            _cursor.execute(query)
            return DatabaseStatus.OK
        
        except expression as identifier:
            return DatabaseStatus.ERROR
    
    @classmethod
    def get_delete_database(cls, cursor ,query: str) -> DatabaseStatus:
        _cursor = cursor
        try:
            _cursor.execute(query)
            return DatabaseStatus.OK
        
        except expression as identifier:
            return DatabaseStatus.ERROR
    @classmethod
    def get_update_database(cls, cursor ,query: str) -> DatabaseStatus:
        _cursor = cursor
        
        try:
            _cursor.execute(query)
            return DatabaseStatus.OK
        
        except expression as identifier:
            return DatabaseStatus.ERROR


""" 
with DatabaseContext as cursor:
    cursor.execute(query)
    result = cursor.fetchone()

with DatabaseContext as cursor:
    result = cursor.execute(query)

with DatabaseContext as db:
    db.get_select_database(cursor, query)
"""

class DatabaseContext(DatabaseContextHandler, DatabaseController):

    pool = Pool(**kwargs_database_info)
    pool.init()

    def __enter__(self):
        connection = self.pool.get_conn()
        cursor = connection.cursor()

        return cursor

    def __exit__(self, exec_type: exeception_type, exec_val, exc_tb): 
        # exception_type, exception_value, exception_traceback
        
        self.pool.release(connetion)