import unittest
from handlePDF import Pdf
import os
from pathlib import Path


class test_handlePDF(unittest.TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(None, None)
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_demo(self):
        """
        check whether demo creates the file hello_world.pdf
        """
        try:
            os.remove("hello_world.pdf")
        except Exception:
            pass

        self.pdf.demo()
        self.assertTrue(os.path.isfile("hello_world.pdf"))

    def test_uniquify(self):
        """
        Check whether uniquify counts up filename if file already exists
        """
        fn = "testUniquify.pdf"
        expected = "testUniquify (1).pdf"
        try:
            Path(fn).touch()
        except Exception:
            pass
        retVal = self.pdf.uniquify(fn)
        self.assertEqual(retVal, expected, "should be equal")
        try:
            os.remove(fn)
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()
