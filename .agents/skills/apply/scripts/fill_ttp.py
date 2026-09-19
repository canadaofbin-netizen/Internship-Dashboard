import asyncio
import sys

from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RESUME_PATH = r"g:\My Drive\Kyubin_Yun_Workspace\04_Internship\01_Resumes\Kyubin_Yun_Resume_2027.pdf"

TTP_MESSAGE = """Dear TTP Hiring Team,

I am writing to express my strong enthusiasm for the Summer Internship 2027 - Software Engineering Consultant position at The Technology Partnership (TTP). As a penultimate-year BSc Psychology and Language Sciences student at University College London (UCL), my academic training and research engineering projects bridge complex data processing, computational modeling, and machine learning pipelines.

In my recent research engineering work, I architected automated AI classification systems that achieved a 98% agreement rate against human coders, and I am actively engineering EEG neural signal decoding models for real-time spatial intent. At TTP, I am excited to apply my software engineering, statistical modeling, and analytical capabilities to solve demanding multidisciplinary client challenges at the intersection of technology, sensing, and breakthrough engineering systems.

UK Work Authorization: I hold a valid UK Student Route visa legally permitting full-time employment (40 hours/week) during university summer vacations without requiring employer sponsorship. Upon graduation in June 2028, I am eligible for the 2-year unsponsored Graduate Route visa granting full working rights.

Thank you for your consideration.

Sincerely,
Kyubin Yun"""

async def fill_ttp():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if 'smartrecruiters.com/oneclick-ui' in pg.url), None)
        if not page:
            print("TTP page not found")
            return

        print("TTP Current URL:", page.url)

        # If already on screening page, navigate Back to ensure Step 1 is populated
        if "screening" in page.url:
            back_btn = page.locator('spl-button:has-text("Back"), button:has-text("Back")')
            if await back_btn.count() > 0:
                print("Navigating Back to Step 1 to verify and complete fields...")
                await back_btn.first.click()
                await page.wait_for_timeout(2000)

        # 1. Fill First Name & Last Name
        await page.locator('input#first-name-input').fill("Kyubin")
        await page.locator('input#last-name-input').fill("Yun")
        print("Filled Name: Kyubin Yun")

        # 2. Fill Email & Confirm Email
        await page.locator('input#email-input').fill("zcjtyun@ucl.ac.uk")
        await page.locator('input#confirm-email-input').fill("zcjtyun@ucl.ac.uk")
        print("Filled Email: zcjtyun@ucl.ac.uk")

        # 3. Fill City (Location autocomplete)
        city_input = page.locator('spl-autocomplete input, [data-test="location-autocomplete"] input')
        if await city_input.count() > 0:
            val = await city_input.first.input_value()
            if not val:
                await city_input.first.click()
                await city_input.first.press_sequentially("London", delay=100)
                await page.wait_for_timeout(1500)
                opt = page.locator('spl-select-option:has-text("London, England, United Kingdom")')
                if await opt.count() > 0:
                    await opt.first.click()
                else:
                    await city_input.first.press("Enter")
            print("Verified City: London, England, United Kingdom")

        # 4. Fill Phone Number
        phone_input = page.locator('input[type="tel"], input#spl-form-element_2')
        if await phone_input.count() > 0:
            await phone_input.first.fill("+447787442404")
            print("Filled Phone: +44 7787 442404")

        # 5. Fill Profiles
        li_input = page.locator('input#linkedin-input')
        if await li_input.count() > 0:
            await li_input.first.fill("https://www.linkedin.com/in/kyubin-yun-495a33301/")
            print("Filled LinkedIn")

        web_input = page.locator('input#website-input')
        if await web_input.count() > 0:
            await web_input.first.fill("https://github.com/canadaofbin-netizen")
            print("Filled GitHub/Website")

        # 6. Upload Resume
        file_input = page.locator('input#file-input, input[type="file"]')
        if await file_input.count() > 0:
            await file_input.first.set_input_files(RESUME_PATH)
            print("Uploaded Resume:", RESUME_PATH)
            await page.wait_for_timeout(2000)

        # 7. Fill Message to Hiring Manager
        ta = page.locator('textarea, spl-textarea textarea, [id*="element_10"] textarea')
        if await ta.count() > 0:
            await ta.first.fill(TTP_MESSAGE)
            print("Filled Message to Hiring Manager (tailored motivation):", len(TTP_MESSAGE), "chars")

        # 8. Click Next button to advance to screening step
        print("Clicking Next button to advance to screening step...")
        next_btn = page.locator('spl-button:has-text("Next"), button:has-text("Next")')
        if await next_btn.count() > 0:
            await next_btn.first.click()
            await page.wait_for_timeout(3000)

        print("Current URL on Step 2:", page.url)

        # 9. Tick declaration checkbox piercing Shadow DOM
        cb = page.locator('spl-checkbox input[type="checkbox"], spl-checkbox[data-test="consent-box"]')
        if await cb.count() > 0:
            is_checked = await page.evaluate("""() => {
                const spl = document.querySelector('spl-checkbox');
                return spl && (spl.value === true || spl.shadowRoot?.querySelector('input')?.checked);
            }""")
            if not is_checked:
                print("Ticking privacy declaration checkbox...")
                await cb.first.click(force=True)
                await page.wait_for_timeout(1000)
            else:
                print("Privacy declaration checkbox already ticked.")

        # 10. Audit final screening state
        final_state = await page.evaluate("""() => {
            const spl = document.querySelector('spl-checkbox');
            const submitBtn = document.querySelector('spl-button[type=\"primary\"], button[type=\"submit\"]');
            return {
                url: window.location.href,
                cbChecked: spl ? (spl.value === true || spl.shadowRoot?.querySelector('input')?.checked) : false,
                submitBtnText: submitBtn ? submitBtn.innerText : 'none'
            };
        }""")
        print("TTP Final Status:", final_state)
        print("[Zero Auto-Submit Guardrail Enforced]: Halted at screening / pre-submit stage without clicking Submit.")

if __name__ == '__main__':
    asyncio.run(fill_ttp())
