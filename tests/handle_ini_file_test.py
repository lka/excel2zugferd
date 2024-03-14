"""
Module for handle_ini_file_test
"""
import os
import unittest
import handle_ini_file


class TestIniFile(unittest.TestCase):
    """Testclass for IniFile"""

    def setUp(self) -> None:
        self.fn = 'Test.ini'
        self.dir = '.'
        self.file = os.path.join(self.dir, self.fn)
        try:
            os.remove(self.file)
        except FileNotFoundError:
            pass
        self.ini_file_class = handle_ini_file.IniFile(self.fn, self.dir)
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
        expected = {'Test1': 'Irgendwas', 'Test3': 'Was anderes', 'Test2': 'Ganz was anderes'}
        self.ini_file_class.create_ini_file(expected)
        file = self.ini_file_class.exists_ini_file()
        self.assertIsNotNone(file, "Should not be None (File-Handle), because ini file exist")
        content = self.ini_file_class.read_ini_file()
        self.assertDictEqual(content, expected, f"Content of Ini-File should be equal to {expected}")  # type: ignore


if __name__ == '__main__':
    unittest.main()
