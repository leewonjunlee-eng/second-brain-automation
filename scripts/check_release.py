#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ID = re.compile(r'\b((?:AUT|INC)-\d{2})\b')
DEFINITION = re.compile(r'^\|\s*((?:AUT|INC)-\d{2})\s*\|', re.M)
FORBIDDEN_NAME = re.compile(r'(^|[._-])(\.env|auth|jobs|credential|credentials|db|log)([._-]|$)', re.I)
SECRET = re.compile(r'(?:BEGIN [A-Z ]+ ' + 'PRIVATE' + r' KEY|ghp_' + r'[A-Za-z0-9]{20,}|sk-' + r'[A-Za-z0-9]{20,})')
HOME_PATH = re.compile(r'(?<![A-Za-z0-9])/' + '(?:home|root)' + r'/[A-Za-z0-9_.-]+')
EMAIL = re.compile(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b')
CONTACT = re.compile(r'(?<!\d)(?:\+?82[- ]?10|01[016789])[- ]?\d{3,4}[- ]?\d{4}(?!\d)')
PRIVATE_IP = re.compile(r'\b(?:' + '10' + r'\.\d{1,3}|192' + r'\.168|172' + r'\.(?:1[6-9]|2\d|3[0-1]))(?:\.\d{1,3}){2}\b')

def scan(root: Path):
    bad = []
    files = [p for p in root.rglob('*') if p.is_file() and not any(x in p.parts for x in ('.git', 'node_modules', '__pycache__'))]
    definitions = []
    for p in files:
        rel = p.relative_to(root)
        if FORBIDDEN_NAME.search(p.name) or p.suffix.lower() in {'.pem', '.key', '.sqlite', '.db', '.log'}:
            bad.append(f'금지 파일명: {rel}')
        text = p.read_text(errors='ignore')
        if SECRET.search(text) or HOME_PATH.search(text) or EMAIL.search(text) or CONTACT.search(text) or PRIVATE_IP.search(text):
            bad.append(f'민감 패턴: {rel}')
        if p.suffix.lower() == '.md':
            definitions.extend((x, rel) for x in DEFINITION.findall(text))
            anchors = set(re.findall(r'<a\s+id=["\']([^"\']+)', text, re.I))
            anchors |= {re.sub(r'[^a-z0-9가-힣 -]', '', h.lower()).strip().replace(' ', '-') for h in re.findall(r'^#{1,6}\s+(.+)$', text, re.M)}
            for target, anchor in re.findall(r'!?\[[^]]*\]\(([^)#\s]+)(?:#([^\s)]+))?[^)]*\)', text):
                if '://' in target:
                    continue
                target_path = (p.parent / target).resolve()
                try:
                    target_path.relative_to(root.resolve())
                    inside_root = True
                except ValueError:
                    inside_root = False
                if not inside_root or not target_path.exists():
                    bad.append(f'끊긴 경로: {rel} -> {target}')
                if anchor and inside_root and target_path.exists():
                    target_text = target_path.read_text(errors='ignore')
                    target_anchors = set(re.findall(r'<a\s+id=["\']([^"\']+)', target_text, re.I))
                    target_anchors |= {re.sub(r'[^a-z0-9가-힣 -]', '', h.lower()).strip().replace(' ', '-') for h in re.findall(r'^#{1,6}\s+(.+)$', target_text, re.M)}
                    if anchor not in target_anchors:
                        bad.append(f'끊긴 anchor: {rel} -> {target}#{anchor}')
    seen = {}
    for value, rel in definitions:
        if value in seen:
            bad.append(f'중복 ID: {value} ({seen[value]}, {rel})')
        seen[value] = rel
    for prefix, required in (('AUT', 18), ('INC', 16)):
        nums = sorted(int(value.split('-')[1]) for value in seen if value.startswith(prefix))
        if not nums or nums != list(range(1, required + 1)):
            bad.append(f'비연속 ID: {prefix}')
    return bad, len(files), len(definitions)

if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).parents[1]
    bad, files, ids = scan(root)
    if bad:
        print('\n'.join(bad))
        raise SystemExit(1)
    print(f'release: {files} files, {ids} stable IDs, links/anchors/patterns passed')
