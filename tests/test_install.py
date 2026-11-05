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
spec = importlib.util.spec_from_file_location("skill_installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = installer
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()

    def links(self, names=None, agents=None, **kwargs):
        return installer.make_links(ROOT, self.home, names or ["diagnosing-bugs"],
                                    agents or ["codex"], [], **kwargs)

    def test_shared_agents_deduplicate_and_install_idempotently(self):
        links = self.links(agents=["codex", "gemini", "claude", "pi"])
        self.assertEqual(len(links), 3)
        installer.apply_links(links)
        installer.apply_links(links)
        for link in links:
            self.assertTrue(link.destination.is_symlink())
            self.assertEqual(link.destination.resolve(), link.source)

    def test_conflict_prevents_all_mutations_and_preserves_content(self):
        links = self.links(names=["blast-radius", "diagnosing-bugs"])
        conflict = links[-1].destination
        conflict.parent.mkdir(parents=True)
        conflict.mkdir()
        (conflict / "personal.txt").write_text("keep me")
        with self.assertRaisesRegex(ValueError, "Conflicts"):
            installer.apply_links(links)
        self.assertFalse(links[0].destination.exists())
        self.assertEqual((conflict / "personal.txt").read_text(), "keep me")

    def test_broken_unrelated_symlink_is_a_conflict(self):
        link = self.links()[0]
        link.destination.parent.mkdir(parents=True)
        link.destination.symlink_to(self.base / "not-here")
        self.assertEqual(installer.state(link), "conflict")
        with self.assertRaises(ValueError):
            installer.apply_links([link])
        self.assertEqual(Path(link.destination.readlink()), self.base / "not-here")

    def test_cyclic_destination_link_is_preserved_as_a_conflict(self):
        destination = self.home / ".agents/skills/diagnosing-bugs"
        destination.parent.mkdir(parents=True)
        destination.symlink_to(destination.name)
        link = self.links()[0]
        self.assertEqual(installer.state(link), "conflict")
        with self.assertRaises(ValueError):
            installer.apply_links([link])
        self.assertEqual(destination.readlink(), Path(destination.name))

    def test_file_in_parent_path_is_a_conflict(self):
        (self.home / ".agents").write_text("personal config")
        link = self.links()[0]
        self.assertEqual(installer.state(link), "conflict")
        with self.assertRaises(ValueError):
            installer.apply_links([link])
        self.assertEqual((self.home / ".agents").read_text(), "personal config")

    def test_removal_only_unlinks_owned_entries_and_keeps_sources(self):
        links = self.links()
        installer.apply_links(links)
        installer.apply_links(links, remove=True)
        installer.apply_links(links, remove=True)
        self.assertFalse(links[0].destination.is_symlink())
        self.assertTrue((links[0].source / "SKILL.md").is_file())

    def test_changed_target_is_not_removed(self):
        link = self.links()[0]
        installer.apply_links([link])
        link.destination.unlink()
        replacement = self.base / "other-skill"
        replacement.mkdir()
        link.destination.symlink_to(replacement)
        with self.assertRaises(ValueError):
            installer.apply_links([link], remove=True)
        self.assertEqual(link.destination.resolve(), replacement)

    def test_instructions_are_opt_in_and_existing_files_are_preserved(self):
        instructions = self.base / "my-agreements.md"
        instructions.write_text("my preferences")
        self.assertTrue(all(link.destination.name != "AGENTS.md" for link in self.links()))
        links = self.links(instructions=instructions)
        destination = self.home / ".codex/AGENTS.md"
        destination.parent.mkdir()
        destination.write_text("existing agreements")
        with self.assertRaises(ValueError):
            installer.apply_links(links)
        self.assertEqual(destination.read_text(), "existing agreements")
        self.assertEqual(instructions.read_text(), "my preferences")

    def test_instructions_for_all_agents_use_one_personalized_file(self):
        instructions = self.base / "my-agreements.md"
        instructions.write_text("my preferences")
        links = installer.make_links(ROOT, self.home, [], list(installer.AGENTS), [], instructions)
        installer.apply_links(links)
        self.assertEqual(len(links), 4)
        self.assertTrue(all(link.destination.resolve() == instructions for link in links))

    def test_unknown_and_traversal_skill_names_are_rejected(self):
        for name in ["missing-skill", "../instructions"]:
            with self.assertRaisesRegex(ValueError, "Unknown"):
                self.links(names=[name])
        self.assertEqual(list(self.home.iterdir()), [])

    def test_symlink_source_outside_repository_is_rejected(self):
        fake = self.base / "repository"
        (fake / "skills").mkdir(parents=True)
        external = self.base / "external"
        external.mkdir()
        (external / "SKILL.md").write_text("private")
        (fake / "skills/escape").symlink_to(external, target_is_directory=True)
        (fake / "catalog.json").write_text(json.dumps({"version": 1, "skills": [{"name": "escape", "path": "skills/escape"}]}))
        with self.assertRaisesRegex(ValueError, "escapes"):
            installer.make_links(fake, self.home, ["escape"], ["codex"], [])

    def test_failure_rolls_back_only_links_created_by_attempt(self):
        links = self.links(names=["blast-radius", "diagnosing-bugs"])
        original = Path.symlink_to

        def fail_second(path, *args, **kwargs):
            if path == links[1].destination:
                raise OSError("simulated symlink permission failure")
            return original(path, *args, **kwargs)

        with patch.object(Path, "symlink_to", fail_second):
            with self.assertRaises(OSError):
                installer.apply_links(links)
        self.assertFalse(links[0].destination.is_symlink())
        self.assertTrue((links[0].source / "SKILL.md").is_file())

    def test_relative_matching_link_can_be_removed(self):
        source = self.base / "source"
        source.mkdir()
        destination = self.home / "skill"
        destination.symlink_to("../source")
        link = installer.Link(source, destination)
        self.assertTrue(installer.points_to(link))
        installer.apply_links([link], remove=True)
        self.assertTrue(source.is_dir())

    def test_default_preview_creates_no_directories(self):
        target = self.base / "preview-only"
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = installer.main(["--skills-dir", str(target), "--skill", "pdf-reader"])
        self.assertEqual(result, 0)
        self.assertIn("Preview only", output.getvalue())
        self.assertFalse(target.exists())

    def test_cli_apply_check_and_remove_in_isolated_directory(self):
        target = self.base / "custom discovery with spaces"
        base = [sys.executable, "-B", str(ROOT / "install.py"), "--skills-dir", str(target),
                "--skill", "pdf-reader"]
        for options in [["--apply"], ["--check"], ["--remove", "--apply"]]:
            result = subprocess.run(base + options, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((target / "pdf-reader").is_symlink())

    def test_overlapping_destinations_are_rejected_before_writes(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            installer.make_links(ROOT, self.home, ["pdf-reader"], [],
                                 [self.home / "skills", self.home / "skills/pdf-reader/nested"])
        self.assertEqual(list(self.home.iterdir()), [])

    def test_entire_distribution_installs_and_removes_through_cli(self):
        target = self.base / "all-skills"
        command = [sys.executable, "-B", str(ROOT / "install.py"), "--skills-dir", str(target), "--all"]
        result = subprocess.run(command + ["--apply"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for item in installer.load_catalog(ROOT):
            installed = target / item["name"]
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            for name in item.get("subskills", []):
                self.assertTrue((installed / "skills" / name / "SKILL.md").is_file())
        result = subprocess.run(command + ["--remove", "--apply"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(target.iterdir()), [])

    def test_aliased_destinations_with_different_sources_conflict_before_writes(self):
        directory = self.home / "skills"
        directory.mkdir()
        alias = self.home / "alias"
        alias.symlink_to(directory, target_is_directory=True)
        instructions = self.base / "my-agreements.md"
        instructions.write_text("my preferences")
        with self.assertRaisesRegex(ValueError, "same destination"):
            installer.make_links(ROOT, self.home, ["pdf-reader"], [], [directory],
                                 instructions, alias / "pdf-reader")
        self.assertEqual(list(directory.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
