# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('../..')))
sys.setrecursionlimit(1500)

# -- Project information -----------------------------------------------------

project = 'Ontologysim'
copyright = '2020, wbk'
author = 'Lars Kiefer, Marvin May'

# The full version, including alpha/beta/rc tags
release = '29.11.2020'
version = '1.0'
# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions=['recommonmark','sphinx.ext.autodoc','sphinx.ext.autosummary','sphinx.ext.doctest','sphinx.ext.todo',
'sphinx.ext.coverage','sphinx.ext.githubpages','sphinx.ext.napoleon','sphinx.ext.intersphinx','sphinx_markdown_tables',
'sphinx.ext.autosectionlabel'
]


templates_path = [ '_templates' ]


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.



# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

source_suffix = ['.rst', '.md']
# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}
html_theme = 'sphinx_rtd_theme'

napoleon_google_docstring=True
napoleon_numpy_docstring=True
napoleon_include_init_with_doc=False
napoleon_include_private_with_doc=False
napoleon_include_special_with_doc=True
napoleon_use_admonition_for_examples=False
napoleon_use_admonition_for_notes=False
napoleon_use_admonition_for_references=False
napoleon_use_ivar=False
napoleon_use_param=True
napoleon_use_rtype=True