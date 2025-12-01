import asyncio
from playwright.async_api import async_playwright
import logging 

#Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            await page.goto(target_url)

            # Extracting data
            page_title = await page.title()
            logging.info(f"Page title: {page_title}")

            # Taking evidence screenshot
            await page.screenshot(path="evidence.png")
            logging.info("Screenshot taken and saved as evidence.png")

        except Exception as e:
            logging.error("Entered URL is invalid")

        finally:
            await context.close()
            await browser.close()
            logging.info("Browser closed. Task completed.")

if __name__ == "__main__":
    url = input("Enter the URL to visit: ")
    asyncio.run(run(url))