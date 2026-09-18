#!/usr/bin/env python3
"""
CEO Control Tower Orchestration CLI & Management Utility.
Manages child chatroom sessions, automated handoff generation with Ground Truth injection,
session return ingestion, and SSOT Excel compilation.
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

WORKSPACE_ROOT = Path(r"G:\My Drive\Kyubin_Yun_Workspace\04_Internship")
REGISTRY_PATH = WORKSPACE_ROOT / "00_CEO_Control_Tower" / "CHATROOM_REGISTRY.json"
SSOT_EXCEL_PATH = WORKSPACE_ROOT / "Master_Internship_Tracker_2027_SSOT.xlsx"
BRIEFS_DIR = WORKSPACE_ROOT / "00_CEO_Control_Tower" / "sessions" / "briefs"
RETURNS_DIR = WORKSPACE_ROOT / "00_CEO_Control_Tower" / "sessions" / "returns"

VALID_PRIORITIES = {"URGENT", "HIGH", "MEDIUM", "LOW"}
VALID_STATUSES = {
    "READY_FOR_DISPATCH",
    "ACTIVE",
    "SUCCESS_REVIEW_READY",
    "COMPLETED",
    "BLOCKED",
    "FAILED",
}


def load_registry(path: Path = REGISTRY_PATH) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Registry file not found at: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_registry(data: dict, path: Path = REGISTRY_PATH) -> None:
    data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def list_rooms(track_filter: str = None, status_filter: str = None) -> list[dict]:
    reg = load_registry()
    rooms = reg.get("chatrooms", [])
    filtered = []
    for r in rooms:
        if track_filter and r.get("track") != track_filter:
            continue
        if status_filter and r.get("status") != status_filter:
            continue
        filtered.append(r)
    return filtered


def print_room_table(rooms: list[dict]) -> None:
    print("\n" + "=" * 90)
    print(f"{'Session ID':<22} | {'Track':<9} | {'Priority':<8} | {'Status':<18} | {'Title'}")
    print("-" * 90)
    for r in rooms:
        sid = r.get("session_id", "N/A")
        trk = r.get("track", "N/A")
        prio = r.get("priority", "N/A")
        stat = r.get("status", "N/A")
        title = r.get("title", "N/A")
        if len(title) > 30:
            title = title[:27] + "..."
        print(f"{sid:<22} | {trk:<9} | {prio:<8} | {stat:<18} | {title}")
    print("=" * 90 + "\n")


def register_room(
    session_id: str,
    track: str,
    title: str,
    priority: str = "HIGH",
    target_companies: list[str] = None,
    outcome_summary: str = "",
) -> dict:
    # 1. Validate session_id
    if not session_id or not isinstance(session_id, str):
        raise ValueError("session_id must be a non-empty string.")
    if not re.match(r"^[A-Za-z0-9_-]+$", session_id) or not (3 <= len(session_id) <= 64):
        raise ValueError(
            f"Invalid session ID '{session_id}'. Must be 3-64 characters alphanumeric, hyphens, or underscores (no slashes or path characters)."
        )

    reg = load_registry()

    # 2. Validate track
    valid_tracks = set(reg.get("tracks", {}).keys())
    if track not in valid_tracks:
        raise ValueError(f"Invalid track '{track}'. Must be one of: {sorted(valid_tracks)}")

    # 3. Validate priority
    prio_upper = priority.upper()
    if prio_upper not in VALID_PRIORITIES:
        raise ValueError(f"Invalid priority '{priority}'. Must be one of: {sorted(VALID_PRIORITIES)}")

    rooms = reg.setdefault("chatrooms", [])

    # Check if already exists
    for r in rooms:
        if r.get("session_id") == session_id:
            raise ValueError(f"Session with ID '{session_id}' already exists!")

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    brief_rel = f"00_CEO_Control_Tower/sessions/briefs/{session_id}_brief.md"

    new_room = {
        "session_id": session_id,
        "track": track,
        "title": title,
        "status": "READY_FOR_DISPATCH",
        "priority": prio_upper,
        "target_companies": target_companies or [],
        "brief_file": brief_rel,
        "return_file": None,
        "created_at": now_iso,
        "updated_at": now_iso,
        "outcome_summary": outcome_summary,
    }
    rooms.append(new_room)
    save_registry(reg)
    print(f"✅ Registered new chatroom session: {session_id} [{track}]")
    return new_room


def generate_handoff(session_id: str) -> Path:
    reg = load_registry()
    target_room = None
    for r in reg.get("chatrooms", []):
        if r.get("session_id") == session_id:
            target_room = r
            break

    if not target_room:
        raise ValueError(f"Session ID '{session_id}' not found in registry!")

    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    brief_path = WORKSPACE_ROOT / target_room.get(
        "brief_file", f"00_CEO_Control_Tower/sessions/briefs/{session_id}_brief.md"
    )
    brief_path.parent.mkdir(parents=True, exist_ok=True)

    targets_str = ", ".join(target_room.get("target_companies", [])) or "Specified in Tracker"

    content = f"""# Mission Handoff Brief: {session_id}

