#!/usr/bin/env python3
"""Archive an intact learning HTML and merge its metadata into study/catalog.json."""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'study/catalog.json'


def read_html(path: Path) -> tuple[bytes, str]:
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    low = text.lower()
    if len(raw) < 250 or not all(x in low for x in ('<html', '<body', '</body>', '</html>')):
        raise ValueError(f'Expected a complete UTF-8 learning HTML: {path}')
    if not low.rstrip().endswith('</html>'):
        raise ValueError(f'HTML appears truncated: {path}')
    if re.search(r'(?:src|href)\s*=\s*[\"\'](?:sandbox:|file:)', text, re.I):
        raise ValueError(f'Local-only resource link in HTML: {path}')
    if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|github_pat_[A-Za-z0-9_]{60,}|ghp_[A-Za-z0-9]{36,}', text):
        raise ValueError(f'Credential marker in HTML: {path}')
    return raw, hashlib.sha256(raw).hexdigest()


def atomic_json(path: Path, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if path.exists() and path.read_text(encoding='utf-8') == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as f:
        f.write(text)
        name = f.name
    os.replace(name, path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', type=Path, required=True)
    ap.add_argument('--topic', required=True, help='Stable topic slug')
    ap.add_argument('--title', required=True, help='Topic title')
    ap.add_argument('--summary', default='')
    ap.add_argument('--category', required=True)
    ap.add_argument('--tags', nargs='*', default=[])
    ap.add_argument('--edition-label', required=True)
    ap.add_argument('--date', required=True, help='Original lesson date, YYYY-MM-DD')
    ap.add_argument('--source-name', help='Original filename, not a private URL')
    ap.add_argument('--recommend', action='store_true')
    ap.add_argument('--existing-path', help='Reuse an existing identical repository HTML')
    args = ap.parse_args()
    if not re.fullmatch(r'[a-z][a-z0-9-]*', args.topic):
        raise ValueError('Topic must be a lowercase ASCII slug')
    datetime.strptime(args.date, '%Y-%m-%d')
    raw, digest = read_html(args.input)
    data = json.loads(CATALOG.read_text(encoding='utf-8'))
    if args.category not in {c['id'] for c in data['categories']}:
        raise ValueError('Unknown category; add it explicitly to catalog.json first')
    before = json.dumps(data, ensure_ascii=False, sort_keys=True)
    source_name = Path(args.source_name or args.input.name).name
    existing_edition = next((e for t in data['topics'] for e in t['editions'] if e['sha256'] == digest), None)
    topic = next((t for t in data['topics'] if t['id'] == args.topic), None)
    if existing_edition is not None:
        if topic is None or existing_edition not in topic['editions']:
            raise ValueError('Identical content already belongs to a different topic; reuse its existing entry')
        existing_edition['source_names'] = sorted(set(existing_edition.get('source_names', []) + [source_name]))
        edition = existing_edition
    else:
        relative = args.existing_path or f'study/lessons/{args.topic}/{digest[:16]}.html'
        target = (ROOT / relative).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not relative.startswith(('study/lessons/', 'reports/learning/')):
            raise ValueError('Unsafe lesson path')
        if args.existing_path:
            if not target.is_file() or read_html(target)[1] != digest:
                raise ValueError('Existing repository HTML does not match input')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != raw:
                raise ValueError('Archive path collision')
            target.write_bytes(raw)
        edition = {'id': digest[:16], 'label': args.edition_label, 'file': relative,
                   'date': args.date, 'sha256': digest, 'source_names': [source_name]}
        if topic is None:
            topic = {'id': args.topic, 'title': args.title, 'summary': args.summary,
                     'category': args.category, 'tags': args.tags, 'editions': [],
                     'recommended': edition['id'], 'updated_at': args.date}
            data['topics'].append(topic)
        topic['editions'].append(edition)
    if args.recommend:
        topic['recommended'] = edition['id']
    topic['updated_at'] = max(e['date'] for e in topic['editions'])
    if json.dumps(data, ensure_ascii=False, sort_keys=True) != before:
        data['updated_at'] = datetime.now(ZoneInfo('Asia/Shanghai')).date().isoformat()
        atomic_json(CATALOG, data)
        print(json.dumps({'status': 'updated', 'topic': topic['id'], 'file': edition['file']}, ensure_ascii=False))
    else:
        print(json.dumps({'status': 'unchanged', 'topic': topic['id'], 'file': edition['file']}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
