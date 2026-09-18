import asyncio
import sys

from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")

from text_normalizer import normalize_text


async def update_live_fields():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        pages = [pg for pg in browser.contexts[0].pages if "lifeattiktok" in pg.url]
        if not pages:
            print("ERROR: TikTok tab not found on port 9222!")
            return False
        page = pages[0]
        print(f"Connected to TikTok tab: {page.url}")

        # 1. Update phone prefix to +44 (United Kingdom) if not already +44
        phone_prefix_text = await page.evaluate("""() => {
            const el = document.querySelector('[data-cy="selectedValue"]');
            return el ? el.innerText.trim() : '';
        }""")
        print(f"Current phone prefix: '{phone_prefix_text}'")

        if phone_prefix_text != "+44":
            print("Selecting United Kingdom (+44)...")
            phone_box = await page.query_selector('[data-cy="phonePrefix"]')
            if phone_box:
                await phone_box.click()
                await page.wait_for_timeout(300)

                # Click the United Kingdom option
                clicked = await page.evaluate("""() => {
                    const items = document.querySelectorAll('.atsx-select-dropdown-menu-item, [role="option"], .atsx-select-dropdown li');
                    for (const item of items) {
                        const text = item.innerText.trim();
                        if (text.includes('United Kingdom') && text.includes('+44')) {
                            item.scrollIntoView();
                            item.click();
                            return true;
                        }
                    }
                    return false;
                }""")
                print(f"Clicked United Kingdom (+44): {clicked}")
                await page.wait_for_timeout(500)

        # 2. Normalize and update all textareas
        textareas = await page.query_selector_all("textarea")
        print(f"Found {len(textareas)} textareas to inspect.")

        for idx, ta in enumerate(textareas):
            # Skip hidden autosize measuring textarea
            is_visible = await ta.is_visible()
            val = await ta.input_value()
            if not is_visible or not val.strip():
                print(f"Skipping textarea #{idx} (visible={is_visible}, len={len(val)})")
                continue

            norm_val = normalize_text(val)
            print(f"\n--- Textarea #{idx} (id={await ta.get_attribute('id')}) ---")
            print("ORIGINAL:")
            print(val)
            print("NORMALIZED:")
            print(norm_val)

            # Fill the normalized value using Playwright .fill()
            await ta.fill(norm_val)

            # Also dispatch standard DOM input & change events
            await page.evaluate(
                """({idx, norm_val}) => {
                const ta = document.querySelectorAll('textarea')[idx];
                if (ta) {
                    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                    setter.call(ta, norm_val);
                    ta.dispatchEvent(new Event('input', { bubbles: true }));
                    ta.dispatchEvent(new Event('change', { bubbles: true }));
                    ta.dispatchEvent(new Event('blur', { bubbles: true }));
                }
            }""",
                {"idx": idx, "norm_val": norm_val},
            )

        await page.wait_for_timeout(500)

        # 3. Verify the updated textareas
        print("\n=== VERIFICATION OF LIVE TEXTAREAS ===")
        for idx, ta in enumerate(textareas):
            if await ta.is_visible() and (await ta.input_value()).strip():
                updated_val = await ta.input_value()
                print(f"Verified Textarea #{idx}:")
                print(updated_val)
                print("---")

        # 4. Check Privacy Policy checkbox (prepare for user review)
        cb_checked = await page.evaluate("""() => {
            const cb = document.querySelector('input[type="checkbox"]');
            if (cb && !cb.checked) {
                cb.click();
                cb.dispatchEvent(new Event('change', { bubbles: true }));
            }
            return cb ? cb.checked : false;
        }""")
        print(f"Privacy Policy checkbox status: {cb_checked}")

        # 5. Reconcile Demographic Survey and Work Authorization selects
        print("\n=== RECONCILING DEMOGRAPHIC & WORK AUTH SELECTS ===")
        targets = [
            (0, "What term best describes your gender identity?", "Man"),
            (1, "Do you have a disability?", "No"),
            (2, "What is your race/ethnicity? (Select all that apply)", "East Asian / East Asian British"),
            (
                3,
                "Do you currently have the right to work in the country where the job you are applying for is located?",
                "Yes",
            ),
            (
                4,
                "Do you now, or will you in the future, require sponsorship for employment visa status to work in the country where the job you are applying for is located?",
                "Yes",
            ),
            (
                5,
                "Where did you hear about this opportunity? Choose the option(s) that influenced your decision to apply.",
                "School career development office",
            ),
        ]

        for idx, label, expected_opt in targets:
            # Check current state first
            cur_val = await page.evaluate(
                """(idx) => {
                const selects = document.querySelectorAll('.ud__select');
                const target = selects[idx];
                const selector = target ? (target.querySelector('.ud__select__selector') || target) : null;
                return selector ? (selector.innerText || '').trim() : '';
            }""",
                idx,
            )

            if expected_opt in cur_val:
                print(f"  Field #{idx} '{label[:35]}...' already matches: '{cur_val}'")
                continue

            print(f"  Field #{idx} '{label[:35]}...' mismatch (current: '{cur_val}'). Updating to '{expected_opt}'...")
            await page.evaluate(
                """(idx) => {
                const selects = document.querySelectorAll('.ud__select');
                const target = selects[idx];
                const selector = target.querySelector('.ud__select__selector') || target;
                selector.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window }));
                selector.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true, view: window }));
                selector.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
            }""",
                idx,
            )
            await page.wait_for_timeout(400)

            clicked = await page.evaluate(
                """({expected_opt}) => {
                const dropdowns = Array.from(document.querySelectorAll('.ud__select__dropdown'))
                    .filter(dd => !dd.className.includes('leave') && !dd.className.includes('hidden'));
                const activeDd = dropdowns.length > 0 ? dropdowns[dropdowns.length - 1] : null;
                if (!activeDd) return false;
                const allEls = activeDd.querySelectorAll('*');
                for (const el of allEls) {
                    const text = (el.innerText || '').trim();
                    if (el.children.length === 0 && text === expected_opt) {
                        const clickTarget = el.closest('[class*="option"]') || el.parentElement || el;
                        clickTarget.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window }));
                        clickTarget.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true, view: window }));
                        clickTarget.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
                        return true;
                    }
                }
                return false;
            }""",
                {"expected_opt": expected_opt},
            )
            await page.wait_for_timeout(300)
            await page.keyboard.press("Escape")

            new_val = await page.evaluate(
                """(idx) => {
                const selects = document.querySelectorAll('.ud__select');
                const target = selects[idx];
                const selector = target ? (target.querySelector('.ud__select__selector') || target) : null;
                return selector ? (selector.innerText || '').trim() : '';
            }""",
                idx,
            )
            print(f"  Updated #{idx} result: '{new_val}' (MATCH: {expected_opt in new_val})")

        # Strictly ensure Submit button is NOT clicked
        print("\n[SAFETY PROTOCOL] Review ready. Submit button was NOT clicked. Waiting for user review.")
        return True


if __name__ == "__main__":
    asyncio.run(update_live_fields())
