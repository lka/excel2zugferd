"""
Module for handle_ini_file_test
"""

import os
import unittest
from pathlib import Path

import src.handle_ini_file as handle_ini_file


class TestIniFile(unittest.TestCase):
    """Testclass for IniFile"""

    def setUp(self) -> None:
        self.fn = "Test.ini"
        self.dir = "."
        self.file = os.path.join(self.dir, self.fn)
        try:
            os.remove(self.file)
        except FileNotFoundError:
            pass
        self.ini_file_class = handle_ini_file.IniFile(path_to_inifile=self.file)
        return super().setUp()

    def tearDown(self) -> None:
        try:
            os.remove(self.file)
        except FileNotFoundError:
            pass
        return super().tearDown()

    def test_exists_false(self):
        """
        Teste, dass kein ini File existiert
        """
        file = self.ini_file_class.exists_ini_file()
        self.assertIsNone(file, "Should be None, because ini file doesn't exist")

    def test_exists_true(self):
        """
        Teste, ob ein ini File existiert
        """
        expected = {
            "Test1": "Irgendwas",
            "Test3": "Was anderes",
            "Test2": "Ganz was anderes",
        }
        self.ini_file_class.create_ini_file(expected)
        file = self.ini_file_class.exists_ini_file()
        self.assertIsNotNone(
            file, "Should not be None (File-Handle), because ini file exist"
        )
        content = self.ini_file_class.read_ini_file()
        self.assertDictEqual(
            content,
            expected,
            f"Content of Ini-File should be equal to {expected}",
            # type: ignore
        )

    def test_merge_content_of_ini_file(self):
        """
        Test the merge of content of ini_file with other content
        """
        MSG = "dicts should be equal"
        self.ini_file_class.content = {
            "Org1": "Test1",
            "Org2": "Test2",
            "Org3": "Test3",
        }
        modification = {"Org2": "Test4", "Mod1": "Test5"}
        expected = {"Org1": "Test1", "Org2": "Test4", "Org3": "Test3", "Mod1": "Test5"}
        self.ini_file_class.merge_content_of_ini_file(modification)
        self.assertDictEqual(self.ini_file_class.content, expected, MSG)

    def test_raise_error_on_false_ini_file(self):
        """
        Test the raise error if ini directory is not creatable
        """
        with self.assertRaises(ValueError):
            handle_ini_file.IniFile(dir=Path("I:/Laber"))


# if __name__ == '__main__':
#     unittest.main()
