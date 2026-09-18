import asyncio
import sys

from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")


async def inspect():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print(f"Failed to connect to CDP: {e}", flush=True)
            return

        context = browser.contexts[0]
        print(f"Total open pages in context: {len(context.pages)}", flush=True)

        for i, page in enumerate(context.pages):
            url = page.url
            if not any(k in url for k in ["greenhouse", "scaleai", "myworkdayjobs", "lifeattiktok"]):
                continue

            try:
                title = await asyncio.wait_for(page.title(), timeout=2.0)
            except Exception:
                title = "Timeout/Unknown"

            print("\n==========================================", flush=True)
            print(f"Page {i}: {title} | {url}", flush=True)

            try:
                info = await asyncio.wait_for(
                    page.evaluate("""() => {
                    const results = [];

                    // Helper to format string

                    function strVal(v) {
                        if (v === null || v === undefined) return '';
                        let s = String(v).replace(/\\n/g, ' ').trim();
                        return s.length > 80 ? s.substring(0, 80) + '...' : s;
                    }

                    // 1. Check for uploaded resumes / files
                    const resumeEls = document.querySelectorAll('p.body__secondary, .chosen, .filename, [data-qa="uploaded-filename"]');
                    resumeEls.forEach(el => {
                        const t = el.innerText.trim();
                        if (t.endsWith('.pdf') || t.endsWith('.docx')) {
                            results.push({
                                tag: 'UPLOAD',
                                type: 'file_attached',
                                id: 'resume_attachment',
                                label: 'Resume Attachment',
                                value: t
                            });
                        }
                    });

                    // 2. Form controls: input, textarea, select
                    const els = document.querySelectorAll('input, textarea, select');
                    for (const el of els) {
                        if (el.type === 'hidden') continue;
                        const rect = el.getBoundingClientRect();
                        const isVisible = rect.width > 0 && rect.height > 0;
                        if (!isVisible) continue;

                        let label = '';
                        if (el.labels && el.labels.length > 0) label = el.labels[0].innerText.trim();
                        if (!label && el.id) {
                            const l = document.querySelector(`label[for="${el.id}"]`);
                            if (l) label = l.innerText.trim();
                        }
                        if (!label && el.closest('label')) label = el.closest('label').innerText.trim();
                        if (!label && el.closest('.atsx-form-item')) {
                            const fl = el.closest('.atsx-form-item').querySelector('.atsx-form-item-label, label');
                            if (fl) label = fl.innerText.trim();
                        }
                        if (!label && el.closest('.ud-formily-item')) {
                            const fl = el.closest('.ud-formily-item').querySelector('.ud-formily-item-label, label');
                            if (fl) label = fl.innerText.trim();
                        }
                        if (!label) label = el.getAttribute('aria-label') || el.name || el.id;

                        let val = el.value;

                        // Check React-Select single-value (Greenhouse)
                        const ctrl = el.closest('.select__control');
                        if (ctrl) {
                            const sv = ctrl.querySelector('.select__single-value');
                            if (sv) val = sv.innerText.trim();
                        }

                        // Check Ant Design select (TikTok)
                        const atsx = el.closest('.atsx-select');
                        if (atsx) {
                            const sv = atsx.querySelector('.atsx-select-selection-selected-value, [data-cy="selectedValue"]');
                            if (sv) val = sv.innerText.trim();
                        }

                        // Check ByteDance ud__select (TikTok)
                        const uds = el.closest('.ud__select');
                        if (uds) {
                            const sv = uds.querySelector('.ud__select__selector__value, .ud__select__selector');
                            if (sv) val = sv.innerText.trim();
                        }

                        if (el.type === 'checkbox') {
                            val = el.checked ? 'Checked (True)' : 'Unchecked (False)';
                        }
                        if (el.type === 'radio') {
                            val = el.checked ? `Checked (${el.value || 'True'})` : 'Unchecked';
                        }

                        results.push({
                            tag: el.tagName,
                            type: el.type,
                            id: el.id,
                            label: label ? label.substring(0, 60) : '',
                            value: strVal(val)
                        });
                    }

                    // 3. Check standalone ud__select components (which might not wrap a standard input)
                    const udSelects = document.querySelectorAll('.ud__select');
                    udSelects.forEach((uds, idx) => {
                        const item = uds.closest('.ud-formily-item');
                        const label = item ? (item.querySelector('.ud-formily-item-label') || {}).innerText : '';
                        const sv = uds.querySelector('.ud__select__selector__value, .ud__select__selector');
                        const val = sv ? sv.innerText.trim() : '';
                        // Avoid duplicates if already captured
                        const already = results.some(r => r.label === (label || '').trim() && r.value === strVal(val));
                        if (!already && label) {
                            results.push({
                                tag: 'UD_SELECT',
                                type: 'dropdown',
                                id: `ud_select_${idx}`,
                                label: (label || '').trim().substring(0, 60),
                                value: strVal(val)
                            });
                        }
                    });

                    return results;
                }"""),
                    timeout=3.0,
                )

                for item in info:
                    print(
                        f"  [{item['tag']}:{item['type']}] '{item['label']}' (id={item['id']}) => '{item['value']}'",
                        flush=True,
                    )

            except Exception as e:
                print(f"  Error reading page: {e}", flush=True)


if __name__ == "__main__":
    asyncio.run(inspect())
