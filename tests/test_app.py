import unittest


class TestApp(unittest.TestCase):
    
    def test_settings(self):
        """Check if path are valid"""
        self.assertTrue(OUTPUT_PATH.exists())