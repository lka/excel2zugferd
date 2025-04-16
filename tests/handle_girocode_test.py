"""
Module for handle_ini_file_test
"""

import unittest
import src.handle_girocode as gc
import qrcode


class TestHandleGirocode(unittest.TestCase):
    """
    TestClass for Handle_Girocode Class
    """

    def test_class_exists_false_1p(self):
        """Test failing first Parameter raises ValueError"""
        self.assertRaises(ValueError, gc.Handle_Girocode, None, None, None)

    def test_class_exists_false_2p(self):
        """Test failing second Parameter raises ValueError"""
        self.assertRaises(ValueError, gc.Handle_Girocode, "Test", None, None)

    def test_class_exists_false_3p(self):
        """Test failing third Parameter raises ValueError"""
        self.assertRaises(ValueError, gc.Handle_Girocode, "BIC", "BAM", None)

    def test_class_exists(self):
        """Test Object creation with 3 Parameters without raising ValueError"""
        GC = gc.Handle_Girocode("BIC", "BAM", "Boom")
        self.assertIsNotNone(GC, "Object exists")

    def test_class_empty(self):
        """Test Object creation, empty qrdata after initialization"""
        GC = gc.Handle_Girocode(
            "SOLADES1TBB123",
            "1234567890123456789012345678901234567890",
            "Max Mustermann",
            True,
        )
        self.assertIsNone(GC.qrdata, "should not be populated")

    def test_girocodegen_umlaute(self):
        """generate girocode, replace Umlaute"""
        GC = gc.Handle_Girocode(
            "SOLADES1TBB123",
            "1234567890123456789012345678901234567890",
            "Max Müstermann",
            True,
        )
        GC.girocodegen(1793.89, "RG20240001 Max Möstermann")
        self.assertEqual(
            GC.qrdata,
            "BCD\n001\n2\nSCT\nSOLADES1TBB\n\
Max Muestermann\n1234567890123456789012345678901234\nEUR1793.89\n\n\n\
RG20240001 Max Moestermann\n",
        )

    def test_girocodegen_image(self):
        """generate girocode"""
        GC = gc.Handle_Girocode(
            "SOLADES1TBB123",
            "1234567890123456789012345678901234567890",
            "Max Mustermann",
        )
        img = GC.girocodegen(1793.89, "RG20240001 Max Mustermann")
        self.assertEqual(
            type(img), qrcode.image.pil.PilImage, "should return an image object"
        )
