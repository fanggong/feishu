from app.database.mysql import db_session
from datetime import datetime
from sqlalchemy.dialects.mysql import insert
from app.models.update_logs import UpdateLogs
from app.utils.decorators import retry
import logging

logger = logging.getLogger(__name__)


class LogService:
    @staticmethod
    @retry(max_retries=5, delay=1)
    def record_update_logs(table_class, status, details=''):
        session = db_session()
        log_entry = {
            'scope': table_class.__scope__,
            'table': table_class.__tablename__,
            'operation': table_class.update_strategy,
            'status': status,
            'details': details,
            'update_at': datetime.now()
        }
        try:
            session.execute(insert(UpdateLogs), log_entry)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e