- **Session ID**: `{session_id}`
- **Track**: `{target_room.get("track", "N/A")}`
- **Priority**: `{target_room.get("priority", "HIGH")}`
- **Target Organization(s)**: {targets_str}
- **Mission Title**: {target_room.get("title", "N/A")}
- **Initial Status**: `{target_room.get("status", "READY_FOR_DISPATCH")}`
- **Summary**: {target_room.get("outcome_summary", "N/A")}

---

## 1. Candidate Ground Truth Baseline (SSOT Injection)

- **Legal Name**: Kyubin Yun (윤규빈) | First Name: Kyubin / Last Name: Yun
- **Preferred Name**: *(None / Blank - Do not fill Jeff)*
- **Official Email**: `zcjtyun@ucl.ac.uk` (UCL Academic ID for all portals)
- **UK Mobile Phone**: `+44 7787 442404` (Country Code: `+44`, UK Mobile)
- **Current UK Address**: 40 Merchant St, Brent Cross, Suite 638, London, NW2 8BB
- **University**: University College London (UCL)
- **Degree**: Bachelor of Science (BSc) in Psychology and Language Sciences
- **Graduation Date**: June 2028 (Penultimate Year Class of 2028)
- **Academic Grade**: Honours (Achieved/Predicted: 70.5/100)
- **UK Work Authorization**: Yes (UK Student Route Visa - full-time summer work legally permitted without employer sponsorship)
- **Graduate Route**: Eligible for 2-Year Unconditional Post-Study Work Visa (Zero sponsorship required upon graduation)
- **Standard Password**: `Jeff0825!!` (General portals)
- **Workday Password**: `Jeff0825!!!!` (Workday 12+ characters requirement)
- **Resume PDF**: [Kyubin_Yun_Resume_2027.pdf](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/01_Resumes/Kyubin_Yun_Resume_2027.pdf) (Local: `g:\\My Drive\\Kyubin_Yun_Workspace\\04_Internship\\01_Resumes\\Kyubin_Yun_Resume_2027.pdf`)
- **GitHub**: `https://github.com/canadaofbin-netizen`
- **LinkedIn**: `https://www.linkedin.com/in/kyubin-yun-495a33301/`

---

## 2. Hard Governance Directives

1. **Zero Auto-Submit**:
   - Every application MUST stop at the Review / Pre-submit stage.
   - NEVER click final Submit.
2. **Visible Naver Whale Browser**:
   - Must operate via visible Whale browser window (`C:\\Program Files\\Naver\\Naver Whale\\Application\\whale.exe` or CDP `localhost:9222`).
   - Headless/temp virtual browser is strictly prohibited.
3. **Form Text Normalization Protocol**:
   - All bullet points must be standardized to `• ` (`\\u2022 `).
   - Unwrap accidental mid-sentence line breaks from PDFs.
4. **SSOT Master Tracker Reference**:
   - Consult [Master_Internship_Tracker_2027_SSOT.xlsx](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/Master_Internship_Tracker_2027_SSOT.xlsx) for company data.

---

## 3. Required Return Deliverable

Upon completing your designated mission, output a formatted `[MISSION COMPLETION DOSSIER]` containing:
- Specific actions taken and portal Review screen status
- 0% discrepancy verification audit against Ground Truth
- Discovered recruiters, URLs, or deadline updates
- Clear instruction for user Kyubin Yun for final submission.
"""
    brief_path.write_text(content, encoding="utf-8")
    print(f"📄 Generated Mission Handoff Brief at: {brief_path}")
    return brief_path


def sync_return(session_id: str, status: str, summary: str, return_file: Path = None) -> None:
    # 1. Validate status
    stat_upper = status.upper()
    if stat_upper not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {sorted(VALID_STATUSES)}")

    # 2. Validate return_file existence if provided
    if return_file is not None:
        rf_path = Path(return_file)
        if not rf_path.exists():
            raise FileNotFoundError(f"Specified return file does not exist: {return_file}")

    reg = load_registry()
    target_room = None
    for r in reg.get("chatrooms", []):
        if r.get("session_id") == session_id:
            target_room = r
            break

    if not target_room:
        raise ValueError(f"Session ID '{session_id}' not found in registry!")

    RETURNS_DIR.mkdir(parents=True, exist_ok=True)
    ret_rel = f"00_CEO_Control_Tower/sessions/returns/{session_id}_return.md"
    ret_path = WORKSPACE_ROOT / ret_rel

    if return_file and Path(return_file).exists():
        content = Path(return_file).read_text(encoding="utf-8")
    else:
        content = f"""# Mission Completion Return Dossier: {session_id}

