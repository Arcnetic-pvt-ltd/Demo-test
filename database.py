import os
import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

# ---------- ASYNC ENGINE (FASTAPI) ----------

async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ---------- SYNC ENGINE (CELERY) ----------

SYNC_DATABASE_URL = DATABASE_URL.replace("asyncpg", "psycopg2")

sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SyncSessionLocal = sessionmaker(bind=sync_engine)

# ---------- BASE MODEL ----------

Base = declarative_base()

# ---------- TABLE ----------

class CrawlResult(Base):
    __tablename__ = "crawl_results"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, unique=True)
    title = Column(String)
    screenshot_b64 = Column(Text)
    html_content = Column(Text)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

# ---------- DB INIT ----------

async def init_db(retries: int = 10, delay: float = 1.0):
    attempt = 0
    while True:
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            print("Database initialized successfully")
            return

        except Exception as e:
            attempt += 1

            if attempt >= retries:
                raise e

            await asyncio.sleep(delay * attempt)

# ---------- FASTAPI DEPENDENCY ----------

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
