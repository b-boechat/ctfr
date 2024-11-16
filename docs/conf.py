# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('../src/ctfr'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ctfr'
copyright = '2024, Bernardo Boechat, Maurício Costa, Luiz Wagner Biscainho'
author = 'Bernardo Boechat, Maurício Costa, Luiz Wagner Biscainho'
from ctfr import __version__
version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx_gallery.gen_gallery'
]

intersphinx_disabled_reftypes = ["*"]

templates_path = ['_templates']
exclude_patterns = [
    '_build', 
    'Thumbs.db', 
    '.DS_Store', 
    'getting_started/examples/GALLERY_HEADER.rst'
]

sphinx_gallery_conf = {
    "examples_dirs": "getting_started/examples",
    "gallery_dirs": "getting_started/examples/gallery",
    "filename_pattern": "/basic_usage.py",
}

add_module_names = True
autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "librosa": ('https://librosa.org/doc/latest', None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = False

# -- Document methods' calling signature and parameters ------------------------------------------

import os
from ctfr import _methods_dict

PAGE_TITLE = "Calling signature"
PARAMETERS_SUBTITLE = "Parameters"
COMBINATION_METHODS_DOC_FOLDER = "combination_methods"
FILE_NAME = "calling.rst"

class CombinationParametersDoc:
    def __init__(self, method_key) -> None:
        self.method_key = method_key
        self.method_entry = _methods_dict[method_key]
        method_parameters = self.method_entry.get("parameters", {})
        self.parameter_names = list(method_parameters.keys())
        self.output_path = os.path.join(COMBINATION_METHODS_DOC_FOLDER, self.method_key, FILE_NAME)

    def signature_end(self):
        if self.parameter_names:
            segment = ", " + ", ".join(self.parameter_names)
        else:
            segment = ""
        return segment + ")"

    def doc_parameter(self, parameter):
        parameter_entry = self.method_entry["parameters"][parameter]
        first_line = f"**{parameter}** (`{parameter_entry['type_and_info']}, optional`)"
        second_line = f"   {parameter_entry['description']}"
        return first_line + "\n\n" + second_line

    def run(self, verbose=False):
        if verbose:
            print(f"Documenting {self.method_key} parameters to {self.output_path}")
        with open(self.output_path, "w") as f:
            f.write(PAGE_TITLE + "\n")
            f.write("-" * len(PAGE_TITLE) + "\n\n")
            #f.write(".. currentmodule:: ctfr" + "\n\n")
            f.write(f'.. function:: ctfr.ctfr(signal, sr, method="{self.method_key}", *, <shared parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write(f'.. function:: ctfr.ctfr_from_specs(specs, method="{self.method_key}", *, <shared parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write(f'.. function:: ctfr.methods.{self.method_key}(signal, sr, *, <shared parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write(f'.. function:: ctfr.methods.{self.method_key}_from_specs(specs, *, <shared parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write("See :func:`ctfr.ctfr` and :func:`ctfr.ctfr_from_specs` for more details on the shared parameters for computing CTFRs with this package. The parameters specific to this method (passed as keyword arguments) are described below." + "\n\n")
            f.write(PARAMETERS_SUBTITLE + "\n")
            f.write("~" * len(PARAMETERS_SUBTITLE) + "\n\n")
            for parameter in self.parameter_names:
                f.write(self.doc_parameter(parameter) + "\n\n")

exclude_methods_from_param_doc = [
    "mean", "median", "min", "gmean"
]
for method_key in _methods_dict.keys():
    if method_key not in exclude_methods_from_param_doc:
        doc = CombinationParametersDoc(method_key)
        doc.run(verbose=True)

# -- Generate gallery .py files from .ipynb ------------------------------------------

import pypandoc as pdoc
from pypandoc.pandoc_download import download_pandoc
import json
from os import path
import re

IPYNB_BASE_DIR = "../examples"
OUTPUT_PY_DIR = "getting_started/examples"

def convert_ipynb_to_gallery(file_name):

    if not file_name.endswith('.ipynb'):
        file_name = file_name + '.ipynb'
    input_path = path.join(IPYNB_BASE_DIR, file_name)
    output_path = path.join(OUTPUT_PY_DIR, file_name.replace('.ipynb', '.py'))

    note_md_pattern = re.compile(r"\s*\*\*Note:\*\*\s*")

    nb_dict = json.load(open(input_path))
    cells = nb_dict['cells']

    for i, cell in enumerate(cells):
        if i == 0:  
            assert cell['cell_type'] == 'markdown', \
                'First cell has to be markdown'

            md_source = ''.join(cell['source'])
            rst_source = pdoc.convert_text(md_source, 'rst', 'md')
            python_file = '"""\n' + rst_source + '\n"""'
        else:
            if cell['cell_type'] == 'markdown':
                md_source = ''.join(cell['source'])
                rst_source = pdoc.convert_text(md_source, 'rst', 'md')
                rst_source = note_md_pattern.sub(".. note::\n   ", rst_source)
                commented_source = '\n'.join(['# ' + x for x in
                                              rst_source.split('\n')])
                python_file = python_file + '\n\n\n' + '#' * 70 + '\n' + \
                    commented_source
            elif cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                python_file = python_file + '\n' * 2 + source

    python_file = python_file.replace("\n%", "\n# %")
    open(output_path, 'w').write(python_file)

example_files = ["basic_usage"] # TODO audio isn't copied, but should be turned into an asset anyway.

for example_file in example_files:
    convert_ipynb_to_gallery(example_file)
    