from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import Config

DATABASE_URL = Config.get_mysql_url()
engine = create_engine(
    DATABASE_URL, echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600,
    connect_args={'connect_timeout': 10}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)
Base = declarative_base()
