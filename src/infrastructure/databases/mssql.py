from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from infrastructure.databases.base import Base
import os

# Database configuration
DATABASE_URI = (Config.DATABASE_URI or '').strip()
# Remove surrounding quotes if present (env values sometimes include them)
if (DATABASE_URI.startswith('"') and DATABASE_URI.endswith('"')) or \
   (DATABASE_URI.startswith("'") and DATABASE_URI.endswith("'")):
    DATABASE_URI = DATABASE_URI[1:-1].strip()

# Compute a local dev DB path inside the `src` folder for fallback
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DEV_DB_PATH = os.path.join(SRC_DIR, 'dev.db')

# Determine connect_args for sqlite
def _connect_args_for(uri: str):
    if uri.startswith('sqlite'):
        return {"check_same_thread": False}
    return {}

# Try to create the engine using the configured URI. If the required DB driver
# is not installed (e.g. `pymssql` for mssql+pymssql), fall back to a local
# SQLite database so the app can run in development without the external driver.
engine = None
_used_uri = DATABASE_URI
if not _used_uri:
    _used_uri = f"sqlite:///{DEV_DB_PATH.replace('\\', '/')}"

from sqlalchemy.engine import url as sa_url
from sqlalchemy.exc import ArgumentError

try:
    # Validate URL parsing first to catch malformed values early
    try:
        sa_url.make_url(_used_uri)
    except ArgumentError:
        # Fallback to sqlite if the configured URI is not parseable
        _used_uri = f"sqlite:///{DEV_DB_PATH.replace('\\', '/')}"

    connect_args = _connect_args_for(_used_uri)
    engine = create_engine(_used_uri, connect_args=connect_args)
except ModuleNotFoundError as e:
    _err = str(e).lower()
    if 'pymssql' in _err or 'module named' in _err:
        _used_uri = f"sqlite:///{DEV_DB_PATH.replace('\\', '/')}"
        connect_args = _connect_args_for(_used_uri)
        engine = create_engine(_used_uri, connect_args=connect_args)
    else:
        raise
except ArgumentError:
    # Any other argument errors fallback to sqlite
    _used_uri = f"sqlite:///{DEV_DB_PATH.replace('\\', '/')}"
    connect_args = _connect_args_for(_used_uri)
    engine = create_engine(_used_uri, connect_args=connect_args)

# Use scoped_session so each thread/request gets its own Session
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# convenience global session (thread-local via scoped_session)
session = SessionLocal

def init_mssql(app=None):
    # Ensure tables exist for the chosen engine
    Base.metadata.create_all(bind=engine)
