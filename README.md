# UV Cookiecutter

[![License](https://img.shields.io/github/license/jevandezande/uv-cookiecutter)](https://github.com/jevandezande/uv-cookiecutter/blob/master/LICENSE)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://docs.astral.sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Markdown style: rumdl](https://img.shields.io/badge/md%20style-rumdl-000000.svg)](https://rumdl.dev)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/jevandezande/uv-cookiecutter/test.yml?branch=master&logo=github-actions)](https://github.com/jevandezande/uv-cookiecutter/actions/)
[![Codecov](https://img.shields.io/codecov/c/github/jevandezande/uv-cookiecutter/master)](https://app.codecov.io/github/jevandezande/uv-cookiecutter/branch/master)

[Cookiecutter](https://github.com/audreyr/cookiecutter) for setting up [uv](https://docs.astral.sh/uv) projects with all the necessary features for modern python development.

## Features

- Packaging with [uv](https://docs.astral.sh/uv)
- Environment loading with [direnv](https://direnv.net)
- Formatting and linting of Python with [ruff](https://github.com/charliermarsh/ruff)
- Formatting and linting of Markdown with [rumdl](http://rumdl.dev)
- Static typing with [ty](https://github.com/astral-sh/ty)
- Testing with [pytest](https://docs.pytest.org/en/latest)
- Git hooks that run all the above with [prek](https://prek.j178.dev)
- Continuous integration with [GitHub Actions](https://github.com/features/actions)
- Code coverage with [Codecov](https://docs.codecov.com/docs)

## Setup

Install `uv` and `direnv`, and optionally the [GitHub CLI](https://cli.github.com/), which is
required when `github_setup` is used.

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -sfL https://direnv.net/install.sh | bash

# Optional
curl -sS https://webi.sh/gh | sh
```

See [notes.md](notes.md#project-tools) for optional dependencies and [alternative installation methods](notes.md#alternative-installation-methods).

```sh
# Use cookiecutter to create a project from this template
uvx cookiecutter gh:jevandezande/uv-cookiecutter
```

The cookiecutter will automagically:

- Write the project from the answers
- Initialize git
- Add the requested dependencies and create the environment with `uv sync`
- Allow direnv, so the environment activates on `cd`
- Install pre-commit and pre-push hooks with prek
- Set up the chosen coding agent, if any
- Run the project's own commit and push hooks, tests included, and report anything they flag
- Make the initial commit
- Add the `origin` remote and, if requested, create the GitHub repository and push

Cookiecutter deletes the output directory when a hook fails. Keep it with
`--keep-project-on-failure`.

## Options

| Option | Description |
| --- | --- |
| `package_name` | Importable package name, defaulting to `project_name` lowercased with `_` for spaces and dashes. Names the repository, the output directory, and the source directory |
| `project_url` | Repository URL, defaulting to the GitHub one built from `github_username` and `package_name`. Used for the README badges, and as the `origin` remote when `github_setup=None` |
| `dependencies` | Space-separated runtime dependencies, with `@` pinning a version (e.g. `numpy scipy@1.14.*`). Written to `[project.dependencies]` |
| `dev_dependencies` | Same, written to the `dev` dependency group alongside the tools the template pins |
| `python_version` | Minimum `major.minor` version, written to `requires-python` and used by the test matrix |
| `line_length` | Ruff line length, 80 or greater |
| `license` | `MIT`, `Apache-2.0`, `BSD-3-Clause`, or `None`. `None` writes no LICENSE and declares no license in `pyproject.toml` |
| `publish_on_pypi` | Keep `publish.yml`, which builds, smoke-tests, and publishes on a GitHub release |
| `github_setup` | Create the GitHub repository as `private`, `internal`, `public`, or `None`. The repository is `github_username/package_name`, so `internal` needs `github_username` to be an organization |
| `coding_agent` | `Claude`, `Codex`, or `None`. `AGENTS.md` is always written, and every agent reads it; `Claude` additionally gets `.claude/settings.json`. The skills land in `.claude/skills/` either way |

`github_username` is required when `github_setup` is not `None`, since it owns the new repository.

## Recommendations

- Make a custom config file (see [template_config.yml](template_config.yml)).
- Install [act](https://github.com/nektos/act) to run GitHub Actions locally.

Read [notes](notes.md) for more tips.

If you need packages from conda or multi-language support, check out `pixi` and the [pixi-cookiecutter](https://github.com/jevandezande/pixi-cookiecutter).
