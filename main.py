from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, HttpUrl
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# Internal Imports
# -----------------------------

from database import (
    init_db,
    get_db,
    CrawlResult,
    WebsiteMetadata
)

from tasks import execute_crawler, process_text_pipeline

# -----------------------------
# CORS Config (Frontend Access)
# -----------------------------

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app = FastAPI(title="Arcnetic Spider AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Startup DB Initialization
# -----------------------------

@app.on_event("startup")
async def on_startup():
    await init_db()

# -----------------------------
# Request Models
# -----------------------------

class AuditRequest(BaseModel):
    url: HttpUrl


class TextProcessRequest(BaseModel):
    text: str


class AuditSummary(BaseModel):
    id: int
    url: str
    title: str | None
    created_at: datetime
    screenshot_b64: str | None


class MetadataSummary(BaseModel):
    id: int
    page_title: str | None
    company_name: str | None
    email: str | None
    domain: str | None
    created_at: datetime


# -----------------------------
# ROUTES
# -----------------------------

# ---------- Root Health ----------

@app.get("/")
def root():
    return {"status": "Arcnetic Spider AI Backend Running"}

# ---------- Trigger Crawl (Celery) ----------

@app.post("/audit")
async def start_audit(request: AuditRequest):

    task = execute_crawler.delay(str(request.url))

    return {
        "status": "accepted",
        "message": "Crawl task submitted successfully",
        "task_id": task.id
    }

# ---------- Get All Crawls ----------

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

# ---------- Get Single Crawl ----------

@app.get("/audit/{id}", response_model=AuditSummary)
async def get_audit(id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(CrawlResult).where(CrawlResult.id == id))
    audit = result.scalars().first()

    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    return audit

# ---------- Delete Crawl ----------

@app.delete("/audit/{id}")
async def delete_audit(id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(CrawlResult).where(CrawlResult.id == id))
    audit = result.scalars().first()

    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    await db.delete(audit)
    await db.commit()

    return {"status": "Deleted", "id": id}

# ---------- Direct AI Processing (TEXT INPUT) ----------

@app.post("/process-text")
async def process_text(request: TextProcessRequest):

    task = process_text_pipeline.delay(request.text)

    return {
        "status": "accepted",
        "message": "AI pipeline task started",
        "task_id": task.id
    }

# ---------- Run AI On Crawled Page ----------

@app.post("/audit-ai/{id}")
async def process_audit_ai(id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(CrawlResult).where(CrawlResult.id == id))
    crawl = result.scalars().first()

    if not crawl:
        raise HTTPException(status_code=404, detail="Audit not found")

    # Send cleaned HTML/text into AI pipeline
    task = process_text_pipeline.delay(crawl.html_content)

    return {
        "status": "accepted",
        "message": "AI extraction started for crawl record",
        "crawl_id": id,
        "task_id": task.id
    }

# ---------- Get Extracted AI Metadata ----------

@app.get("/metadata", response_model=List[MetadataSummary])
async def get_metadata(db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(
            WebsiteMetadata.id,
            WebsiteMetadata.page_title,
            WebsiteMetadata.company_name,
            WebsiteMetadata.email,
            WebsiteMetadata.domain,
            WebsiteMetadata.created_at
        ).order_by(WebsiteMetadata.id.desc())
    )

    return result.all()
