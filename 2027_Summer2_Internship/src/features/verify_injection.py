import sys
from pathlib import Path

import win32com.client


def verify_injection():
    print("Starting Injection Verification Loop (QA Pipeline)...")
    base_dir = Path(__file__).resolve().parents[2]
    file_path = base_dir / "2027_BCI_Internship_Tracker.xlsx"

    # Locate pristine backup
    backup_dir = base_dir / "Backups"
    candidates = [
        backup_dir / "2027_BCI_Internship_Tracker_5_20260806_131351.xlsx",
        backup_dir / "2027_BCI_Internship_Tracker_20260806_131351.xlsx",
        backup_dir / "2027_BCI_Internship_Tracker (5)_20260806_131351.xlsx",
    ]
    backup_path = next((c for c in candidates if c.exists()), None)

    if not file_path.exists():
        print("ERROR: Target Excel file not found.")
        sys.exit(1)
    if not backup_path or not backup_path.exists():
        print("ERROR: Pristine backup file not found for formatting comparison.")
        sys.exit(1)

    excel = win32com.client.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    wb = None
    wb_back = None
    errors = []

    try:
        wb = excel.Workbooks.Open(str(file_path))
        wb_back = excel.Workbooks.Open(str(backup_path), ReadOnly=True)

        ws_ov = wb.Sheets("1.Overview_Map")
        ws_ov_back = wb_back.Sheets("1.Overview_Map")
        ws_db = wb.Sheets("2.Research_Database")

        # --- Test 1 & 2: Background, Borders & Hyperlink Formatting ---
        # We will check Overview_Map rows 2-25, cols 3-4 (where we typically inject)
        print("Running Test 1 & 2: Format Destruction & Hyperlink Styling...")
        for r in range(2, 25):
            for c in [3, 4]:
                cell = ws_ov.Cells(r, c)
                back_cell = ws_ov_back.Cells(r, c)

                # Check background color mismatch (Edge Case 1)
                if cell.Interior.Color != back_cell.Interior.Color:
                    errors.append(
                        f"[Overview_Map R{r}C{c}] Background color destroyed (Current: {cell.Interior.Color}, Expected: {back_cell.Interior.Color}). Did you run PasteFormats?"
                    )

                # Check hyperlink styling and raw URLs (Edge Cases 2 & 3)
                if cell.Hyperlinks.Count > 0:
                    if cell.Font.Color != 12611584:
                        errors.append(f"[Overview_Map R{r}C{c}] Hyperlink font is not blue (Color: {cell.Font.Color}).")
                    if cell.Font.Underline != 2:
                        errors.append(f"[Overview_Map R{r}C{c}] Hyperlink font is not underlined.")

                    hl = cell.Hyperlinks(1)
                    if hl.TextToDisplay and hl.TextToDisplay.startswith("http"):
                        errors.append(f"[Overview_Map R{r}C{c}] Raw URL exposed as TextToDisplay: {hl.TextToDisplay}")

        # --- Test 3 & 4: Surgical Mapping & Merged Structure ---
        # Check Research_Database to ensure companies are in their correct rows (no sequential overwrite)
        print("Running Test 3 & 4: Surgical Mapping & Structure Integrity...")

        # In a pristine file, each company block is 3 rows.
        expected_companies = {
            2: "Apple",
            5: "Google",
            8: "Google DeepMind",
            11: "Meta (Reality Labs London)",
            14: "Microsoft (Microsoft Research)",
            17: "Samsung AI Center (Cambridge)",
            20: "Snap Inc. (Snap Lab London)",
            23: "Sony Interactive Entertainment (SIE London)",
            26: "BIOS Health",
            29: "CoMind",
            32: "Cogitat",
            35: "Connectome Health",
            38: "CrossSense",
            41: "Cumulus Neuroscience",
            44: "Emteq Labs",
            47: "MyndPlay",
            50: "Neurable",
            53: "OpenBCI",
            56: "Synchron",
            59: "Gaudio Lab",
        }

        for r, expected_name in expected_companies.items():
            cell_val = ws_db.Cells(r, 1).Value
            if cell_val != expected_name:
                errors.append(
                    f"[Research_Database R{r}C1] Surgical Mapping Failure: Expected '{expected_name}', found '{cell_val}'. The merged layout has been overwritten."
                )

        # --- Test 5: Failsafe Telemetry Hidden ---
        print("Running Test 5: Failsafe Columns Hidden...")
        for col in range(7, 12):  # Cols G to K
            if not ws_db.Columns(col).Hidden:
                errors.append(f"[Research_Database] Column {col} is NOT hidden. Failsafe was not executed properly.")

    except Exception as e:
        errors.append(f"Unexpected COM Error during verification: {e!s}")
    finally:
        if wb_back:
            wb_back.Close(SaveChanges=False)
        if wb:
            wb.Close(SaveChanges=False)
        excel.Quit()

    if errors:
        print("\n" + "=" * 50)
        print("VERIFICATION FAILED: Excel Injection Verification Failed!")
        print("=" * 50)
        for err in errors:
            print(f"- {err}")
        print("=" * 50)
        print("ACTION REQUIRED: You must fix the injection script and re-run it until this loop passes with 0 errors.")
        sys.exit(1)
    else:
        print("\n" + "=" * 50)
        print("VERIFICATION PASSED: All Excel Injection Tests (Formatting, Structure, Telemetry) passed perfectly!")
        print("=" * 50)
        sys.exit(0)


if __name__ == "__main__":
    verify_injection()
