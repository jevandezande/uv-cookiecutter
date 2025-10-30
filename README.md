# UV Cookiecutter
[![License](https://img.shields.io/github/license/jevandezande/uv-cookiecutter)](https://github.com/jevandezande/uv-cookiecutter/blob/master/LICENSE)
[![Powered by: uv](https://img.shields.io/badge/-uv-purple)](https://docs.astral.sh/uv)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Typing: ty](https://img.shields.io/badge/typing-ty-EFC621.svg)](https://github.com/astral-sh/ty)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/jevandezande/uv-cookiecutter/test.yml?branch=master&logo=github-actions)](https://github.com/jevandezande/uv-cookiecutter/actions/)
[![Codecov](https://img.shields.io/codecov/c/github/jevandezande/uv-cookiecutter)](https://app.codecov.io/github/jevandezande/uv-cookiecutter)

[Cookiecutter](https://github.com/audreyr/cookiecutter) for setting up [uv](https://docs.astral.sh/uv) projects with all the necessary features for modern python development.

## Features
- Packaging with [uv](https://docs.astral.sh/uv)
- Environment loading with [direnv](https://direnv.net)
- Formatting and linting with [ruff](https://github.com/charliermarsh/ruff)
- Static typing with [ty](https://github.com/astral-sh/ty)
- Testing with [pytest](https://docs.pytest.org/en/latest)
- Git hooks that run all the above with [pre-commit](https://pre-commit.com)
- Continuous integration with [GitHub Actions](https://github.com/features/actions)
- Code coverage with [Codecov](https://docs.codecov.com/docs)


## Setup
While all of the steps are automated, you will need to first install `uv`, `cookiecutter`, and `direnv`, and optionally install the [GitHub-CLI](https://cli.github.com/).

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -sfL https://direnv.net/install.sh | bash

# Optional
curl -sS https://webi.sh/gh | sh
```
See [notes.md](notes.md#Project-Tools) for optional dependencies and [alternative installation methods](notes.md#Alternative-installation-methods).

```sh
# Use cookiecutter to create a project from this template
cookiecutter gh:jevandezande/uv-cookiecutter
```

The cookiecutter will automagically
- Generate a project with the input configuration
- Initialize git
- Setup environment
- Setup pre-commit and pre-push hooks
- Make initial commit
- Sets up remote on GitHub (optional)


## Recommendations
- Make a custom config file (see [template_config.yml](template_config.yml)).
- Install [act](https://github.com/nektos/act) to run GitHub Actions locally.
- Install [direnv](https://direnv.net) to automagically load the environment.

Read [notes](notes.md) for more tips.

This package is derived from the [pixi-cookiecutter](https://github.com/jevandezande/pixi-cookiecutter), which is a great alternative if you prefer something that can natively handle conda packages.
