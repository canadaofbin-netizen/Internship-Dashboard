import asyncio
import sys

from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RESUME_PATH = r"g:\My Drive\Kyubin_Yun_Workspace\04_Internship\01_Resumes\Kyubin_Yun_Resume_2027.pdf"

STANHOPE_STATEMENT = """As a penultimate-year undergraduate in Psychology and Language Sciences at University College London (UCL), I am deeply passionate about Active Inference and the Free Energy Principle applied to embodied intelligence and robotics. My work focuses on neural computation, machine learning pipelines, and predictive processing architectures. In previous research engineering roles, I developed automated AI classification pipelines achieving a 98% agreement score against human coders, and I am currently engineering EEG signal decoding models for spatial intent.

UK Work Authorization: I hold a valid UK Student Route visa legally permitting full-time employment (40 hours/week) during university summer vacations without requiring employer sponsorship. Upon graduation in June 2028, I am eligible for the 2-year unsponsored Graduate Route visa granting full working rights."""

async def fill_stanhope():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if 'stanhopeai.com' in pg.url), None)
        if not page:
            print("Stanhope page not found")
            return

        print("Stanhope URL:", page.url)

        # Ensure lightbox is open
        form = await page.query_selector('.sqs-modal-lightbox-content, form')
        if not form or not await form.is_visible():
            print("Opening lightbox...")
            btn = await page.query_selector('button.lightbox-handle')
            if btn:
                await btn.click()
                await page.wait_for_timeout(2000)

        # 1. Name
        fname = page.locator('input#name-yui_3_17_2_1_1761673008630_3366-fname-field, input[name="fname"]')
        lname = page.locator('input#name-yui_3_17_2_1_1761673008630_3366-lname-field, input[name="lname"]')
        await fname.fill("Kyubin")
        await lname.fill("Yun")
        print("Filled Name: Kyubin Yun")

        # 2. Email
        email = page.locator('input#email-yui_3_17_2_1_1761673008630_3367-field')
        await email.fill("zcjtyun@ucl.ac.uk")
        print("Filled Email: zcjtyun@ucl.ac.uk")

        # 3. Phone (Select GB country code and clean phone input without trailing spaces)
        country_code = page.locator('select#phone-fb8fd118-a8c2-412f-a5dc-bd3701441998-country-code-field')
        if await country_code.count() > 0:
            await country_code.select_option("GB")
            print("Selected Country Code: GB (+44)")

        await page.evaluate("""() => {
            const el = document.querySelector('input#phone-fb8fd118-a8c2-412f-a5dc-bd3701441998-input-field');
            if (el) {
                el.focus();
                el.value = '7787 442404';
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.blur();
            }
        }""")
        print("Filled Phone: +44 7787 442404 (normalized without trailing spaces)")

        # 4. What country are you currently based in?
        country_based = page.locator('input#text-e8f206bb-7a8f-4070-ab49-a7754dca296b-field')
        await country_based.fill("United Kingdom")
        print("Filled Country Based: United Kingdom")

        # 5. What course are you currently studying?
        course = page.locator('input#text-13525d54-dae3-43af-b575-d839a25e3e41-field')
        await course.fill("BSc in Psychology and Language Sciences")
        print("Filled Course: BSc in Psychology and Language Sciences")

        # 6. Which university are you studying at and when are you expecting to graduate?
        uni = page.locator('input#text-30d18b13-5ce9-4ea9-bd82-0dcc4c31bc17-field')
        await uni.fill("University College London (UCL), expecting to graduate June 2028")
        print("Filled Uni & Grad: UCL, June 2028")

        # 7. What months will you be available to complete your internship?
        months = page.locator('input#text-d88fdfac-86ed-497f-b1f6-4e8b5919096f-field')
        await months.fill("June 2027 – September 2027 (3 months summer full-time)")
        print("Filled Availability: June 2027 - September 2027")

        # 8. Area of interest checkboxes (AI, Machine Learning)
        ai_box = page.locator('input[type="checkbox"][value="AI"]')
        if await ai_box.count() > 0 and not await ai_box.is_checked():
            await ai_box.check()
            print("Checked AI")

        ml_box = page.locator('input[type="checkbox"][value="Machine Learning"]')
        if await ml_box.count() > 0 and not await ml_box.is_checked():
            await ml_box.check()
            print("Checked Machine Learning")

        # 9. LinkedIn profile / website
        linkedin = page.locator('input#text-513bcba6-2f85-4efe-b6cb-dc4369393cae-field')
        await linkedin.fill("https://www.linkedin.com/in/kyubin-yun-495a33301/ | https://github.com/canadaofbin-netizen")
        print("Filled LinkedIn & GitHub")

        # 10. CV Upload verification
        cv_status = await page.evaluate("""() => {
            const el = document.querySelector('#file-dbec0b7f-1569-4e72-a421-e149ff22f822');
            return el ? el.innerText : 'none';
        }""")
        if "Kyubin_Yun_Resume_2027.pdf" not in cv_status:
            cv_item = page.locator('#file-dbec0b7f-1569-4e72-a421-e149ff22f822')
            file_input = cv_item.locator('input[type="file"]')
            if await file_input.count() > 0:
                await file_input.first.set_input_files(RESUME_PATH)
                await page.wait_for_timeout(2000)
                print("Uploaded CV:", RESUME_PATH)
        else:
            print("CV already securely attached:", cv_status.splitlines()[1] if len(cv_status.splitlines()) > 1 else cv_status)

        # 11. Additional message
        msg = page.locator('textarea#textarea-yui_3_17_2_1_1761673008630_3369-field')
        await msg.fill(STANHOPE_STATEMENT)
        print("Filled tailored Active Inference motivation & visa details")

        # 12. Verification & Safety Halt
        print("\n[Zero Auto-Submit Guardrail Enforced]")
        print("Stanhope AI application form is completely filled and standing at final Review / Pre-submit stage.")
        print("Submit button NOT clicked. User can review form directly in visible Whale browser window.")

if __name__ == '__main__':
    asyncio.run(fill_stanhope())
