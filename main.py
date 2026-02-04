from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, HttpUrl
from typing import List
from fastapi.middleware.cors import CORSMiddleware

#importing modules
from database import init_db, get_db, CrawlResult
from tasks import execute_crawler

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app = FastAPI(title="Arcnetic Spider API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow POST, GET, DELETE
    allow_headers=["*"],
)
#initialize the database on startup
@app.on_event("startup")
async def on_startup():
    await init_db()

#pydantic model validation
class AuditRequest(BaseModel):
    url: HttpUrl

class AuditSummary(BaseModel):
    id: int
    url: str
    title: str | None
    created_at: datetime
    screenshot_b64: str | None

#---ROUTES---
# Trigger Crawl (ASYNC USING CELERY)
@app.post("/audit")
async def start_audit(request: AuditRequest):

    task = execute_crawler.delay(str(request.url))

    return {
        "status": "accepted",
        "message": "Crawl task submitted successfully",
        "task_id": task.id
    }

# Get All Audits
@app.get("/audits", response_model=List[AuditSummary])
async def get_audits(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            CrawlResult.id,
            CrawlResult.url,
            CrawlResult.title,
            CrawlResult.created_at,
            CrawlResult.screenshot_b64
        ).order_by(CrawlResult.id.desc())
    )
    return result.all()

# Get Single Audit
@app.get("/audit/{id}", response_model=AuditSummary)
async def get_audit(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CrawlResult).where(CrawlResult.id == id))
    audit = result.scalars().first()

    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    return audit

# Delete Audit
@app.delete("/audit/{id}")
async def delete_audit(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CrawlResult).where(CrawlResult.id == id))
    audit = result.scalars().first()

    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    await db.delete(audit)
    await db.commit()

    return {"status": "Deleted", "id": id}