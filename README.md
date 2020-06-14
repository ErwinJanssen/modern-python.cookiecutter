# Cookiecutter: Modern Python project

This Cookiecutter provides a template for modern Python projects. It provides
best practices, and uses modern versions of tooling, which allows a better
packaging experience.

Highlights:

-   Uses a `src/` layout. For arguments on why you would want this, check out
    the following blog post:
    -   https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
-   Uses Markdown for the README. Markdown is the most popular format for
    documentation and READMEs, but PyPi only supported reStructedText for a
    long time. With the new PyPi, Markdown is now supported.
-   Uses declarative configuration as much as possible. The build tools are
    specified in `pyproject.toml`, and the package data is in setup.cfg. This
    means that a `setup.py` (the default way for many project to manage their
    metadata) is no longer necessary. This reduces complexity, and makes it
    easier to transition to a different build system if desired.
-   Uses the source control management to specify the version number (e.g. git
    tags), instead of manually keeping them up to date in `setup.cfg` and
    `__version__`.
