from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import unittest

TEMPLATE = Path(__file__).resolve().parents[1] / 'references' / 'gate_script_template.sh'

class GateTemplateTests(unittest.TestCase):
    def run_gate(self, empty=False):
        with tempfile.TemporaryDirectory(prefix='gate space ') as root:
            root = Path(root)
            runner = root / 'fake runner'
            runner.write_text('#!/usr/bin/env bash\nprintf "ARG:%s\\n" "$@"\n')
            runner.chmod(0o755)
            script = root / 'scripts' / 'gate.sh'
            script.parent.mkdir()
            source = TEMPLATE.read_text().replace(
                'RUNNER=(python -m pytest -q -p no:cacheprovider)',
                'RUNNER=(' + shlex.quote(str(runner)) + ')')
            replacement = 'FAST_GATE=()' if empty else 'FAST_GATE=("tests/test file.py")'
            source = re.sub(r'FAST_GATE=\([\s\S]*?\n\)', lambda _: replacement, source, count=1)
            script.write_text(source)
            return subprocess.run(['bash', str(script), 'fast'], capture_output=True, text=True)

    def test_runner_and_test_paths_with_spaces_stay_single_arguments(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('ARG:tests/test file.py\n', result.stdout)

    def test_empty_fast_gate_does_not_run_the_whole_suite(self):
        result = self.run_gate(empty=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('ARG:', result.stdout)
        self.assertIn('fast gate is not configured', result.stderr)

if __name__ == '__main__':
    unittest.main()
