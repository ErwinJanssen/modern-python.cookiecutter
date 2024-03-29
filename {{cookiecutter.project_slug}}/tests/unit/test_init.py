import unittest

import {{ cookiecutter.module_slug }}

class MetadataTest(unittest.TestCase):

    def test_version(self):
        """Version number should be set"""
        # Version number should be set, so evaluate to True
        self.assertTrue({{ cookiecutter.module_slug }}.__version__)

        # Version number should be the default value of 0.0.0
        self.assertNotEqual({{ cookiecutter.module_slug }}.__version__, "0.0.0")
