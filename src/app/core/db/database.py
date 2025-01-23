from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.core.config import settings

DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_SYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

engine = create_engine(DATABASE_URL, echo=False, future=True)

local_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()