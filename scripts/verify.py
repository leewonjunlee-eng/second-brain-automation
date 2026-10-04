#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import os

ROOT = Path(__file__).parents[1]
COMMANDS = [
    ([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py'], 'unittest discover'),

    ([sys.executable, 'scripts/check_release.py'], 'release'),
]

def main():
    for command, name in COMMANDS:
        print(f'[{name}] {" ".join(command)}', flush=True)
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            raise SystemExit(result.returncode)
    for timezone in ('UTC', 'Asia/Seoul'):
        print(f'[node TZ={timezone}]', flush=True)
        env = os.environ.copy(); env['TZ'] = timezone
        result = subprocess.run(['node', '--test', 'tests/date.test.mjs'], cwd=ROOT, env=env)
        if result.returncode:
            raise SystemExit(result.returncode)
    for svg in (ROOT / 'assets').glob('*.svg'):
        ET.parse(svg)
    with tempfile.TemporaryDirectory() as directory:
        print('[capture]', flush=True)
        result = subprocess.run([
            sys.executable, 'examples/capture.py', 'title', 'body', '--root', directory
        ], cwd=ROOT)
        if result.returncode:
            raise SystemExit(result.returncode)
    print('검증 완료: capture, scanner, Node, release, SVG XML, CLI 임시 root')

if __name__ == '__main__':
    main()
