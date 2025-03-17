# Documentation

## MKDOCS [mkdocs](https://www.mkdocs.org/)

to setup the tool:

- `pip install mkdocs`

To generate the documentation from the docstrings from code. [mkdocstrings](https://mkdocstrings.github.io/)

- `pip install "mkdocstrings[python]"`

The last is the theme [mkdocs-material-theme](https://github.com/squidfunk/mkdocs-material).

- `pip install mkdocs-material`

Tool to generate documentation from the source code. To configure the project: `mkdocs new .` will genrate docs folder with index.md inside. and mkdocs.yml file for configuration.

### Configuration of mkdocs

in mkdocs.yml

```yml
# document name
site_name: My Doc

# setting up the theme for documentation
theme:
  name: "material"

# to generate documentation from docstrings from code
plugins:
  - mkdocstrings
  
# include new chapter / md files
nav:
  - index.md
  - tutorials.md
  - how-to-guides.md
  - reference.md
  - explanation.md
```

This is how the subpages can be added in index.md file:

```md
1. [Tutorials](tutorials.md)
2. [How-To Guides](how-to-guides.md)
3. [Reference](reference.md)
4. [Explanation](explanation.md)
```

To use the docstrings in documentation: `::: udentifier`

```md
::: spec_handler.handler
```

spec_handler: folder with `__init__.py`
handler: is the handler.py within the spec_handler folder.

- to build the documentation as html file: `mkdocs build`
- to generate the documentation and to show it on a local host: `mkdocs serve`