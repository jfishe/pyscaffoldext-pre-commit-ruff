pyscaffoldext-pre-commit-ruff
=============================

.. image:: https://github.com/jfishe/pyscaffoldext-pre-commit-ruff/actions/workflows/publish-package.yml/badge.svg
   :target: https://github.com/jfishe/pyscaffoldext-pre-commit-ruff/actions/workflows/publish-package.yml
   :alt: Test and Publish Python 🐍 distribution 📦 to PyPI and TestPyPI
.. image:: https://img.shields.io/pypi/v/pyscaffoldext-pre-commit-ruff.svg
   :target: https://pypi.org/project/pyscaffoldext-pre-commit-ruff/
   :alt: PyPI Version
.. image:: https://img.shields.io/pypi/pyversions/pyscaffoldext-pre-commit-ruff.svg
   :alt: Python Versions
.. image:: https://readthedocs.org/projects/pyscaffoldext-pre-commit-ruff/badge/?version=latest
   :target: https://pyscaffoldext-pre-commit-ruff.readthedocs.io/en/latest/
   :alt: Documentation Status
.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :target: https://pre-commit.com/
   :alt: pre-commit enabled
.. image:: https://img.shields.io/badge/linting-ruff-blue
   :alt: Ruff
.. image:: https://coveralls.io/repos/github/jfishe/pyscaffoldext-pre-commit-ruff/badge.svg?branch=main
   :target: https://coveralls.io/github/jfishe/pyscaffoldext-pre-commit-ruff?branch=main
   :alt: Coverage Status

`PyScaffold`_ extension to use the `Ruff Linter`_ and `Ruff Formatter`_
in place of the `Pre Commit Extension`_, ``putup --pre-commit`` defaults
`flake8`_ and `isort`_.

The ``ruff`` configuration is added to ``pyproject.toml`` because
``ruff`` does not support ``setup.cfg``. Some `Ruff Linter`_ recommended
settings are commented out, for consistency with `PyScaffold`_'s
``flake8`` settings.

Uncomment to enable `pre-commit`_ additional hook in ``.pre-commit-config.yaml``.

  - `pre-commit-hooks`_ ``name-tests-test`` ``--pytest-test-first``.
  - `Markdown Lint`_
  - `mdformat`_
  - `gitlint`_
  - `Codespell`_
  - `pyproject-fmt`_

`Mypy`_ settings are added to ``setup.cfg``.

Usage
-----

Just install this package with
``pip install pyscaffoldext-pre-commit-ruff`` and note that ``putup -h``
shows a new option ``--pre-commit-ruff``. Use this flag to use the `Ruff
Linter`_ and `Ruff Formatter`_ in place of ``putup --pre-commit``
defaults `flake8`_ and `isort`_.

.. _pyscaffold-notes:

Making Changes & Contributing
-----------------------------

This project uses `pre-commit`_, please make sure to install it before
making any changes:

::

   uv tool install pre-commit
   cd pyscaffoldext-pre-commit-ruff
   pre-commit install

It is a good idea to update the hooks to the latest version:

::

   pre-commit autoupdate

Note
----

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.

.. _Codespell: https://github.com/codespell-project/codespell
.. _Markdown Lint: https://github.com/igorshubovych/markdownlint-cli
.. _Mypy: https://mypy.readthedocs.io/
.. _Pre Commit Extension: https://pyscaffold.org/en/stable/features.html#pre-commit-hooks
.. _PyScaffold: https://pyscaffold.org/
.. _Ruff Formatter: https://docs.astral.sh/ruff/formatter/
.. _Ruff Linter: https://docs.astral.sh/ruff/linter/
.. _flake8: https://flake8.pycqa.org/
.. _gitlint: https://github.com/hukkin/mdformat
.. _isort: https://pycqa.github.io/isort/
.. _mdformat: https://github.com/hukkin/mdformat
.. _pre-commit-hooks: https://github.com/pre-commit/pre-commit-hooks
.. _pre-commit: https://pre-commit.com/
.. _pyproject-fmt: https://github.com/tox-dev/pyproject-fmt
