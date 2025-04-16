"""
Module Test Lieferant
"""

import unittest
from pathlib import Path
from src.middleware import Middleware


class TestMiddleware(unittest.TestCase):
    """
    Test Class for Class Middleware
    """

    def test_quiet_workflow(self):
        """test quiet workflow for correct directory"""
        middleware = Middleware()
        middleware.set_iniFile()
        middleware.ini_file.content["Verzeichnis"] = "C:\\Users\\XXXX\\Documents"
        middleware.quiet = True
        filename = ".\\TestRechnung.xlsx"
        try:
            middleware.quiet_workflow(filename, 1)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        except IOError:
            self.fail("raised IOError unexpectedly!")
        except SystemExit:
            self.fail("raised SystemExit expectedly!")

    def test_filenames(self):
        """Test correct filenames for program execution"""
        the_args = ["prog_name", "-1", ".\\Rechnung2.PDF", ".\\TestRechnung.xlsx"]
        MSG = "should be equal"
        mw = Middleware()
        mw.set_iniFile()
        mw.quiet = True
        mw.setStammdatenToInvoiceCollection()
        Path(".\\Rechnung2.PDF").touch()
        self.assertEqual(mw.check_filenames(the_args), ".\\TestRechnung.xlsx", MSG)
        Path(".\\Rechnung2.PDF").unlink()
