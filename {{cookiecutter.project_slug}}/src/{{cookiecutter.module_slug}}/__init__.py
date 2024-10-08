"""Package entry point, defines metadata."""

import importlib.metadata

# Single source version number by using the metadata from the installed
# package.
__version__ = importlib.metadata.version("{{ cookiecutter.project_slug }}")
