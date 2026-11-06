#!/usr/bin/env python3
"""Validate learning archives; merge daily AI lessons and refresh search metadata."""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from add_lesson import ROOT, CATALOG, atomic_json, read_html


class TextIndex(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)

    def handle_data(self, text):
        if not self.skip:
            self.parts.append(text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    original = CATALOG.read_text(encoding='utf-8')
    data = json.loads(original)
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported learning catalog schema')
    categories = {c['id'] for c in data['categories']}
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    daily = next((c for c in manifest['categories'] if c['id'] == 'learning'), {})
    for report in daily.get('reports', []):
        relative = report['path']
        if report.get('kind') != 'full' or not relative.startswith('reports/learning/'):
            continue
        raw, digest = read_html(ROOT / relative)
        if any(e['sha256'] == digest for t in data['topics'] for e in t['editions']):
            continue
        topic = next((t for t in data['topics'] if t['id'] == 'daily-ai-concepts'), None)
        if topic is None:
            topic = {'id': 'daily-ai-concepts', 'title': '每日 AI 五词精讲',
                     'summary': '从 AI 术语到 Coding Agent 工程机制，结合案例、发音与练习逐期学习。',
                     'category': 'ai', 'tags': ['AI 术语', 'Coding Agent', '原理与实践'], 'editions': []}
            data['topics'].append(topic)
        topic['editions'].append({'id': digest[:16], 'label': report['title'], 'file': relative,
                                 'date': report['date'], 'sha256': digest, 'source_names': []})
        topic['recommended'] = max(topic['editions'], key=lambda e: e['date'])['id']
    ids, digests, paths = set(), set(), set()
    for topic in data['topics']:
        if topic['id'] in ids or topic['category'] not in categories or not topic['editions']:
            raise ValueError(f'Duplicate or invalid topic: {topic["id"]}')
        ids.add(topic['id'])
        texts = []
        edition_ids = set()
        for edition in topic['editions']:
            relative = edition['file']
            target = (ROOT / relative).resolve()
            if not target.is_relative_to(ROOT.resolve()) or not relative.startswith(('study/lessons/', 'reports/learning/')):
                raise ValueError(f'Unsafe lesson path: {relative}')
            raw, digest = read_html(target)
            if edition['sha256'] != digest or digest in digests or relative in paths:
                raise ValueError(f'Duplicate or changed archive: {relative}')
            digests.add(digest)
            paths.add(relative)
            edition_ids.add(edition['id'])
            datetime.strptime(edition['date'], '%Y-%m-%d')
            parser = TextIndex()
            parser.feed(raw.decode('utf-8-sig'))
            texts.append(re.sub(r'\s+', ' ', ' '.join(parser.parts)).strip())
        if topic.get('recommended') not in edition_ids:
            raise ValueError(f'Missing recommended edition: {topic["id"]}')
        topic['updated_at'] = max(e['date'] for e in topic['editions'])
        topic['search_text'] = ' '.join(texts)
    archived_paths = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'study/lessons').rglob('*.html')}
    if archived_paths - paths:
        raise ValueError(f'Unindexed learning HTML: {sorted(archived_paths - paths)}')
    data['topics'].sort(key=lambda t: (t['updated_at'], t['id']), reverse=True)
    data['stats'] = {'topic_count': len(data['topics']), 'document_count': len(paths),
                     'category_count': len({t['category'] for t in data['topics']})}
    before = json.loads(original)
    # Date reflects a real catalog/content change, not just an unchanged daily build.
    if data != before:
        data['updated_at'] = datetime.now(ZoneInfo('Asia/Shanghai')).date().isoformat()
    desired = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.write:
        atomic_json(CATALOG, data)
    elif original != desired:
        raise SystemExit('Learning index needs refresh: run scripts/build_learning_index.py --write')
    print(json.dumps({'status': 'valid', **data['stats']}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
