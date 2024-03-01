import os
import unittest

import settings


class TestApp(unittest.TestCase):
    
    def test_settings(self):
        """Check if path are valid"""
        self.assertTrue(os.path.exists(settings.OUTPUT_PATH))
        self.assertTrue(os.path.exists(settings.INPUT_PATH))
        self.assertTrue(os.path.exists(settings.WORKFLOW_FILE))
        self.assertTrue(os.path.exists(settings.MISSING_SKETCH))


if __name__ == "__main__":
    unittest.main()