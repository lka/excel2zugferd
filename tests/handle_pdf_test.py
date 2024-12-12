"""
Modul handle_pdf_test
"""

import os
from pathlib import Path
import unittest
import src.handle_pdf as handle_pdf


class TestHandlePdf(unittest.TestCase):
    """
    Test Class for handling pdf
    """
    def setUp(self) -> None:
        self.pdf = handle_pdf.Pdf(None, None)
        return super().setUp()

    def test_demo(self):
        """
        check whether demo creates the file hello_world.pdf
        """
        try:
            os.remove("hello_world.pdf")
        except OSError:
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
        except OSError:
            pass
        retval = self.pdf.uniquify(fn)
        self.assertEqual(retval, expected, "should be equal")
        try:
            os.remove(fn)
        except OSError:
            pass

    def test_uniquify_appendix(self):
        """
        Check whether uniquify counts up filename if file already exists
        """
        fn = "testUniquify.pdf"
        expected = "testUniquify_E.pdf"
        try:
            Path(fn).touch()
        except OSError:
            pass
        retval = self.pdf.uniquify(fn, '_E')
        self.assertEqual(retval, expected, "should be equal")
        try:
            os.remove(fn)
        except OSError:
            pass

    def test_uniquify_appendix_with_already_existant_appendix(self):
        """
        Check whether uniquify counts up filename if file already exists
        without appending already existant appendix
        """
        fn = "testUniquify_E.pdf"
        expected = "testUniquify_E (1).pdf"
        try:
            Path(fn).touch()
        except OSError:
            pass
        retval = self.pdf.uniquify(fn, '_E')
        self.assertEqual(retval, expected, "should be equal")
        try:
            os.remove(fn)
        except OSError:
            pass

# if __name__ == "__main__":
#     unittest.main()
