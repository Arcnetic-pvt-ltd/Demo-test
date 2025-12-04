import os
import asyncio
import logging
import base64
from datetime import datetime, timezone
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from database import SessionLocal, CrawlResult, init_db
from sqlalchemy import select

# Load .env
load_dotenv()

#Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retry for crawling page
async def retry_goto(page, url, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Attempt {attempt}: navigating to {url}")
            await page.goto(url, timeout=15000)  # 15s timeout
            return  # success
        except Exception as e:
            logging.error(f"Navigation failed: {e}")
            if attempt == retries:
                raise
            await asyncio.sleep(delay)

async def run(url: str):
    async with async_playwright() as p:
        logging.info("Launching browser...")
        browser = await p.chromium.launch(headless=True)

        # loading the page in a new context in iphone 13
        iphone_13 = p.devices["iPhone 13"]
        context = await browser.new_context(**iphone_13)
        page = await context.new_page()

        target_url = url
        logging.info(f"Navigating to {target_url}...")
        # Error handling for invalid URL
        try:
            # Visit the target URL
            await retry_goto(page, url)

            # Extracting data
            page_title = await page.title()
            logging.info(f"Page title: {page_title}")

            # Extract HTML
            html_content = await page.content()

            created_at = datetime.now(timezone.utc) 

            # Taking evidence screenshot and encoding to base64
            screenshot_bytes = await page.screenshot(full_page=True)
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            logging.info("Screenshot taken and encoded to base64.")

            #saving to database
            async with SessionLocal() as session:
                result = await session.execute(select(CrawlResult).where(CrawlResult.url == url))
                row = result.scalar_one_or_none()

                if row:
                    logging.info("URL exists - updating entry.")
                    row.title = page_title
                    row.screenshot_b64 = screenshot_b64
                    row.html_content = html_content
                else:
                    logging.info("New URL - inserting entry.")
                    new_entry = CrawlResult(
                        url=url,
                        title=page_title,
                        screenshot_b64=screenshot_b64,
                        html_content=html_content
                    )
                    session.add(new_entry)

                await session.commit()

        except Exception as e:
            logging.error(f"Final failure after retries: {e}")

        finally:
            await context.close()
            await browser.close()
            logging.info("Browser closed. Task completed.")

async def main():
    await init_db()
    url = os.getenv("TARGET_URL", "https://default.com")
    await run(url)

if __name__ == "__main__":
    asyncio.run(main())