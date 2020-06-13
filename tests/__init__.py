import unittest
import tempfile
import pathlib
import venv
import subprocess

import os

from cookiecutter.main import cookiecutter


class TestProjectGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary directory for this test run
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.tempdir_path = pathlib.Path(cls.tempdir.name)
        cls.output_path = cls.tempdir_path / "output"

        # Generate virtual environment for this test run
        cls.venv_path = cls.tempdir_path / "venv"
        cls.venv_python = cls.venv_path / "bin" / "python"
        venv.create(env_dir=cls.venv_path, system_site_packages=False, with_pip=True)

        # Set variables
        cls.project_name = "Modern Python"
        cls.project_slug = "modern-python"
        cls.module_slug = "modern_python"
        cls.project_path = cls.output_path / cls.project_slug

        # Generate the project with Cookiecutter
        cookiecutter(
            # The template to test is located in the current working directory
            template=".",
            # Do not ask for input, as this blocks the test runner
            no_input=True,
            # Use a temporary output directory
            output_dir=cls.output_path,
            # Additional variables
            extra_context={
                "project_name": cls.project_name,
                "project_slug": cls.project_slug,
            },
        )

    def test_directory_name(self):
        # There should be a single generated folder in `output_path`, and the
        # name should match the project slug.
        contents = list(self.output_path.iterdir())
        self.assertEqual(len(contents), 1)

        result_path = contents[0]
        self.assertTrue(result_path.is_dir)
        self.assertEqual(result_path.name, self.project_slug)

    def test_toplevel_contents(self):
        expected = {
            ".git": True,
            ".gitignore": False,
            "pyproject.toml": False,
            "setup.cfg": False,
            "setup.py": False,
            "src": True,
        }
        actual = {path.name: path.is_dir() for path in self.project_path.iterdir()}
        self.assertEqual(actual, expected)

    def test_src_contents(self):
        src_path = self.project_path / "src"

        expected = {
            self.module_slug: True,
        }
        actual = {path.name: path.is_dir() for path in src_path.iterdir()}
        self.assertEqual(actual, expected)

    def test_module_contents(self):
        module_path = self.project_path / "src" / self.module_slug

        expected = {
            "__init__.py": False,
        }
        actual = {path.name: path.is_dir() for path in module_path.iterdir()}
        self.assertEqual(actual, expected)

    def test_install(self):
        run_command = [self.venv_python, "-m", "pip", "install", self.project_path]
        subprocess.run(
            run_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    @classmethod
    def tearDownClass(cls):
        # Cleanup the temporary directory
        cls.tempdir.cleanup()
