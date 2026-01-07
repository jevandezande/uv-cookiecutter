"""Hooks for setting up project once generated."""

import logging
import shutil
import subprocess
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from shutil import rmtree
from typing import Any, Literal

logger = logging.Logger("post_gen_project_logger")
logger.setLevel(logging.INFO)


PROTOCOL = Literal["git", "https"]
GITHUB_PRIVACY_OPTIONS = ["private", "internal", "public"]
MINIMUM_PYTHON_MINOR_VERSION = 12


class CodingAgent(str, Enum):
    """Coding agents supported."""

    CLAUDE = "claude"
    CODEX = "codex"


def call(cmd: str, check: bool = True, **kwargs: Any) -> subprocess.CompletedProcess[bytes]:
    """
    Call shell commands.

    :param cmd: command to call
    :param check: whether to raise an exception if the command fails
    :param kwargs: keyword arguments to pass to subprocess.call

    Warning: strings with spaces are not yet supported.
    """
    logger.debug(f"Calling: {cmd}")
    return subprocess.run(cmd.split(), check=check, **kwargs)


def set_python_version() -> None:
    """Set the python version in pyproject.toml and .github/workflows/test.yml."""
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    logger.info(f"Settting {python_version=}")
    if sys.version_info.minor < MINIMUM_PYTHON_MINOR_VERSION:
        logger.warning(
            f"{python_version=} should be upgraded to the latest avaiable python version."
        )

    file_names = [
        ".github/workflows/test.yml",
        "pyproject.toml",
    ]

    for file_name in file_names:
        with open(file_name) as f:
            contents = f.read().replace("{python_version}", python_version)
        with open(file_name, "w") as f:
            f.write(contents)


def set_license(license: str | None = "MIT") -> None:
    """
    Copy the license file to LICENSE (if any).

    :param license: name of the license (or None for no license)
    """
    if not license or license == "None":
        logger.debug("No license set")
        return

    licenses = {lic.name for lic in Path("data/licenses").iterdir()}
    if license not in licenses:
        try:
            # Check and correct cases
            license = next(lic for lic in licenses if lic.lower() == license.lower())
            logger.warning(f"Corrected license to {license=}")
        except StopIteration as e:
            raise ValueError(f"{license=} not available; select from:\n{licenses}") from e

    shutil.copy(f"data/licenses/{license}", "LICENSE")

    with open("LICENSE") as f:
        contents = f.read().replace("{year}", f"{datetime.now().year}")
        contents = contents.replace("{author_name}", "{{cookiecutter.author_name}}")
    with open("LICENSE", "w") as f:
        f.write(contents)

    logger.debug(f"Set {license=}")


def git_init() -> None:
    """Initialize a git repository."""
    call("git init")


def process_dependencies(deps: str) -> str:
    r"""
    Process a space separated list of dependencies.

    :param deps: dependencies to process
    :param sep: separator between dependencies
    :return: processed dependencies in the format '"package=version",\n...'

    >>> process_dependencies(' ')
    ''
    >>> process_dependencies("pytest matplotlib~=3.7 black!=1.2.3")
    '    "pytest",\n    "matplotlib~=3.7",\n    "black!=1.2.3",\n'
    """
    if not deps.strip():
        return ""

    return "".join(f'    "{dep}",\n' for dep in deps.split())


def update_dependencies() -> None:
    """Add and update the dependencies in pyproject.toml and uv.lock."""
    # Extra space and .strip() avoids accidentally creating '""""'
    dependencies = process_dependencies("""{{cookiecutter.dependencies}} """.strip())
    dev_dependencies = process_dependencies("""{{cookiecutter.dev_dependencies}} """.strip())

    with open("pyproject.toml") as f:
        contents = (
            f.read()
            .replace("    {dependencies}\n", dependencies)
            .replace("    {dev_dependencies}\n", dev_dependencies)
        )
    with open("pyproject.toml", "w") as f:
        f.write(contents)

    call("uv sync")


def check_program(program: str, install_str: str, **run_kwargs: Any) -> None:
    """
    Check that a program is installed.

    :param program: name of the program to check
    :param install_str: string to print if the program is not installed

    >>> check_program("python", "https://www.python.org")
    >>> check_program("this_program_does_not_exist", "nothing")
    Traceback (most recent call last):
    ...
    OSError: this_program_does_not_exist is not installed; install with `nothing`
    """
    try:
        call(program, stdout=subprocess.DEVNULL, **run_kwargs)
    except FileNotFoundError as e:
        raise OSError(f"{program} is not installed; install with `{install_str}`") from e
    except subprocess.CalledProcessError as e:
        raise OSError(f"Issue with {program} encountered") from e


