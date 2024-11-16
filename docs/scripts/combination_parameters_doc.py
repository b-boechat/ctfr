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
        self.output_path = os.path.join(COMBINATION_METHODS_DOC_FOLDER, self.method_key, FILE_NAME)

    def signature_end(self):
        parameters_names = self.method_entry["parameters"].keys()
        if parameters_names:
            segment = ", " + ", ".join(parameters_names)
        else:
            segment = ""
        return segment + ")"

    def doc_parameter(self, parameter_name):
        parameter_entry = self.method_entry["parameters"][parameter_name]
        first_line = f"**{parameter_name}** (`{parameter_entry['type_and_info']}, optional`)"
        second_line = f"   {parameter_entry['description']}"
        return first_line + "\n\n" + second_line

    def run(self, verbose=False):
        if verbose:
            print(f"Documenting {self.method_key} parameters to {self.output_path}")
        with open(self.output_path, "w") as f:
            f.write(PAGE_TITLE + "\n")
            f.write("=" * len(PAGE_TITLE) + "\n\n")
            #f.write(".. currentmodule:: ctfr" + "\n\n")
            f.write(f'.. function:: ctfr.ctfr(signal, sr, method={self.method_key}, *, <other parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write(f'.. function:: ctfr.ctfr_from_specs(specs, method={self.method_key}, *, <other parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write(f'.. function:: ctfr.methods.{self.method_key}(signal, sr, *, <other parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write(f'.. function:: ctfr.methods.{self.method_key}_from_specs(specs, *, <other parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write("See :func:`ctfr.ctfr` and :func:`ctfr.ctfr_from_specs` for more details on the general parameters for computing CTFRs. The parameters specific to this method (passed as keyword arguments) are described below." + "\n\n")
            f.write(PARAMETERS_SUBTITLE + "\n")
            f.write("-" * len(PARAMETERS_SUBTITLE) + "\n\n")
            for parameter_name in self.method_entry["parameters"].keys():
                f.write(self.doc_parameter(parameter_name) + "\n\n")


if __name__ == '__main__':
    import sys
    doc = CombinationParametersDoc(sys.argv[-1])
    doc.run(verbose=True)