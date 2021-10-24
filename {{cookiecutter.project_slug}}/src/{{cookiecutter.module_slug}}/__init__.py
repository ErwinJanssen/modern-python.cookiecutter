# The module `import.metadata` was added in Python 3.8. For earlier version,
# the package `importlib_metadata` can be used.
try:
    import importlib.metadata
except ModuleNotFoundError:
    import importlib
    import importlib_metadata
    importlib.metadata = importlib_metadata

# Single source version number by using the metadata from the installed
# package.
__version__ = importlib.metadata.version("{{ cookiecutter.project_slug }}")
