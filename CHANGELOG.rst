=========
Changelog
=========


All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_, and this project adheres to
`Semantic Versioning`_.

`Unreleased`_
=============

Added
-----

Changed
-------

Removed
-------

`1.1.0`_ 2026-04-11
===================

Added
-----

- `pre-commit-hooks`_ ``name-tests-test`` ``--pytest-test-first``.
- `Markdown Lint`_
- `mdformat`_
- `gitlint`_
- `pyproject-fmt`_

Changed
-------

- Sort and format ``.pre-commit-config.yaml``.
- Enable Ruff show fixes.

Removed
-------

`1.0.2`_ 2025-12-05
===================

Changed
-------

- Fix description ``setup.cfg``.
- Test ``py3.10`` through ``py3.14``.

`1.0.1`_ 2024-11-22
===================

Changed
-------

- Fix project and documentation URLs in ``setup.cfg``.

`1.0.0`_ - 2024-11-21
=====================

Added
-----

- Include ``-–pre-commit`` by default because ``-–pre-commit-ruff`` extends
  ``-–pre-commit``.
- Add ``ruff`` configuration to ``pyproject.toml`` because ``ruff`` does
  not support ``setup.cfg``.
- Extend pre-commit template with ``ruff`` lint and fix.
- Add ``mypy`` configuration to ``setup.cfg`` and template.

Changed
-------

- Minimum ``tox`` version 4.2.23
- Adopt ``ruff``, ``ruff-format``, ``codespell``, and ``rst-lint`` for
  project.

Removed
-------

- ``isort`` configuration
- ``flake8`` template and configuration
- ``[testenv:publish]`` in ``tox.ini``

.. _1.0.0: https://github.com/jfishe/pyscaffoldext-pre-commit-ruff/compare/3e1993e7efea9da6d7e8007317cc6d3ea3333a65...1.0.0
.. _1.0.1: https://github.com/jfishe/pyscaffoldext-pre-commit-ruff/compare/1.0.0...1.0.1
.. _1.0.2: https://github.com/jfishe/pyscaffoldext-pre-commit-ruff/compare/1.0.1...1.0.2
.. _1.1.0: https://github.com/jfishe/pyscaffoldext-pre-commit-ruff/compare/1.0.2...1.1.0
.. _Unreleased: https://github.com/jfishe/pyscaffoldext-pre-commit-ruff/compare/1.1.0...HEAD
.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Markdown Lint: https://github.com/igorshubovych/markdownlint-cli
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html
.. _gitlint: https://github.com/hukkin/mdformat
.. _mdformat: https://github.com/hukkin/mdformat
.. _pre-commit-hooks: https://github.com/pre-commit/pre-commit-hooks
.. _pre-commit: https://pre-commit.com/
.. _pyproject-fmt: https://github.com/tox-dev/pyproject-fmt
