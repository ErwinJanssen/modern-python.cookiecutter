import unittest
import tempfile
import pathlib

import os

from cookiecutter.main import cookiecutter


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory in which the template project can be
        created, and define some defaults.
        """
        self.tempdir = tempfile.TemporaryDirectory()
        self.tempdir_path = pathlib.Path(self.tempdir.name)

        self.default_args = {
            # The template to test is located in the current working directory
            "template": ".",
            # Do not ask for input, as this blocks the test runner
            "no_input": True,
            # Use a temporary output directory
            "output_dir": self.tempdir_path,
        }

    def tearDown(self):
        """Cleanup the temporary directory."""
        self.tempdir.cleanup()


class TestPackageSlug(BaseTestCase):
    def test_specify_package_slug(self):
        package_name = "Test Package"
        package_slug = "test_package"

        cookiecutter(
            **self.default_args,
            extra_context={"package_name": package_name, "package_slug": package_slug,}
        )

        # There should be a single generated folder in the tempdir, and the
        # name should match the specified project slug.
        contents = list(self.tempdir_path.iterdir())
        self.assertEqual(len(contents), 1)

        result_path = contents[0]
        self.assertTrue(result_path.is_dir)
        self.assertEqual(result_path.name, package_slug)

    def test_infer_package_slug(self):
        package_name = "Other Test Package"
        package_slug = "other_test_package"

        # Do not pass the package_slug
        cookiecutter(**self.default_args, extra_context={"package_name": package_name,})

        # There should be a single generated folder in the tempdir, and the
        # name should match the specified project slug.
        contents = list(self.tempdir_path.iterdir())
        self.assertEqual(len(contents), 1)

        result_path = contents[0]
        self.assertTrue(result_path.is_dir)
        self.assertEqual(result_path.name, package_slug)


class TestPackageContents(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.package_name = "Test package"
        self.package_slug = "test_package"
        self.package_path = self.tempdir_path / self.package_slug

        self.default_args["extra_context"] = {
            "package_name": self.package_name,
            "package_slug": self.package_slug,
        }

    def test_toplevel_defaults(self):
        cookiecutter(**self.default_args)

        expected_contents = {
            ".gitignore",
            "pyproject.toml",
            "setup.cfg",
            "setup.py",
            "src",
        }
        actual_contents = {path.name for path in self.package_path.iterdir()}
        self.assertEqual(actual_contents, expected_contents)
