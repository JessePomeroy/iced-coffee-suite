import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("inventory", Path(__file__).with_name("test_inventory.py"))
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)

class InventoryTests(unittest.TestCase):
    def test_hidden_project_tests_are_included_but_dependencies_are_excluded(self):
        with tempfile.TemporaryDirectory() as root:
            for relative in ["tests/test_public.py", ".fixtures/test_hidden.py", "node_modules/pkg/test_vendor.py", ".venv/test_env.py"]:
                target = Path(root, relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("")
            self.assertEqual(inventory.on_disk(root, "", inventory.DEFAULT_PATTERNS), {"tests/test_public.py", ".fixtures/test_hidden.py"})

    def test_custom_scope_and_pattern(self):
        with tempfile.TemporaryDirectory() as root:
            for relative in ["custom/check.case", "other/check.case"]:
                target = Path(root, relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("")
            self.assertEqual(inventory.on_disk(root, "custom", ["*.case"]), {"custom/check.case"})

if __name__ == "__main__":
    unittest.main()
