"""Test helper functions."""

import os
import shlex
import stat
import sys
import traceback
from pathlib import Path
from shutil import rmtree
from subprocess import STDOUT, CalledProcessError, check_output
from time import sleep
from uuid import uuid4
from warnings import warn

from pyscaffold.shell import get_executable

IS_POSIX = os.name == "posix"

PYTHON = sys.executable
"""Same python executable executing the tests... Hopefully the one inside the virtualenv
inside tox folder. If we install packages by mistake is not a huge problem.
"""


def uniqstr():
    """Generate a unique random long string every time it is called."""
    return str(uuid4())


def rmpath(path):
    """Carelessly/recursively remove path.

    If an error occurs it will just be ignored, so not suitable for every usage.
    The best is to use this function for paths inside pytest tmp directories, and with
    some hope pytest will also do some cleanup itself.
    """
    try:
        rmtree(str(path), onerror=set_writable)
    except FileNotFoundError:
        return
    except Exception:
        msg = f"rmpath: Impossible to remove {path}, probably an OS issue...\n\n"
        warn(msg + traceback.format_exc(), stacklevel=1)


def set_writable(func, path, _exc_info):
    """set_writable.

    :param func: Function
    :param path: Path
    :param _exc_info: Not used.
    """
    sleep(1)  # Sometimes just giving time to the SO, works

    if not Path(path).exists():
        return  # we just want to remove files anyway

    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)

    # now it either works or re-raise the exception
    func(path)


def run(*args, **kwargs):
    """Run the external command. See ``subprocess.check_output``."""
    # normalize args
    if len(args) == 1:
        if isinstance(args[0], str):
            args = shlex.split(args[0], posix=IS_POSIX)
        else:
            args = args[0]

    if args[0] in ("python", "putup", "pip", "tox", "pytest", "pre-commit"):
        raise SystemError("Please specify an executable with explicit path")

    opts = dict(stderr=STDOUT, universal_newlines=True)
    opts.update(kwargs)

    try:
        return check_output(args, **opts)
    except CalledProcessError as ex:
        print("\n\n" + "!" * 80 + "\nError while running command:")
        print(args)
        print(opts)
        traceback.print_exc()
        msg = "\n******************** Terminal ($? = {}) ********************\n{}"
        print(msg.format(ex.returncode, ex.output))
        raise


def run_common_tasks(tests=True, docs=True, pre_commit=True, install=True):
    """run_common_tasks.

    :param tests: Run tests.
    :param docs: Build docs and run doctests.
    :param pre_commit: Run pre-commit on all files.
    :param install: Install the package.
    """
    # Requires tox, setuptools_scm and pre-commit in setup.cfg ::
    # opts.extras_require.testing
    if tests:
        run(f"{PYTHON} -m tox")

    run(f"{PYTHON} -m tox -e build")
    wheels = list(Path("dist").glob("*.whl"))
    assert wheels

    run(f"{PYTHON} setup.py --version")

    if docs:
        run(f"{PYTHON} -m tox -e docs,doctests")

    if pre_commit:
        try:
            run(f"{PYTHON} -m pre_commit run --all-files")
        except CalledProcessError:
            print(run(get_executable("git"), "diff"))
            raise

    if install:
        assert Path(".venv").exists(), "Please use --venv when generating the project"
        venv_pip = get_executable("pip", prefix=".venv", include_path=False)
        assert venv_pip, "Pip not found, make sure you have used the --venv option"
        run(venv_pip, "install", wheels[0])
