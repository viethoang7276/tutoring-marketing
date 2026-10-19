#!/usr/bin/env python3
"""Refresh public quiz discovery/metadata without reproducing question banks.

Requires Python 3, curl and beautifulsoup4. Output is a reviewable new snapshot;
the existing manifest and Google Sheet are never modified automatically.
"""
import argparse
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
ROOTS = {
    'Economics': 'https://www.proprofs.com/quiz-school/topic/economics',
    'Accounting': 'https://www.proprofs.com/quiz-school/topic/accounting',
    'Statistics': 'https://www.proprofs.com/quiz-school/topic/statistics-and-probability',
    'Corporate finance': 'https://www.proprofs.com/quiz-school/topic/corporate-finance',
}

def fetch(url):
    result = subprocess.run(['curl', '--fail', '--silent', '--show-error',
                             '--max-time', '45', '-L', url], capture_output=True, text=True)
    time.sleep(1)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    manifest = ROOT / 'data/research/proprofs/sources.json'
    if args.output.resolve() == manifest.resolve():
        parser.error('Write a new snapshot and review it before replacing the saved manifest.')
    old = json.loads(manifest.read_text())
    ids = {row['url']: row['id'] for row in old}
    next_id = max(int(row['id'].split('-')[1]) for row in old) + 1
    records, errors = [], []
    for subject, url in ROOTS.items():
        try:
            page = BeautifulSoup(fetch(url), 'html.parser')
            heading = next((h for h in page.find_all(['h2','h3'])
                            if 'Top Trending' in h.get_text()), None)
            if heading is None:
                raise RuntimeError('Top Trending heading missing; inspect layout manually.')
            seen = set()
            for node in heading.next_elements:
                if getattr(node, 'name', None) == 'h2':
                    break
                if getattr(node, 'name', None) != 'a' or not node.get('href'):
                    continue
                link = urljoin(url, node['href'])
                title = node.get_text(' ', strip=True)
                if 'story.php?' not in link or link in seen or not title:
                    continue
                seen.add(link)
                records.append(dict(category=subject, title=title, url=link,
                                    discovered_on=url, section='Top Trending', rank=len(seen)))
            if not seen:
                raise RuntimeError('No quiz links found; inspect layout manually.')
        except RuntimeError as exc:
            errors.append({'url': url, 'error': str(exc)})
    banking = next(row for row in old if row['id']=='PP-21')
    records.append({k: banking[k] for k in ['category','title','url','discovered_on','section','rank']})
    for row in records:
        if row['url'] not in ids:
            ids[row['url']] = f'PP-{next_id:02d}'
            next_id += 1
        row.update(id=ids[row['url']], crawl_date=datetime.now(timezone.utc).date().isoformat())
        try:
            html = fetch(row['url'])
            soup = BeautifulSoup(html, 'html.parser')
            row.update(fetch_status='ok', html_sha256=hashlib.sha256(html.encode()).hexdigest(),
                       visible_questions=sum(bool(n.find_parent('form'))
                                             and 'nickname' not in n.get_text(' ',strip=True).lower()
                                             for n in soup.select('.question_count_text')))
        except RuntimeError as exc:
            row.update(fetch_status='failed', error=str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({'sources':records,'discovery_errors':errors}, indent=2)+'\n')
    print(f'Saved {len(records)} source records; {len(errors)} discovery errors: {args.output}')
    if errors or any(row['fetch_status']!='ok' for row in records):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
