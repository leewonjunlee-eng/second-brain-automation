import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCANNER = Path(__file__).parents[1] / 'scripts' / 'check_release.py'

def run(root):
    return subprocess.run([sys.executable, str(SCANNER), str(root)], capture_output=True, text=True)

def good(root):
    rows = [f'| AUT-{i:02d} |' for i in range(1, 19)] + [f'| INC-{i:02d} |' for i in range(1, 17)]
    (root / 'README.md').write_text('\n'.join(rows) + '\n')

class ReleaseScannerTests(unittest.TestCase):
    def test_valid_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); good(root)
            (root / 'docs').mkdir()
            (root / 'README.md').write_text((root / 'README.md').read_text() + '[문서](docs/a.md#계약)\n')
            (root / 'docs/a.md').write_text('# 계약\n')
            self.assertEqual(run(root).returncode, 0)

    def test_missing_duplicate_and_nonsequential_ids(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / 'README.md').write_text('| AUT-01 |\n| AUT-01 |\n| INC-01 |\n| INC-03 |\n')
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('중복 ID', result.stdout)
            self.assertIn('비연속 ID', result.stdout)

    def test_broken_link_and_anchor(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); good(root)
            (root / 'README.md').write_text((root / 'README.md').read_text() + '[없음](missing.md#nope)\n')
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('끊긴 경로', result.stdout)

    def test_existing_file_with_missing_anchor(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); good(root)
            (root / 'docs').mkdir()
            (root / 'docs/a.md').write_text('# 계약\n')
            (root / 'README.md').write_text((root / 'README.md').read_text() + '[없는 anchor](docs/a.md#nope)\n')
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('끊긴 anchor', result.stdout)

    def test_nested_document_root_relative_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); good(root)
            (root / 'docs' / 'nested').mkdir(parents=True)
            (root / 'docs' / 'a.md').write_text('# 계약\n')
            (root / 'docs' / 'nested' / 'page.md').write_text('[문서](docs/a.md)\n')
            result = run(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('끊긴 경로', result.stdout)

    def test_out_of_root_link_is_rejected_even_when_target_exists(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); good(root)
            outside = root.parent / f'{root.name}-outside.md'
            outside.write_text('# 외부\n')
            try:
                (root / 'README.md').write_text((root / 'README.md').read_text() + '[외부](../' + outside.name + ')\n')
                result = run(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('끊긴 경로', result.stdout)
            finally:
                outside.unlink()

    def test_forbidden_filename_secret_and_private_path(self):
        for filename, content, expected in (
            ('.env', 'x', '금지 파일명'),
            ('note.md', 'test' + '@example.com', '민감 패턴'),
            ('note.md', '10' + '.0.0.1', '민감 패턴'),
            ('note.md', '/' + 'home/private', '민감 패턴'),
        ):
            with tempfile.TemporaryDirectory() as d:
                root = Path(d); good(root)
                (root / filename).write_text(content)
                result = run(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stdout)

    def test_complete_minimal_fixture_is_checked(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); good(root)
            self.assertEqual(run(root).returncode, 0)

if __name__ == '__main__':
    unittest.main()
