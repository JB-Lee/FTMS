from ftms_lib import SessionStatus, SessionHandler, NullSessionHandler, SessionManager, SessionContext
from ftms_lib import protocol
from .databases import DatabaseContext, DatabaseController, DatabaseStatus
import time, uuid
    

class DBSessionManager(SessionManager):
    _session_keeping_time = 600 # session 유지 시간


    def get_session_state(self, session: str) -> SessionStatus:
        _session = session
        if _session is None:
            return SessionStatus.INVALID

        _query = f"SELECT session_id FROM session WHERE session_id == {_session}"
        with DatabaseContext() as cursor:
            last_modified = int(DatabaseController.get_select_database(cursor, _query)["last_modified"])
            
            if last_modified + self._session_keeping_time  <= time.time():
                return SessionStatus.EXPIRED
            else:
                return SessionStatus.OK


    def create_session(self, session: str) -> bool:
        _creation_time: int = time.time()
        _last_modified: _creation_time = _creation_time
        session = str(uuid.uuid4())

        _query = f"INSERT INTO session VALUES ({session}, {_last_modified}, {_creation_time}"
        with DatabaseContext() as cursor:
            result = DatabaseController.get_insert_database(cursor, _query)
            
            if result == DatabaseStatus.OK:
                return True
            else:
                return False

    
    def delete_session(self, session: str) -> bool:
        _query = f"DELETE FROM session WHERE session_id = {session}"

        with DatabaseContext() as cursor:
            result = DatabaseController.get_delete_database(cursor, _query)

            if result == DatabaseStatus.OK:
                return True
            else: # ERROR
                return False
    
    def update_session(self, session: str) -> bool:
        _query = f"UPDATE session SET last_modified = {time.time()} WHERE session_id = {session}"
        
        with DatabaseContext() as cursor:
            result = DatabaseController.get_update_database(cursor, _query)

            if result == DatabaseStatus.OK:
                return True
            else:
                return False


class SessionStateHandler(SessionHandler, DBSessionManager):

    def on_session_ok(self, session: str):        
        # session 존재 하니 동작 할 것
        self.update_session(session)
        pass

    def on_session_expired(self, session: str):
        self.delete_session(session)
        # session 만료 (재 로그인)

        with SessionContext(ctx) as sess:
            sess.write(
                protocol.ProtocolBuilder()
                .set_method("on_session_expired")
                .set_session(None)
                .set_result("Re-login")
            )
        pass

    def on_session_invalid(self, session: str):
        
        # session 존재하지 않음 (생성 요구)
        self.create_session(session)
        pass
