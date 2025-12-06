from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, HttpUrl
from typing import List
from fastapi.middleware.cors import CORSMiddleware

#importing modules
from database import init_db, get_db, CrawlResult
from crawler_engine import run_crawler_task

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
# Tirigger Crawl
@app.post("/audit")
async def start_audit(request: AuditRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_crawler_task, str(request.url))
    return {"status": "accepted", "message": "Crawler started"}

# Get All Audits
@app.get("/audits", response_model=List[AuditSummary])
async def get_audits(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CrawlResult.id, CrawlResult.url, CrawlResult.title, CrawlResult.created_at, CrawlResult.screenshot_b64).order_by(CrawlResult.id.desc()))
    return result.all()

#Getting single audit with screenshot
@app.get("/audit/{id}", response_model=AuditSummary)
async def get_audit(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CrawlResult).where(CrawlResult.id == id))
    audit = result.scalars().first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit

# Delete an audit
@app.delete("/audit/{id}")
async def delete_audit(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CrawlResult).where(CrawlResult.id == id))
    audit = result.scalars().first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    await db.delete(audit)
    await db.commit()
    return {"status": "Deleted", "id": id}