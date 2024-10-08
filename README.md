# Cookiecutter: Modern Python project

This Cookiecutter provides a template for modern Python projects. It provides
best practices, and uses modern versions of tooling, which allows a better
packaging experience.

Highlights:

-   Use a `src/` layout. The most important difference with a "flat" layout, is
    that the project must be installed before it can be imported. This prevents
    accidental usage of code that resides in the project directory, but is not
    (properly) included in the actual package.

    For arguments on why you would want this, check out these resources:
    -   https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
    -   https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure

-   Write the README in Markdown. Markdown is a very popular format for
    documentation and READMEs, but PyPi only supported reStructedText for
    a long time. Markdown support was added in 2018.

-   Use declarative configuration as much as possible. The build tools and
    package data are specified in `pyproject.toml`. This means that
    a `setup.py` (the default way for many project to manage their metadata) is
    no longer necessary. This reduces complexity, and makes it easier to
    transition to a different build system if desired.

-   Rely on source control management to specify the version number (e.g. git
    tags), instead of manually keeping them up to date in `setup.cfg` and
    `__version__`.

-   Keep code quality high by running various lint and format tools after every
    commit through Git hooks managed by [pre-commit](https://pre-commit.com/).
