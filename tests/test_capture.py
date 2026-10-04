import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import importlib.util

CAPTURE = Path(__file__).parents[1] / 'examples' / 'capture.py'
SPEC = importlib.util.spec_from_file_location('capture', CAPTURE)
capture = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(capture)

class CaptureTests(unittest.TestCase):
    def test_requires_root(self):
        result = subprocess.run([sys.executable, str(CAPTURE), 'title', 'body'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--root', result.stderr)

    def test_two_captures_are_sequential_and_local(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = []
            for _ in range(2):
                outputs.append(subprocess.check_output([
                    sys.executable, str(CAPTURE), 'Synthetic parser contract', 'raw technical example',
                    '--root', str(root), '--area', 'ai'
                ], text=True).strip())
            self.assertNotEqual(outputs[0], outputs[1])
            self.assertIn('raw technical example', Path(outputs[0]).read_text())
            self.assertFalse((root / '.git').exists())

    def test_hostile_metadata_is_rejected(self):
        cases = [
            (("title", "body", "ai", ["safe]\nstatus: done"], "2026-01-01"), {}),
            (("title\nstatus: done", "body", "ai", [], "2026-01-01"), {}),
            (("title", "body", "ai", [], "2026-01-01"), {"next_action": "next\nstatus: done"}),
            (("title", "body", "ai", [], "2026-01-01"), {"received_at": "date\nstatus: done"}),
        ]
        for args, kwargs in cases:
            with self.assertRaises(ValueError):
                capture.build_note(*args, **kwargs)

    def test_multiline_body_is_preserved_after_strip(self):
        note = capture.build_note('title', '  first\nsecond\n', 'ai', [], '2026-01-01')
        self.assertIn('## Raw\nfirst\nsecond\n\n## Processing Log', note)

if __name__ == '__main__':
    unittest.main()
