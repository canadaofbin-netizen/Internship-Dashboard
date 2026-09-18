#!/usr/bin/env python3
"""
Visible Browser Launcher for Internship Applications.
Directly launches Naver Whale (or standard visible Chrome) with target application URLs
so the user can clearly see and interact with all application tabs on their main screen.
"""

import argparse
import os
import subprocess
import sys

TARGET_APPLICATIONS = {
    "scale_ai": {
        "name": "Scale AI (SWE Intern Summer 2027)",
        "url": "https://job-boards.greenhouse.io/scaleai/jobs/4730846005",
    },
    "graham_capital": {
        "name": "Graham Capital (2027 Summer Internship - London)",
        "url": "https://job-boards.greenhouse.io/grahamcapitalmanagement/jobs/4733835005?gh_jid=4733835005",
    },
    "citi": {
        "name": "Citi (Banking Summer Analyst 2027)",
        "url": "https://citi.wd5.myworkdayjobs.com/en-US/2/job/London--United-Kingdom/Banking--Commercial-Banking--Summer-Analyst--London---United-Kingdom-2027_26993448/apply/applyManually",
    },
    "lseg": {
        "name": "LSEG (Engineering Summer Internship 2027)",
        "url": "https://lseg.wd3.myworkdayjobs.com/en-US/Graduate_Careers/job/London%2C-United-Kingdom/Engineering-Summer-Internship-Programme_R0123389/apply/applyManually",
    },
    "tiktok": {"name": "TikTok (Campus Internship Programme 2027)", "url": "https://lifeattiktok.com/resume/edit"},
    "barclays": {
        "name": "Barclays (Technology Summer Intern - Data & Analytics)",
        "url": "https://barclays.wd3.myworkdayjobs.com/en-US/External_Career_Site_Barclays/job/Canary-Wharf%2C-1-Churchill-Place/XMLNAME-2027-Customer-and-Digital---Data-and-Analytics-Summer-Internship-Programme-London_JR-0000129280/apply/autofillWithResume",
    },
    "orbis": {
        "name": "Orbis Investments (Investment Analyst Intern 2026-2027)",
        "url": "https://vhr-orbis.wd3.myworkdayjobs.com/en-US/Orbis_Careers/job/London-Dorset-Square/Investment-Analyst-Internship-2026-2027_JR564/apply/applyManually?utm_source=Trackr&utm_medium=tracker&utm_campaign=UK_Finance_2027&source=Trackr&employeeContractType=f0623a187241100115b8174985c70000",
    },
    "rystad": {
        "name": "Rystad Energy (Management Consultant Intern 2027)",
        "url": "https://app.the-trackr.com/company/rystad-energy",
    },
}

WHALE_PATH = r"C:\Program Files\Naver\Naver Whale\Application\whale.exe"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def get_browser_executable(preferred="whale"):
    if preferred == "whale" and os.path.exists(WHALE_PATH):
        return WHALE_PATH
    if os.path.exists(CHROME_PATH):
        return CHROME_PATH
    if os.path.exists(WHALE_PATH):
        return WHALE_PATH
    return None


def open_url(url, browser_exe=None):
    if browser_exe and os.path.exists(browser_exe):
        subprocess.Popen([browser_exe, url])
        print(f"[Visible Browser] Opened '{url}' in {os.path.basename(browser_exe)}")
    else:
        # Fallback to system default browser
        if sys.platform == "win32":
            os.startfile(url)
            print(f"[Visible Browser] Opened '{url}' via Windows shell")
        else:
            subprocess.Popen(["xdg-open", url])


def main():
    parser = argparse.ArgumentParser(description="Open visible application tabs in Naver Whale or Chrome.")
    parser.add_argument(
        "--company", choices=list(TARGET_APPLICATIONS.keys()) + ["all"], help="Company key to open, or 'all'"
    )
    parser.add_argument("--url", help="Custom URL to open")
    parser.add_argument(
        "--browser", choices=["whale", "chrome", "default"], default="whale", help="Browser to use (default: whale)"
    )
    args = parser.parse_args()

    browser_exe = get_browser_executable(args.browser)
    if not browser_exe and args.browser != "default":
        print(f"Warning: Preferred browser '{args.browser}' not found. Falling back to default.")

    if args.url:
        open_url(args.url, browser_exe)
    elif args.company == "all":
        print("Opening all active application tabs...")
        for key, app in TARGET_APPLICATIONS.items():
            print(f"-> Opening {app['name']}")
            open_url(app["url"], browser_exe)
    elif args.company:
        app = TARGET_APPLICATIONS[args.company]
        print(f"-> Opening {app['name']}")
        open_url(app["url"], browser_exe)
    else:
        print(
            "Usage: python open_visible_browser.py --company [scale_ai|graham_capital|citi|lseg|tiktok|all] OR --url <URL>"
        )
        print("\nAvailable Companies:")
        for key, app in TARGET_APPLICATIONS.items():
            print(f"  - {key}: {app['name']}")


if __name__ == "__main__":
    main()
