import asyncio
import logging
import base64
from datetime import datetime, timezone
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from sqlalchemy import select

from database import SyncSessionLocal, CrawlResult

# Load environment
load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------- Retry Helper ----------

async def retry_goto(page, url, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Attempt {attempt}: navigating to {url}")
            await page.goto(url, timeout=20000)
            return
        except Exception as e:
            logging.error(f"Navigation failed: {e}")

            if attempt == retries:
                raise

            await asyncio.sleep(delay)

# ---------- MAIN CRAWLER ----------

async def run_crawler_task(url: str):

    async with async_playwright() as p:

        logging.info("Launching browser...")

        browser = await p.chromium.launch(headless=True)

        iphone_13 = p.devices["iPhone 13"]
        context = await browser.new_context(**iphone_13)
        page = await context.new_page()

        try:
            logging.info(f"Navigating to {url}")

            # Visit page
            await retry_goto(page, url)

            # Extract data
            page_title = await page.title()
            html_content = await page.content()

            logging.info(f"Page title: {page_title}")

            # Screenshot
            screenshot_bytes = await page.screenshot(full_page=True)
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode()

            logging.info("Screenshot captured")

            # ---------- SYNC DB WRITE (CELERY SAFE) ----------

            with SyncSessionLocal() as session:

                result = session.execute(
                    select(CrawlResult).where(CrawlResult.url == url)
                )

                row = result.scalar_one_or_none()

                if row:
                    logging.info("Existing URL found → updating record")

                    row.title = page_title
                    row.screenshot_b64 = screenshot_b64
                    row.html_content = html_content
                    row.created_at = datetime.now(timezone.utc)

                else:
                    logging.info("New URL → inserting record")

                    new_entry = CrawlResult(
                        url=url,
                        title=page_title,
                        screenshot_b64=screenshot_b64,
                        html_content=html_content,
                        created_at=datetime.now(timezone.utc)
                    )

                    session.add(new_entry)

                session.commit()

            logging.info("Database commit successful")

            return {
                "status": "completed",
                "url": url,
                "title": page_title
            }

        except Exception as e:
            logging.error(f"Crawler failed: {e}")

            return {
                "status": "failed",
                "url": url,
                "error": str(e)
            }

        finally:
            await context.close()
            await browser.close()
            logging.info("Browser closed")
