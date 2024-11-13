"""Convert jupyter notebook to sphinx gallery notebook styled examples.

Usage: python ipynb_to_gallery.py <notebook.ipynb>

Dependencies:
pypandoc: install using `pip install pypandoc`
"""

IPYNB_BASE_DIR = "../examples"
OUTPUT_PY_DIR = "examples"

import pypandoc as pdoc
from pypandoc.pandoc_download import download_pandoc
import json
from os import path
import re

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

if __name__ == '__main__':
    import sys
    download_pandoc() # This is a workaround for now.
    convert_ipynb_to_gallery(sys.argv[-1])