def allow_direnv() -> None:
    """Allow direnv."""
    check_program("direnv", "pixi global install direnv")
    call("direnv allow .")


def git_hooks() -> None:
    """Install pre-commit and pre-push hooks (via prek)."""
    call("uv run prek install")


def setup_coding_agent(agent: str) -> None:
    """
    Set up coding agent including readme and environment.

    :param agent: coding agent name ("claude", "codex", or "none")
    """
    if agent.lower() == "none":
        return

    coding_agent = CodingAgent(agent.lower())
    logger.info(f"Setting up {coding_agent} coding agent.")

    # Copy agent README to appropriate filename
    source = Path("data/AGENTS_README.md")
    match coding_agent:
        case CodingAgent.CLAUDE:
            destination = Path("CLAUDE.md")
        case CodingAgent.CODEX:
            destination = Path("AGENTS.md")
        case _:
            raise ValueError(f"Unsupported coding agent: {coding_agent}")

    shutil.copy(source, destination)
    logger.info(f"Copied {source} to {destination}")

    # Set up agent environment
    match coding_agent:
        case CodingAgent.CLAUDE:
            logger.info("Type /init in claude to finish setup and then exit.")
            shutil.copytree("data/.claude", ".claude")
            try:
                call(str(Path("~").expanduser() / ".claude/local/claude"))
            except FileNotFoundError as e:
                raise OSError(
                    "claude failed to run, check if installed in `~/.claude/local/claude`\n"
                    "or install with: `npm install -g @anthropic-ai/claude-code`"
                ) from e
        case CodingAgent.CODEX:
            try:
                call("codex")
            except FileNotFoundError as e:
                raise OSError(
                    "codex failed to run, check if installed\n"
                    "or install with appropriate package manager"
                ) from e
        case _:
            raise ValueError(f"Unsupported coding agent: {coding_agent}")


def remove_data_dir() -> None:
    """Remove the data directory."""
    rmtree("data")


def git_initial_commit() -> None:
    """Make the initial commit."""
    call("git add .")
    call("git commit -m Setup")


def setup_remote(remote: str = "origin") -> None:
    """
    Add remote (and optionally setup GitHub).

    :param remote: name for the remote
    :raises ValueError: if the privacy option is not valid
    """
    if "{{cookiecutter.github_setup}}" != "None":  # type: ignore [comparison-overlap]  # noqa: PLR0133
        github_setup("{{cookiecutter.github_setup}}", remote)
    else:
        git_add_remote(remote, "{{cookiecutter.project_url}}")


def git_add_remote(remote: str, url: str, protocol: PROTOCOL = "git") -> None:
    """
    Add a remote to the git repository.

    :param remote: name for the remote
    :param url: url of remote
    :param protocol: protocol of the remote ("git" or "https")
    """
    if protocol == "git":
        _, _, hostname, path = url.split("/", 3)
        url = f"{protocol}@{hostname}:{path}"

    call(f"git remote add {remote} {url}")


def github_setup(privacy: str, remote: str = "origin", default_branch: str = "master") -> None:
    """
    Make a repository on GitHub (requires GitHub CLI).

    :param privacy: privacy of the repository ("private", "internal", "public")
    :param remote: name of the remote to add
    :param default_branch: name of the default branch for upstream
    """
    if privacy not in GITHUB_PRIVACY_OPTIONS:
        raise ValueError(f"{privacy=} not in {GITHUB_PRIVACY_OPTIONS}")

    check_program("gh", "https://cli.github.com/")

    try:
        call(
            f"gh repo create {{cookiecutter.package_name}} --{privacy} --remote {remote} --source ."
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating GitHub repository, likely already exists: {e}")

    try:
        call(f"git config branch.{default_branch}.remote {remote}")
        call(f"git config branch.{default_branch}.merge refs/heads/{default_branch}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting upstream to {default_branch}: {e}")


def notes() -> None:
    """Print notes for the user."""
    print(
        """
If using GitHub, generate a CODECOV_TOKEN at:
https://app.codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.package_name}}/settings
and add it to the GitHub repository secrets as CODECOV_TOKEN at:
https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.package_name}}/settings/secrets/actions
"""
    )


SUCCESS = "\x1b[1;32m"
TERMINATOR = "\x1b[0m"


def main() -> None:
    """Run the post generation hooks."""
    set_python_version()
    set_license("{{cookiecutter.license}}")
    git_init()
    update_dependencies()
    allow_direnv()
    git_hooks()
    setup_coding_agent("{{cookiecutter.coding_agent}}")
    remove_data_dir()
    git_initial_commit()
    setup_remote("origin")

    notes()

    print(f"{SUCCESS}Project successfully initialized{TERMINATOR}")


if __name__ == "__main__":
    main()
