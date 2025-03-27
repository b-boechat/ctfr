import pypandoc as pdoc
import json
from glob import glob
from os import path
import re

IPYNB_BASE_DIR = "../examples"
OUTPUT_PY_DIR = "getting_started/examples"

class GalleryGenerator:

    def __init__(self, ipynb_base_dir, output_py_dir) -> None:
        self.ipynb_base_dir = ipynb_base_dir
        self.output_py_dir = output_py_dir
        
    def run(self, file_name):

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
                python_file = '"""\n' + rst_source + '\n"""'
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

def gallery_gen_main():
    
    example_files = glob(path.join(IPYNB_BASE_DIR, "*.ipynb"))
    
    gg = GalleryGenerator(IPYNB_BASE_DIR, OUTPUT_PY_DIR)

    for example_file in example_files:
        gg.run(example_file)