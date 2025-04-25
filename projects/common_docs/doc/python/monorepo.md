# [Monorepo Basics](https://gafni.dev/blog/cracking-the-python-monorepo/) 

[additional ressources](https://github.com/JasperHG90/uv-monorepo)

## Tools 
The monorepo is built with [uv](https://docs.astral.sh/uv/getting-started/) and [dagger](https://docs.dagger.io/ci/quickstart/daggerize/)

> UV-Git: [uv](https://github.com/astral-sh/uv)

## Setup monorepo

```
mkdir uv-dagger-dream
cd uv-dagger-dream
uv init
uv add --group dev ruff pyright             (adds dependencies to the root project)
mkdir projects
uv init --package --lib projects/lib-one
uv init --package --lib projects/lib-two
uv lock
```
This results in:
```
.
├── README.md
├── projects
│   ├── lib-one
│   │   ├── pyproject.toml
│   │   └── src
│   │       └── lib_one
│   │           └── __init__.py
│   └── lib-two
│       ├── pyproject.toml
│       └── src
│           └── lib_two
│               └── __init__.py
├── pyproject.toml
└── uv.lock
```

To create dependency between the projects:
```
uv add --package lib-two lib-one
```
The `--package` flag tells _uv_ to execute the command in the context of the _lib-two_ package. The lib-one package is added as a dependency to lib-two’s pyproject.toml and the root uv.lock file is updated automatically.

After that we have **monorepo** - two different packages in one repo.

# Python project setup

Following topics are overed:
- How exactly should project folders be organised?
- Should tests be inside or outside the package directory?
- Does the package itself belong at the root level or in a special src directory?
- And how do you properly import and test package functionality from scripts or external test files? 

[source](https://pybit.es/articles/developing-and-testing-python-packages-with-uv/)

## Challenge 

A typical and recurring problem in Python is how to import code that lives in a different place from where it is called. There are two natural ways to organise your code: modules and packages.

Python 3.3 introduced **implicit namespace packages** - no `__init__.py` is required for recognizing directories as packages (under certain conditions, see PEP 420). 
This is not a solution for this problem, though.
```
$ tree
.
├── scripts
│   └── main.py
└── src
    ├── __init__.py
    └── utils.py
```
```python
from src.utils import helper
```
>The problem can be solved with uv:
If you use `uv init --package PACKAGENAME` **build-system** section is generated into `pyproject.toml`,  which instructs uv to install the code under _PACKAGENAME_ into the virtual environment managed by uv. In other words, uv will install your package and all its dependencies into the virtual environment so that it can be used by all other scripts and modules, wherever they are.

Virtual environment is created automatically by `uv sync` if there is none and update it with the dependencies from __pyproject.toml__. You can also just create a virtual environment by `uv venv` command.

> Now it doesn’t really matter where you want to import the code you’re developing under _PACKAGENAME_, because it’s **installed in the virtual environment and thus known to all Python modules**, no matter where they are in the file system. Your package is basically like any other third-party or system package. 

This is now working:

```
$ tree
.
├── scripts
│   └── main.py
├── src
│   └── my_package
│       ├── __init__.py
│       └── utils.py
└── tests
    └── test_utils.py
```
``` python
# main.py
from my_package.utils import helper


def main():
    print(helper())

# utils.py
def helper():
    return "helper"

# test_utils.py
from my_package.utils import helper


def test_helper():
    assert helper() == "helper"
```
uv builds the package when `uv sync` is executed and installs it into virtual environment. Editable install means that changes to the source directory will immediately affect the installed package, without the need to reinstall. 