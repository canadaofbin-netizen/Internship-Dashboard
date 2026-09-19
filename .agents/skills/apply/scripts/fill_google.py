import asyncio
import sys

from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def fill_google():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if 'google.com/about/careers/applications' in pg.url and 'apply' in pg.url), None)
        if not page:
            print("Google apply page not found, searching in context...")
            for pg in context.pages:
                if 'google.com' in pg.url:
                    print("Found google page:", pg.url)
            return

        print("Google Apply URL:", page.url)

        # Check current step
        # If on role step:
        if 'role' in page.url:
            print("Filling Step 2: Role Information...")
            # Question 1: Are you legally eligible to work in the country of employment? -> Yes
            q1_yes = page.locator('input[name="WorkAuthEligibleQuestion"][value="Yes"]')
            if await q1_yes.count() > 0:
                await q1_yes.check()
                print("Selected WorkAuthEligible: Yes")

            # Question 2: Do you currently need, or will you someday require, Google to sponsor work authorization? -> Yes
            q2_yes = page.locator('input[name="WorkAuthSponsorQuestion"][value="Yes"]')
            if await q2_yes.count() > 0:
                await q2_yes.check()
                print("Selected WorkAuthSponsor: Yes")

            # Click Next to advance to Step 4: Review & Apply
            next_btn = page.locator('button:has-text("Next")')
            if await next_btn.count() > 0:
                print("Clicking Next to proceed to Review step...")
                await next_btn.click()
                await page.wait_for_timeout(3000)
                print("Current URL after Next:", page.url)
                print("Current Title:", await page.title())

        # Read the Review page
        text = await page.evaluate('() => document.body.innerText')
        print("\n--- Review & Apply Page Snippet ---")
        print(text[:1000])

        # Check if Submit button exists
        submit_btn = page.locator('button:has-text("Submit application"), button:has-text("Submit"), [role="button"]:has-text("Submit")')
        print(f"Submit button present: {await submit_btn.count() > 0}")
        print("\n[Zero Auto-Submit Guardrail Enforced]")
        print("Google Careers application is halted at Step 4: Review & Apply.")
        print("Submit button is NOT clicked. Candidate can review all details on screen.")

if __name__ == '__main__':
    asyncio.run(fill_google())
