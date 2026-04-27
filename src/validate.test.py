import importlib.util
import unittest
from pathlib import Path


module_path = Path(__file__).with_name("validate.py")
spec = importlib.util.spec_from_file_location("validate_module", module_path)
assert spec is not None and spec.loader is not None
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)


class ValidateTests(unittest.TestCase):
    def test_ordinary_title_is_true(self) -> None:
        self.assertTrue(validate.isValidTitle("牛乳を買う"))

    def test_empty_string_is_false(self) -> None:
        self.assertFalse(validate.isValidTitle(""))

    def test_whitespace_only_is_false(self) -> None:
        self.assertFalse(validate.isValidTitle("   "))

    def test_more_than_100_characters_is_false(self) -> None:
        long_title = "あ" * 101
        self.assertFalse(validate.isValidTitle(long_title))

    def test_exactly_100_characters_is_true(self) -> None:
        max_title = "あ" * 100
        self.assertTrue(validate.isValidTitle(max_title))


if __name__ == "__main__":
    unittest.main()
