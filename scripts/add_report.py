#!/usr/bin/env python3
"""Import a complete HTML briefing into the AI Daily Hub static archive.

Run locally from the repository root, then git add/commit/push.
GitHub Pages deploys committed static files; it does not run the report generator.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a complete HTML report.")
    parser.add_argument("--topic", required=True, help="One of the manifest categories")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD; use the end date for a range")
    parser.add_argument("--file", required=True, type=Path, help="Existing complete HTML source")
    parser.add_argument("--title", required=True, help="Display title")
    parser.add_argument("--label", help="Optional short period label")
    args = parser.parse_args()

    try:
        report_date = dt.date.fromisoformat(args.date)
    except ValueError as exc:
        parser.error("Invalid --date: " + str(exc))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        parser.error("--date must have YYYY-MM-DD shape")

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    category = next((c for c in data["categories"] if c["id"] == args.topic), None)
    if category is None:
        parser.error("Unknown topic; check manifest.json")

    src = args.file.expanduser().resolve()
    if not src.is_file():
        parser.error("Input HTML does not exist: " + str(src))
    raw = src.read_bytes()
    if len(raw) < 500:
        parser.error("HTML source seems too small for a complete report")
    try:
        sample = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        parser.error("HTML must be UTF-8")
    lower = sample.lower()
    if "<html" not in lower or "</html>" not in lower or "<body" not in lower:
        parser.error("Expected a complete HTML document, not an excerpt")
    if not sample.strip().endswith("</html>"):
        parser.error("HTML has trailing content or appears truncated")

    dest_rel = "reports/" + args.topic + "/" + args.date + ".html"
    dest = ROOT / dest_rel
    if dest.exists() or any(x["path"] == dest_rel for c in data["categories"] for x in c.get("reports", [])):
        parser.error("Report already exists; edit it deliberately rather than replacing silently")

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    entry = {
        "date": args.date,
        "title": args.title,
        "label": args.label or args.date,
        "path": dest_rel,
        "kind": "full",
    }
    category.setdefault("reports", []).append(entry)
    category["reports"].sort(key=lambda x: x["date"], reverse=True)
    category["source_status"] = "full"
    data["updated_at"] = dt.datetime.now(dt.timezone.utc).date().isoformat()
    data["counts"] = {
        "topic_count": len(data["categories"]),
        "verified_full_reports": sum(len(c.get("reports", [])) for c in data["categories"]),
    }

    # Atomic index update. Content integrity still requires editorial review.
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=MANIFEST.parent, prefix=".manifest.", suffix=".tmp", delete=False
    ) as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.write("\n")
        temp_name = tmp.name
    os.replace(temp_name, MANIFEST)
    print("Added:", dest_rel)
    print("Topic:", category["name"])
    print("Reports:", data["counts"]["verified_full_reports"])
    print("Next: review the report; git add manifest.json", dest_rel, "&& git commit && git push")
    return 0


if __name__ == "__main__":
    sys.exit(main())
