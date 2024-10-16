"""Add pre-commit-ruff extension."""

import string
from functools import partial
from typing import List

from pyscaffold import shell, structure
from pyscaffold.actions import Action, ActionParams, ScaffoldOpts, Structure
from pyscaffold.exceptions import ShellCommandException
from pyscaffold.extensions import Extension, venv
from pyscaffold.file_system import chdir
from pyscaffold.log import logger
from pyscaffold.operations import FileOp, no_overwrite
from pyscaffold.structure import AbstractContent, ResolvedLeaf
from pyscaffold.templates import get_template

from . import templates as my_templates

EXECUTABLE = "pre-commit"
CMD_OPT = "____command-pre_commit"  # we don't want this to be persisted
INSERT_AFTER = ".. _pyscaffold-notes:\n"

UPDATE_MSG = """
It is a good idea to update the hooks to the latest version:

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.
"""

SUCCESS_MSG = "\nA pre-commit hook was installed in your repo." + UPDATE_MSG

ERROR_MSG = """
Impossible to install pre-commit automatically, please open an issue in
https://github.com/pyscaffold/pyscaffold/issues.
"""

INSTALL_MSG = f"""
A `.pre-commit-config.yaml` file was generated inside your project but in
order to make sure the hooks will run, please install `pre-commit`:

    cd {{project_path}}
    # it is a good idea to create and activate a virtualenv here
    pip install pre-commit
{UPDATE_MSG}
"""

README_NOTE = f"""
Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd {{name}}
    pre-commit install
{UPDATE_MSG.replace(':', '::')}
.. _pre-commit: https://pre-commit.com/
"""

PYPROJ_INSERT_AFTER = 'version_scheme = "no-guess-dev"\n'


class PreCommitRuff(Extension):
    """Generate pre-commit configuration file.

    This class serves as the skeleton for your new PyScaffold Extension. Refer
    to the official documentation to discover how to implement a PyScaffold
    extension - https://pyscaffold.org/en/latest/extensions.html
    """

    def activate(self, actions: List[Action]) -> List[Action]:
        """Activate extension.

        See :obj:`pyscaffold.extension.Extension.activate`.

        Args:
            actions (list): list of actions to perform

        Returns:
            list: updated list of actions
        """
        actions = self.register(actions, add_files, after="define_structure")
        actions = self.register(actions, find_executable, after="define_structure")
        return self.register(actions, install, before="report_done")


def add_files(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Add .pre-commit-config.yaml file to structure."""
    files: Structure = {
        ".pre-commit-config.yaml": (
            get_template(
                name="pre-commit-ruff-config", relative_to=my_templates.__name__
            ),
            no_overwrite(),
        ),
    }

    struct = structure.modify(
        struct,
        "README.rst",
        partial(add_instructions, opts),
    )
    struct = structure.modify(
        struct,
        "pyproject.toml",
        partial(add_pyproject, opts),
    )
    return structure.merge(struct, files), opts


def find_executable(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Find the pre-commit executable that should run later in the next action...

    Or take advantage of the venv to install it...
    """
    pre_commit = shell.get_command(EXECUTABLE)
    opts = opts.copy()
    if pre_commit:
        opts.setdefault(CMD_OPT, pre_commit)
    else:
        # We can try to add it for venv to install... it will only work if the user is
        # already creating a venv anyway.
        opts.setdefault("venv_install", []).extend(["pre-commit"])

    return struct, opts


def install(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Attempt to install pre-commit in the project."""
    project_path = opts.get("project_path", "PROJECT_DIR")
    pre_commit = opts.get(CMD_OPT) or shell.get_command(EXECUTABLE, venv.get_path(opts))
    # ^  try again after venv, maybe it was installed
    if pre_commit:
        try:
            with chdir(opts.get("project_path", "."), **opts):
                pre_commit("install", pretend=opts.get("pretend"))
            logger.warning(SUCCESS_MSG)
            return struct, opts
        except ShellCommandException:
            logger.error(ERROR_MSG, exc_info=True)

    logger.warning(INSTALL_MSG.format(project_path=project_path))
    return struct, opts


def add_instructions(
    opts: ScaffoldOpts, content: AbstractContent, file_op: FileOp
) -> ResolvedLeaf:
    """Add pre-commit instructions to README."""
    text = structure.reify_content(content, opts)
    if text is not None:
        i = text.find(INSERT_AFTER)
        assert i > 0, f"{INSERT_AFTER!r} not found in README template:\n{text}"
        j = i + len(INSERT_AFTER)
        text = text[:j] + README_NOTE.format(**opts) + text[j:]
    return text, file_op


def add_pyproject(
    opts: ScaffoldOpts, content: AbstractContent, file_op: FileOp
) -> ResolvedLeaf:
    """Append Ruff configuration to pyproject.toml."""
    template: string.Template = get_template(
        name="pyproject_toml",
        relative_to=my_templates.__name__,
    )

    text = structure.reify_content(content, opts)
    if text is not None:
        i = text.find(PYPROJ_INSERT_AFTER)
        assert i > 0, (
            f"{PYPROJ_INSERT_AFTER!r} not found in " f"pyproject.toml template:\n{text}"
        )
        j = i + len(PYPROJ_INSERT_AFTER)
        text = (
            text[:j]
            + str(
                structure.reify_content(template, opts),
            )
            + text[j:]
        )
    return text, file_op
