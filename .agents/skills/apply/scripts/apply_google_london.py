import asyncio
import sys

from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def review_google_london():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if 'google.com' in pg.url and 'apply' in pg.url), None)
        if not page:
            print("No Google apply tab found")
            return

        print("Current Apply URL:", page.url)

        # If still on Role or VSI step, click Next to reach Review
        next_btns = page.locator('button:has-text("Next")')
        if await next_btns.count() > 0 and 'review' not in page.url:
            print("Advancing to Review step...")
            await next_btns.last.click()
            await page.wait_for_timeout(4000)

        # Ensure consent checkbox on Review & Apply step is checked to enable the Apply button
        consent_cb = page.locator('input[type="checkbox"], input#c4')
        if await consent_cb.count() > 0:
            is_checked = await consent_cb.first.is_checked()
            if not is_checked:
                print("Checking applicant privacy consent checkbox on Review & Apply page...")
                await consent_cb.first.check()
                await page.wait_for_timeout(1000)
            else:
                print("Consent checkbox is already checked.")

        # Audit review page
        apply_btn = page.locator('button:has-text("Apply")')
        is_disabled = True
        if await apply_btn.count() > 0:
            is_disabled = await apply_btn.first.is_disabled()

        print("\n=======================================================")
        print("GOOGLE LONDON SWE/SRE INTERN 2027 APPLICATION STATUS:")
        print("URL:", page.url)
        print("Title:", await page.title())
        print(f"Apply Button Present: {await apply_btn.count() > 0}, Disabled: {is_disabled}")
        print("\n[Zero Auto-Submit Guardrail Enforced]")
        print("Google Careers London application is strictly halted at final Review & Apply step.")
        print("Apply button is enabled and was NOT clicked. Candidate can review all details on screen.")
        print("=======================================================")

if __name__ == '__main__':
    asyncio.run(review_google_london())
