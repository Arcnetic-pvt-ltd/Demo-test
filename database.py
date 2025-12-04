import os
import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, TIMESTAMP


DATABASE_URL = os.getenv("DATABASE_URL")

#setingup the database engine
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


#defifining the table

class CrawlResult(Base):
    __tablename__ = 'crawl_results'
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    title = Column(String)
    #Storing Screenshot
    screenshot_b64 = Column(Text)
    html_content = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))

#initializing the database
async def init_db(retries: int = 10, delay: float = 1.0):
    attempt = 0
    while True:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("init_db: database initialized")
            return
        except Exception as e:
            attempt += 1
            if attempt >= retries:
                print(f"init_db: failed after {attempt} attempts: {e!r}")
                raise
            # simple backoff
            wait = delay * attempt
            print(f"init_db: attempt {attempt}/{retries} failed: {e!r}. Sleeping {wait}s and retrying...")
            await asyncio.sleep(wait)

#dependency to get db session
async def get_db():
    async with SessionLocal() as session:
        yield session