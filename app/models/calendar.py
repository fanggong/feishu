from sqlalchemy import Column, Date
from app.database.mysql import Base


class Calendar(Base):
    __scope__ = 'crypto'
    __tablename__ = 'calendar'

    date = Column(Date, primary_key=True, nullable=False, comment='日期')

    def __repr__(self):
        return f"<Calendar(date={self.date})>"
