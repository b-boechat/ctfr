# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath("../src/ctfr"))
sys.path.append(os.path.relpath("./conf_extras"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ctfr"
author = "Bernardo A. Boechat, Maurício do V. M. da Costa, Luiz W. P. Biscainho"
copyright = "2024, Bernardo A. Boechat, Maurício do V. M. da Costa, Luiz W. P. Biscainho"
from ctfr import __version__
version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.imgmath",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx_gallery.gen_gallery"
]

intersphinx_disabled_reftypes = ["*"]

templates_path = ["_templates"]
exclude_patterns = [
    "_build", 
    "Thumbs.db", 
    ".DS_Store", 
    "getting_started/examples/GALLERY_HEADER.rst"
]

sphinx_gallery_conf = {
    "examples_dirs": "getting_started/examples",
    "gallery_dirs": "getting_started/examples/gallery",
    "filename_pattern": "/basic_usage.py",
}

add_module_names = True
autodoc_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "librosa": ("https://librosa.org/doc/latest", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = False

# -- Document methods' calling signature and parameters ------------------------------------------

from combination_methods_doc import combination_methods_doc_main
combination_methods_doc_main()

# -- Generate gallery .py files from .ipynb ------------------------------------------
    
from gallery_gen import gallery_gen_main
gallery_gen_main()