- **Session ID**: `{session_id}`
- **Track**: `{target_room.get("track", "N/A")}`
- **Status**: `{stat_upper}`
- **Timestamp**: {datetime.datetime.now(datetime.timezone.utc).isoformat()}
- **Execution Summary**:
  {summary}
- **SSOT Impact**:
  Synchronized with `Master_Internship_Tracker_2027_SSOT.xlsx`.
"""
    ret_path.write_text(content, encoding="utf-8")

    target_room["status"] = stat_upper
    target_room["outcome_summary"] = summary
    target_room["return_file"] = ret_rel
    target_room["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    save_registry(reg)
    print(f"🔄 Synchronized return dossier for session {session_id} (Status: {stat_upper})")


def print_status_summary() -> None:
    reg = load_registry()
    tracks = reg.get("tracks", {})
    rooms = reg.get("chatrooms", [])

    print("\n" + "=" * 80)
    print(" 👑 CEO CONTROL TOWER - EXECUTIVE SYSTEM STATUS")
    print("=" * 80)
    print(f"Candidate : {reg.get('candidate')} ({reg.get('degree')})")
    print(f"Master SSOT: {SSOT_EXCEL_PATH.name} (Exists: {SSOT_EXCEL_PATH.exists()})")
    print(f"Updated At : {reg.get('updated_at')}")
    print("-" * 80)
    print("Track Breakdown:")
    for tid, tinfo in tracks.items():
        print(
            f"  [{tid}] {tinfo.get('name'):<35} | Targets: {tinfo.get('target_count'):<4} | Sheet: {tinfo.get('sheet_ref')}"
        )
    print("-" * 80)
    print(f"Registered Child Chatrooms: {len(rooms)} total")
    status_counts = {}
    for r in rooms:
        s = r.get("status", "UNKNOWN")
        status_counts[s] = status_counts.get(s, 0) + 1
    for st, cnt in status_counts.items():
        print(f"  - {st:<22}: {cnt} session(s)")
    print("=" * 80 + "\n")


def build_ssot() -> None:
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    from consolidate_excel_ssot import build_master_ssot

    build_master_ssot()


def main():
    parser = argparse.ArgumentParser(description="CEO Control Tower Orchestration CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: list
    p_list = subparsers.add_parser("list", help="List registered child chatrooms")
    p_list.add_argument("--track", help="Filter by track ID (e.g. TRACK-B)")
    p_list.add_argument("--status", help="Filter by status (e.g. COMPLETED)")

    # Command: register
    p_reg = subparsers.add_parser("register", help="Register a new child chatroom")
    p_reg.add_argument("--session-id", required=True, help="Unique session ID (e.g. ROOM-UK-AMAZON-004)")
    p_reg.add_argument("--track", required=True, help="Track ID (TRACK-A, TRACK-B, TRACK-C, TRACK-D)")
    p_reg.add_argument("--title", required=True, help="Descriptive title of the mission")
    p_reg.add_argument("--priority", default="HIGH", help="Priority (URGENT, HIGH, MEDIUM, LOW)")
    p_reg.add_argument("--targets", nargs="*", default=[], help="Target company or organization names")
    p_reg.add_argument("--summary", default="", help="Initial mission objective summary")

    # Command: handoff
    p_hand = subparsers.add_parser("handoff", help="Generate mission handoff brief for a child chatroom")
    p_hand.add_argument("--session-id", required=True, help="Session ID to generate handoff for")

    # Command: sync-return
    p_ret = subparsers.add_parser("sync-return", help="Sync completion return from child chatroom")
    p_ret.add_argument("--session-id", required=True, help="Session ID")
    p_ret.add_argument("--status", default="COMPLETED", help="Execution status (COMPLETED, BLOCKED, etc.)")
    p_ret.add_argument("--summary", required=True, help="Summary of achievements/outcomes")
    p_ret.add_argument("--return-file", help="Path to detailed markdown return file (optional)")

    # Command: status
    subparsers.add_parser("status", help="Print executive system status overview")

    # Command: build-ssot
    subparsers.add_parser("build-ssot", help="Recompile Master SSOT Excel workbook")

    args = parser.parse_args()

    if args.command == "list":
        rooms = list_rooms(args.track, args.status)
        print_room_table(rooms)
    elif args.command == "register":
        register_room(
            session_id=args.session_id,
            track=args.track,
            title=args.title,
            priority=args.priority,
            target_companies=args.targets,
            outcome_summary=args.summary,
        )
    elif args.command == "handoff":
        generate_handoff(args.session_id)
    elif args.command == "sync-return":
        sync_return(
            session_id=args.session_id,
            status=args.status,
            summary=args.summary,
            return_file=Path(args.return_file) if args.return_file else None,
        )
    elif args.command == "status":
        print_status_summary()
    elif args.command == "build-ssot":
        build_ssot()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
