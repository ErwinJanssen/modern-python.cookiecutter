"""Unit tests to verify project is correctly initialized and packaged."""

# Ignore Ruff's pytest assert rule here, since built-in `unittest` is used.
# ruff: noqa: PT009
import unittest

import {{ cookiecutter.module_slug }}


class MetadataTest(unittest.TestCase):
    """Verify metadata of this package."""

    def test_version(self) -> None:
        """Version number should be set."""
        # Version number should be set, so evaluate to True
        self.assertTrue({{ cookiecutter.module_slug }}.__version__)

        # Version number should be the default value of 0.0.0
        self.assertNotEqual({{ cookiecutter.module_slug }}.__version__, "0.0.0")
