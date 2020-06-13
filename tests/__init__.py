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


class TestProjectSlug(BaseTestCase):
    def test_specify_project_slug(self):
        project_name = "Test Project"
        project_slug = "test_project"

        cookiecutter(
            **self.default_args,
            extra_context={"project_name": project_name, "project_slug": project_slug,}
        )

        # There should be a single generated folder in the tempdir, and the
        # name should match the specified project slug.
        contents = list(self.tempdir_path.iterdir())
        self.assertEqual(len(contents), 1)

        result_path = contents[0]
        self.assertTrue(result_path.is_dir)
        self.assertEqual(result_path.name, project_slug)

    def test_infer_project_slug(self):
        project_name = "Other Test Project"
        project_slug = "other_test_project"

        # Do not pass the project_slug
        cookiecutter(**self.default_args, extra_context={"project_name": project_name,})

        # There should be a single generated folder in the tempdir, and the
        # name should match the specified project slug.
        contents = list(self.tempdir_path.iterdir())
        self.assertEqual(len(contents), 1)

        result_path = contents[0]
        self.assertTrue(result_path.is_dir)
        self.assertEqual(result_path.name, project_slug)


class BaseGeneratedTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.project_name = "Test project"
        self.project_slug = "test_project"
        self.project_path = self.tempdir_path / self.project_slug

        self.default_args["extra_context"] = {
            "project_name": self.project_name,
            "project_slug": self.project_slug,
        }

        cookiecutter(**self.default_args)


class TestProjectContents(BaseGeneratedTestCase):

    def test_toplevel_defaults(self):
        expected_contents = {
            ".gitignore",
            "pyproject.toml",
            "setup.cfg",
            "setup.py",
            "src",
        }
        actual_contents = {path.name for path in self.project_path.iterdir()}
        self.assertEqual(actual_contents, expected_contents)

    def test_src_defaults(self):
        expected_contents = {
                self.project_slug,
        }
        project_src_path = self.project_path / "src"
        actual_contents = {path.name for path in project_src_path.iterdir()}
        self.assertEqual(actual_contents, expected_contents)

    def test_package_defaults(self):
        expected_contents = {
                "__init__.py",
        }
        project_package_path = self.project_path / "src" / self.project_slug
        actual_contents = {path.name for path in project_package_path.iterdir()}
        self.assertEqual(actual_contents, expected_contents)
