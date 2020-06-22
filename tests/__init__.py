import unittest
import tempfile
import pathlib
import subprocess
import shlex
import sys

from cookiecutter.main import cookiecutter


def checked_subprocess_run(command, **kwargs):
    """Run the command, print the output, and check if the call was successful.

    Using this wrapper function in the tests offers the follow functionality:

    -   Pass the command as a string, instead of a list. This is easier to
        write, and `shlex.split` ensure it is split correctly.
    -   Capture and decode both stdout and stderr.
    -   Print both stdout and stderr, to include the output in the test case.
    -   Raise an exception on a non-zero exit status.
    """
    args = shlex.split(command)
    completed = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
    )

    out = completed.stdout.decode()
    err = completed.stderr.decode()

    # Print the subprocess output to include in the test output
    print(out, file=sys.stdout)
    print(err, file=sys.stderr)

    # After printing the output, raise an exception on a non-zero exit status.
    completed.check_returncode()

    return out, err


class TestProjectGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary directory for this test run
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.tempdir_path = pathlib.Path(cls.tempdir.name)
        cls.output_path = cls.tempdir_path / "output"

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
            ".flake8": False,
            ".git": True,
            ".gitignore": False,
            ".pre-commit-config.yaml": False,
            "pyproject.toml": False,
            "setup.cfg": False,
            "src": True,
            "tests": True,
            "tox.ini": False,
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

    def test_tox(self):
        """Run the test suite of the generated project."""
        checked_subprocess_run("tox -e py,lint", cwd=self.project_path)

    @classmethod
    def tearDownClass(cls):
        # Cleanup the temporary directory
        cls.tempdir.cleanup()
