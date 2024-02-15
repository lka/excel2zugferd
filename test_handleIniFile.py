import unittest
import handleIniFile
import os

class test_IniFile(unittest.TestCase):

    def setUp(self) -> None:
        self.fn = 'Test.ini'
        self.dir = '.'
        self.file = os.path.join(self.dir, self.fn)
        try:
            os.remove(self.file)
        except FileNotFoundError:
            pass
        self.IniFileClass = handleIniFile.IniFile(self.fn, self.dir)
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
        file = self.IniFileClass.existsIniFile()
        self.assertIsNone(file, "Should be None, because ini file doesn't exist")

    def test_exists_true(self):
        """
        Teste, ob ein ini File existiert
        """
        expected = { 'Test1': 'Irgendwas', 'Test3': 'Was anderes', 'Test2': 'Ganz was anderes'}
        self.IniFileClass.createIniFile(expected)
        file = self.IniFileClass.existsIniFile()
        self.assertIsNotNone(file, "Should not be None (File-Handle), because ini file exist")
        content = self.IniFileClass.readIniFile()
        self.assertDictEqual(content, expected, f"Content of Ini-File should be equal to {expected}")

if __name__ == '__main__':
    unittest.main()