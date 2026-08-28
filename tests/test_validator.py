from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import tempfile
import unittest
import sys
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location("validator", ROOT / "scripts" / "validate_playables_bundle.py")
validator = module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


GOOD_INDEX = """<!doctype html>
<script src="https://www.youtube.com/game_api/v1"></script>
<script src="game.js"></script>
"""


class ValidatorTests(unittest.TestCase):
    def test_valid_directory_passes_static_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "index.html").write_text(GOOD_INDEX, encoding="utf-8")
            (root / "game.js").write_text("window.game = {};", encoding="utf-8")
            _, findings = validator.validate(root)
            self.assertFalse([item for item in findings if item.level == "error"])

    def test_inline_code_before_sdk_fails_order(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "index.html").write_text(
                '<script>window.game = {};</script>'
                '<script src="https://www.youtube.com/game_api/v1"></script>',
                encoding="utf-8",
            )
            _, findings = validator.validate(root)
            self.assertIn("SDK_ORDER", {item.code for item in findings})

    def test_zip_requires_root_index(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "bad.zip"
            with ZipFile(archive, "w") as bundle:
                bundle.writestr("build/index.html", GOOD_INDEX)
            _, findings = validator.validate(archive)
            self.assertIn("INDEX_ROOT", {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()
