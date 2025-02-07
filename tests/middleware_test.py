"""
Module Test Lieferant
"""

import unittest
from src.middleware import Middleware


class TestMiddleware(unittest.TestCase):
    """
    Test Class for Class Middleware
    """

    def test_quiet_workflow(self):
        """test quiet workflow for correct directory"""
        middleware = Middleware()
        middleware.set_iniFile()
        middleware.ini_file.content["Verzeichnis"] =\
            u"C:\\Users\\XXXX\\Documents"
        middleware.quiet = True
        filename = u".\\TestRechnung.xlsx"
        try:
            middleware.quiet_workflow(filename, 1)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        except IOError:
            self.fail("raised IOError unexpectedly!")
        except SystemExit:
            self.fail("raised SystemExit expectedly!")
