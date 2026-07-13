from pathlib import Path
from tempfile import TemporaryDirectory
import base64
import unittest

from src.common_utils import gen_dict, safe_target
from src.updater import apply_json_pack, try_to_erase_file


class UpdaterTests(unittest.TestCase):
    def test_safe_target_rejects_escape_and_other_siblings(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            hybrid = root / "hybrid_knot_indexer"
            hybrid.mkdir()
            for relative in ("../outside", "/absolute", "other/file"):
                with self.subTest(relative=relative), self.assertRaises(ValueError):
                    safe_target(relative, root, hybrid)

    def test_apply_and_delete_stay_inside_hybrid_directory(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            hybrid = root / "hybrid_knot_indexer"
            hybrid.mkdir()
            old = hybrid / "old.txt"
            old.write_text("old", encoding="utf-8")
            package = {"hybrid_knot_indexer/new.txt": b"new"}
            self.assertEqual(apply_json_pack(package, root, hybrid), 1)
            self.assertEqual((hybrid / "new.txt").read_bytes(), b"new")
            self.assertEqual(try_to_erase_file(package, root, hybrid), 1)
            self.assertFalse(old.exists())

    def test_scan_is_deterministic_and_encodes_bytes(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            hybrid = root / "hybrid_knot_indexer"
            hybrid.mkdir()
            (hybrid / "b.txt").write_bytes(b"b")
            (hybrid / "a.txt").write_bytes(b"a")
            result = gen_dict(root, hybrid)
            self.assertEqual(list(result), [
                "hybrid_knot_indexer/a.txt",
                "hybrid_knot_indexer/b.txt",
            ])
            self.assertEqual(base64.b64decode(result["hybrid_knot_indexer/a.txt"]), b"a")


if __name__ == "__main__":
    unittest.main()
