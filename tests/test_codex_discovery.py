import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("codex_discovery", ROOT / "scripts/check_codex_discovery.py")
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cwd = Path(self.temp.name).resolve()
        self.manifest = ROOT / "skills/slice-loop-workflow/SKILL.md"
        self.expected = {"slice-loop-workflow": self.manifest}

    def listing(self, skills=None, errors=None):
        if skills is None:
            skills = [{"name": "slice-loop-workflow", "path": str(self.manifest), "enabled": True}]
        return {"data": [{"cwd": str(self.cwd), "skills": skills, "errors": errors or []}]}

    def test_same_name_from_another_installation_does_not_pass(self):
        result = self.listing([{"name": "slice-loop-workflow", "path": str(self.cwd / "other/SKILL.md"), "enabled": True}])
        rows, _ = discovery.assess(result, self.cwd, self.expected)
        self.assertEqual(rows[0]["status"], "OTHER_SOURCE")

    def test_disabled_and_missing_manifests_are_distinct(self):
        for skills, status in [([], "MISSING"), ([{
            "name": "slice-loop-workflow", "path": str(self.manifest), "enabled": False,
        }], "DISABLED")]:
            with self.subTest(status=status):
                rows, _ = discovery.assess(self.listing(skills), self.cwd, self.expected)
                self.assertEqual(rows[0]["status"], status)

    def test_matching_symlink_and_other_named_copy_are_reported(self):
        alias = self.cwd / "SKILL.md"
        alias.symlink_to(self.manifest)
        result = self.listing([
            {"name": "slice-loop-workflow", "path": str(alias), "enabled": True},
            {"name": "slice-loop-workflow", "path": str(self.cwd / "other.md"), "enabled": True},
        ])
        rows, _ = discovery.assess(result, self.cwd, self.expected)
        self.assertEqual(rows[0]["status"], "FOUND")
        self.assertEqual(rows[0]["other_sources"], 1)

    def test_wrong_cwd_and_malformed_results_cannot_claim_discovery(self):
        cases = [{}, {"data": []}, self.listing([{"name": "slice-loop-workflow"}]),
                 self.listing([{"name": "slice-loop-workflow", "path": "relative.md", "enabled": True}])]
        wrong = self.listing()
        wrong["data"][0]["cwd"] = str(self.cwd / "another-project")
        cases.append(wrong)
        for result in cases:
            with self.subTest(result=result), self.assertRaises(ValueError):
                discovery.assess(result, self.cwd, self.expected)

    def run_main(self, result):
        with patch.object(discovery.shutil, "which", return_value="codex"), \
                patch.object(discovery, "list_skills", return_value=result), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return discovery.main(["--skill", "slice-loop-workflow", "--cwd", str(self.cwd)])

    def test_link_presence_alone_does_not_pass_discovery(self):
        link = self.cwd / ".agents/skills/slice-loop-workflow"
        link.parent.mkdir(parents=True)
        link.symlink_to(self.manifest.parent)
        self.assertTrue((link / "SKILL.md").is_file())
        self.assertEqual(self.run_main(self.listing([])), 1)
        self.assertEqual(self.run_main(self.listing()), 0)

    def test_discovery_errors_fail_even_when_selected_skill_is_listed(self):
        self.assertEqual(self.run_main(self.listing(errors=[{"path": "broken.md", "message": "invalid metadata"}])), 1)

    def test_bad_arguments_or_missing_cli_never_start_a_server(self):
        with patch.object(discovery, "list_skills") as start, \
                patch.object(discovery.shutil, "which", return_value=None), \
                contextlib.redirect_stderr(io.StringIO()):
            for options in [["--skill", "unknown"], ["--all", "--timeout", "nan"],
                            ["--all", "--timeout", "0"], ["--all", "--cwd", str(self.cwd / "missing")],
                            ["--skill", "slice-loop-workflow"]]:
                self.assertEqual(discovery.main(options), 2)
            start.assert_not_called()

    def run_server(self, mode="normal", timeout=5):
        script = self.cwd / "fake_codex.py"
        calls = self.cwd / "requests.jsonl"
        script.write_text(
            "import json, sys, time\n"
            f"mode = {mode!r}\n"
            "for line in sys.stdin:\n"
            " request = json.loads(line)\n"
            f" with open({str(calls)!r}, 'a') as log: log.write(json.dumps(request) + '\\n')\n"
            " if mode == 'timeout': time.sleep(60)\n"
            " if mode == 'exit': sys.exit(0)\n"
            " if 'id' not in request: continue\n"
            " if mode == 'error':\n"
            "  print(json.dumps({'id': request['id'], 'error': {'message': 'unsupported'}}), flush=True)\n"
            "  continue\n"
            " print(json.dumps({'method': 'notification', 'params': {}}), flush=True)\n"
            f" result = {{}} if request['method'] == 'initialize' else {self.listing()!r}\n"
            " print(json.dumps({'id': request['id'], 'result': result}), flush=True)\n",
            encoding="utf-8",
        )
        original = subprocess.Popen
        processes = []

        def start(command, **kwargs):
            self.assertEqual(command[1:3], ["app-server", "--stdio"])
            process = original([sys.executable, "-B", str(script)], **kwargs)
            processes.append(process)
            return process

        try:
            with patch.object(discovery.subprocess, "Popen", side_effect=start):
                return discovery.list_skills("test-codex", self.cwd, timeout)
        finally:
            self.assertEqual(len(processes), 1)
            self.assertIsNotNone(processes[0].poll(), "the diagnostic left its app-server running")

    def test_stdio_handshake_lists_without_inference_and_closes_server(self):
        self.assertEqual(self.run_server(), self.listing())
        requests = [json.loads(line) for line in (self.cwd / "requests.jsonl").read_text().splitlines()]
        self.assertEqual([request["method"] for request in requests], ["initialize", "initialized", "skills/list"])
        self.assertTrue(requests[-1]["params"]["forceReload"])
        self.assertEqual(requests[-1]["params"]["cwds"], [str(self.cwd)])

    def test_timeout_terminates_only_its_server(self):
        with self.assertRaises(TimeoutError):
            self.run_server("timeout", timeout=0.15)

    def test_protocol_error_and_early_exit_are_unavailable(self):
        for mode in ("error", "exit"):
            with self.subTest(mode=mode), self.assertRaises(RuntimeError):
                self.run_server(mode)


if __name__ == "__main__":
    unittest.main()
