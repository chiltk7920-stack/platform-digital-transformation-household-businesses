from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from infrastructure.databases.base import Base

# Database configuration
DATABASE_URI = Config.DATABASE_URI

# For sqlite use-case (development/in-memory) we must allow cross-thread usage
# and set appropriate connect_args. For other DB backends, leave defaults.
connect_args = {}
if DATABASE_URI.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URI, connect_args=connect_args)

# Use scoped_session so each thread/request gets its own Session
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# convenience global session (thread-local via scoped_session)
session = SessionLocal

def init_mssql(app):
    Base.metadata.create_all(bind=engine)