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

import pypandoc as pdoc
from pypandoc.pandoc_download import download_pandoc
import json
from os import path
import re

IPYNB_BASE_DIR = "../examples"
OUTPUT_PY_DIR = "getting_started/examples"

def convert_ipynb_to_gallery(file_name):

    if not file_name.endswith(".ipynb"):
        file_name = file_name + ".ipynb"
    input_path = path.join(IPYNB_BASE_DIR, file_name)
    output_path = path.join(OUTPUT_PY_DIR, file_name.replace(".ipynb", ".py"))

    note_md_pattern = re.compile(r"\s*\*\*Note:\*\*\s*")

    nb_dict = json.load(open(input_path))
    cells = nb_dict["cells"]

    for i, cell in enumerate(cells):
        if i == 0:  
            assert cell["cell_type"] == "markdown", \
                "First cell has to be markdown"

            md_source = "".join(cell["source"])
            rst_source = pdoc.convert_text(md_source, "rst", "md")
            python_file = """"\n" + rst_source + "\n""""
        else:
            if cell["cell_type"] == "markdown":
                md_source = "".join(cell["source"])
                rst_source = pdoc.convert_text(md_source, "rst", "md")
                rst_source = note_md_pattern.sub(".. note::\n   ", rst_source)
                commented_source = "\n".join(["# " + x for x in
                                              rst_source.split("\n")])
                python_file = python_file + "\n\n\n" + "#" * 70 + "\n" + \
                    commented_source
            elif cell["cell_type"] == "code":
                source = "".join(cell["source"])
                python_file = python_file + "\n" * 2 + source

    python_file = python_file.replace("\n%", "\n# %")
    open(output_path, "w").write(python_file)

example_files = ["basic_usage"] # TODO audio isn"t copied, but should be turned into an asset anyway.

for example_file in example_files:
    convert_ipynb_to_gallery(example_file)
    