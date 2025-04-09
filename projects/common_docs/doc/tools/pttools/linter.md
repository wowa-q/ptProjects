# Linter Tools

## PYLINT [pylint](https://pylint.pycqa.org/en/latest/user_guide/usage/run.html)

pylint scans the code about potential issues or error that might occur. It check also some PEP8 rules. => checking the coding style

`pylint file.py` run in the terminal the results will be printed into the terminal.
`pylint folder` to run pylint over the whole folder

### PYLINT configuration file

generate the configuration file by `pylint --generate-rcfile > .pylintrc`
will genrate the ***.pylintrc*** file, which is configuring the pylint for the whole project.

Instead of the ***.pylintrc*** file, which is only for the pylint the ***setup.cfg*** can be used.

## FLAKE8 [flake8](https://flake8.pycqa.org/en/latest/)

flake8 is checking the PEP8 rules.

`flake8 file.py` run in the terminal the results will be printed into the terminal, similar to the pylint.

.flake8 configuration file can be created, or setup.cfg

## AUTOPEP8 [autopep8](https://github.com/peter-evans/autopep8)

The tool is formating the code according to PEP8. It uses the flake8 configuration file.

`autopep8 --in-place file.py` will update the source file. `autopep8 file.py --diff` will just show what will be modified in the file, but not change it.

## MYPY [mypy](https://mypy.readthedocs.io/en/stable/)

The tool is checking the types e.g.: `def fun(var: str) -> str`
With `mypy file.py` the results will be printed in the terminal e.g. inconsistoncies in the types.
`from typing import Iterable`



# More Tools:

- [WAT](https://github.com/igrek51/wat/blob/master/README.md): WAT is a powerful inspection tool designed to help you explore unknown objects and examine them at runtime.
- [Pydantic](https://realpython.com/python-pydantic/): robust type checking and data validation - to be used in productive development