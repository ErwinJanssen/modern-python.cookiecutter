# Cookiecutter: Modern Python package

This Cookiecutter provides a template for modern Python packages. It provides
best practices, and uses modern versions of tooling, which allows a better
packaging experience.

Highlights:

-   Uses a `src/` layout. For arguments on why you would want this, check out
    the following blog post:
    -   https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
-   Uses Markdown for the README. Markdown is the most popular format for
    documentation and READMEs, but PyPi only supported reStructedText for a
    long time. With the new PyPi, Markdown is now supported.
-   Uses `setup.cfg` as much as possible. The `setup.py` script is the default
    way for many project to manage their metadata, but since it is a Python
    script, things tend to get overly complex. The `setup.cfg` file provides a
    cleaner and more structured alternative. The `setup.py` file remains
    present, since the `setup()` call is mandatory for setuptools to function.
