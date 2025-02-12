from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from functools import lru_cache
import app_config

@lru_cache
def get_settings():
    return app_config.Settings()

SQLALCHEMY_DATABASE_URL = get_settings().db_url

# Using an asynchronous engine for SQLAlchemy
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependency to get the database session
async def get_db():
    async with SessionLocal() as session:
        yield session
