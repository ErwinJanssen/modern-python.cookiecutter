import unittest
import tempfile
import pathlib
import venv
import subprocess
import json
import os
import shlex
import sys
import textwrap

from cookiecutter.main import cookiecutter


def checked_subprocess_run(command):
    """Run the command, print the output, and check if the call was successful.

    Using this wrapper functions in the tests offers the follow functionality:

    -   Pass the command as a string, instead of a list. This is easier to
        write, and `shlex.split` ensure it is split correctly.
    -   Capture and decode both stdout and stderr.
    -   Print both stdout and stderr, to include the output in the test case.
    -   Raise an exception on a non-zero exit status.
    """
    args = shlex.split(command)
    completed = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

        # Generate virtual environment for this test run
        cls.venv_path = cls.tempdir_path / "venv"
        cls.venv_python = cls.venv_path / "bin" / "python"
        venv.create(env_dir=cls.venv_path, system_site_packages=False, with_pip=True)

        # Ensure the virtual environment has the most recent version of pip.
        checked_subprocess_run(f"{cls.venv_python} -m pip install --upgrade pip")

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
        run_command = f"{self.venv_python} -m pip install {self.project_path}"
        checked_subprocess_run(run_command)

        # Verify that name is correct and version number is set
        run_command = f"{self.venv_python} -m pip list --format json"
        out, err = checked_subprocess_run(run_command)
        output = json.loads(out)
        entries = [entry for entry in output if entry["name"] == self.project_slug]

        # Exactly one entry should remain
        self.assertEqual(len(entries), 1)

        # Version number should be set through setuptools_scm, and not be 0.0.0
        expected_version = "0.1.dev0"
        self.assertEqual(entries[0]["version"], expected_version)

        # This version number should be in the `__version__` attribute of the
        # module.
        script = textwrap.dedent(
            f"""\
            import {self.module_slug}
            print({self.module_slug}.__version__, end="")
        """
        )
        run_command = f"{self.venv_python} -c '{script}'"
        out, err = checked_subprocess_run(run_command)
        self.assertEqual(out, expected_version)

    @classmethod
    def tearDownClass(cls):
        # Cleanup the temporary directory
        cls.tempdir.cleanup()
