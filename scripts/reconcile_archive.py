#!/usr/bin/env python3
"""Reconcile and validate the public AI Daily Hub archive.

The program scans only reports/*.html, never private workspaces or external services.
It preserves existing entries, refuses incomplete HTML, and never replaces a report.
"""
from __future__ import annotations
import argparse
from datetime import datetime
from html import unescape
import json
import os
from pathlib import Path
import re
import tempfile
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "manifest.json"
REPORTS = ROOT / "reports"
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def validated_html(path: Path) -> str:
    raw = path.read_bytes()
    if len(raw) < 250:
        raise ValueError(f"HTML too short: {path}")
    html = raw.decode("utf-8-sig")
    low = html.lower()
    if not all(tag in low for tag in ("<html", "<body", "</body>", "</html>")):
        raise ValueError(f"Missing full HTML structure: {path}")
    if not low.rstrip().endswith("</html>"):
        raise ValueError(f"HTML looks truncated: {path}")
    if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", html):
        raise ValueError(f"Private key detected: {path}")
    if re.search(r"(?:github_pat_[A-Za-z0-9_]{60,}|ghp_[A-Za-z0-9]{36,})", html):
        raise ValueError(f"GitHub credential detected: {path}")
    if "sandbox:/mnt/data/" in html:
        raise ValueError(f"Ephemeral sandbox URL in public HTML: {path}")
    match = TITLE.search(html)
    return unescape(re.sub(r"\s+", " ", match.group(1))).strip() if match else path.stem


def report_date(path: Path) -> str | None:
    parts = DATE.findall(path.stem)
    if not parts:
        return None
    result = parts[-1]
    try:
        datetime.strptime(result, "%Y-%m-%d")
    except ValueError:
        return None
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Safely add unindexed full HTML files")
    args = ap.parse_args()
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    categories = data["categories"]
    topics = {c["id"]: c for c in categories}
    existing: set[str] = set()
    for c in categories:
        for r in c.get("reports", []):
            p = r["path"]
            if p in existing:
                raise ValueError(f"Duplicate path in manifest: {p}")
            existing.add(p)
            absolute = (ROOT / p).resolve()
            if not absolute.is_relative_to(REPORTS.resolve()) or not absolute.is_file():
                raise ValueError(f"Missing or unsafe manifest path: {p}")
            validated_html(absolute)
            datetime.strptime(r["date"], "%Y-%m-%d")
    missing = []
    warnings = []
    for f in sorted(REPORTS.rglob("*.html")):
        path = f.relative_to(ROOT).as_posix()
        if path in existing:
            continue
        parts = f.relative_to(REPORTS).parts
        topic = "official-ai" if len(parts) == 1 else parts[0]
        date = report_date(f)
        if topic not in topics or not date:
            warnings.append(f"Unrecognized report path or date: {path}")
            continue
        title = validated_html(f)
        if any(r["date"] == date for r in topics[topic].get("reports", [])):
            warnings.append(f"Same-date report requires manual review: {path}")
            continue
        missing.append((topic, date, title, path))
    if warnings:
        for warning in warnings:
            print("WARNING:", warning)
    if missing:
        for topic, date, title, path in missing:
            print("UNINDEXED:", topic, date, path)
        if args.write:
            for topic, date, title, path in missing:
                c = topics[topic]
                c.setdefault("reports", []).append({
                    "date": date, "title": title, "label": date,
                    "path": path, "kind": "full"
                })
                c["reports"].sort(key=lambda r: r["date"], reverse=True)
                if c.get("source_status") == "missing_original":
                    c["source_status"] = "partial_archive"
            data["updated_at"] = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
        else:
            raise SystemExit("Run with --write to add verified unindexed reports")
    count = sum(len(c.get("reports", [])) for c in categories)
    data.setdefault("counts", {})["topic_count"] = len(categories)
    data["counts"]["verified_full_reports"] = count
    if args.write:
        new_content = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        old_content = INDEX.read_text(encoding="utf-8")
        if new_content != old_content:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=ROOT, prefix=".manifest.",
                suffix=".tmp", delete=False
            ) as tmp:
                tmp.write(new_content)
                name = tmp.name
            os.replace(name, INDEX)
            print(f"UPDATED: manifest, {count} full HTML reports")
        else:
            print(f"NO CHANGE: {count} full HTML reports")
    else:
        if data["counts"]["topic_count"] != len(categories) or data["counts"]["verified_full_reports"] != count:
            raise ValueError("Incorrect counts in manifest")
        print(f"VALID: {len(categories)} topics; {count} HTML reports")
    if warnings:
        raise SystemExit("Some report files were not indexed; manual review needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
