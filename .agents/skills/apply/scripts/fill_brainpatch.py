import asyncio
import sys

from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BRAINPATCH_STUDY = """Investigation into real-time closed-loop neuromodulation and autonomic regulation combining non-invasive stimulation (taVNS/tES) with continuous EEG and HRV biomarker tracking. As an undergraduate penultimate-year student in Psychology and Language Sciences at University College London (UCL), my background spans neural signal decoding, biofeedback pipelines, and machine learning architectures.

In this study, I aim to evaluate closed-loop parameter adaptation of stimulation based on real-time RMSSD and EEG spectral dynamics to accelerate recovery from cognitive fatigue and optimize attentional readiness. I am legally authorized for full-time research in the UK under my UK Student Route visa (and eligible for the 2-year unsponsored Graduate Route visa upon graduation)."""

async def fill_brainpatch():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if 'brainpatch.ai' in pg.url), None)
        if not page:
            print("BrainPatch page not found")
            return

        print("BrainPatch URL:", page.url)

        # 1. Full name
        name_input = page.locator('#academicName, input[name="fullName"]')
        await name_input.fill("Kyubin Yun")
        print("Filled Name: Kyubin Yun")

        # 2. Email
        email_input = page.locator('#academicEmail, input[name="email"]')
        await email_input.fill("zcjtyun@ucl.ac.uk")
        print("Filled Email: zcjtyun@ucl.ac.uk")

        # 3. Institution / Lab
        inst_input = page.locator('#academicInst, input[name="institution"]')
        await inst_input.fill("University College London (UCL) - Psychology and Language Sciences")
        print("Filled Institution: UCL")

        # 4. Country
        country_input = page.locator('#academicCountry, input[name="country"]')
        await country_input.fill("United Kingdom")
        print("Filled Country: United Kingdom")

        # 5. Research Pillar (Closed-Loop HRV/EEG/ML)
        pillar_sel = page.locator('#academicPillar, select[name="researchPillar"]')
        await pillar_sel.select_option("closed-loop-hrv-eeg-ml")
        print("Selected Pillar: Closed-Loop HRV/EEG/ML")

        # 6. Role (Research engineer / lab manager)
        role_sel = page.locator('#academicRole, select[name="role"]')
        await role_sel.select_option("research-engineer")
        print("Selected Role: Research engineer / lab manager")

        # 7. Study description
        study_input = page.locator('#academicStudy, textarea[name="studyDescription"]')
        await study_input.fill(BRAINPATCH_STUDY)
        print("Filled Study Description (tailored proposal):", len(BRAINPATCH_STUDY), "chars")

        # 8. Verification & Safety Halt
        submit_btn = page.locator('#academic-submit, button[type="submit"]:has-text("Submit application")')
        print(f"Submit button present: {await submit_btn.count() > 0}")
        print("\n[Zero Auto-Submit Guardrail Enforced]")
        print("BrainPatch.AI academic application is completely filled and standing at final Review / Pre-submit stage.")
        print("Submit button (#academic-submit) NOT clicked. User can review directly in visible Whale browser window.")

if __name__ == '__main__':
    asyncio.run(fill_brainpatch())
