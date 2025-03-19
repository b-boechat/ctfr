import os
from ctfr import _methods_dict

class CombinationMethodsDoc:
    def __init__(
        self, 
        method_key, 
        page_title="Calling signature",
        parameters_subtitle = "Parameters",
        combination_methods_doc_folder = "combination_methods",
        file_name = "calling.rst"
    ) -> None:
        self.method_key = method_key
        self.method_entry = _methods_dict[method_key]
        method_parameters = self.method_entry.get("parameters", {})
        self.parameter_names = list(method_parameters.keys())

        self.page_title = page_title
        self.parameters_subtitle = parameters_subtitle
        self.combination_methods_doc_folder = combination_methods_doc_folder
        self.file_name = file_name 


        self.output_path = os.path.join(self.combination_methods_doc_folder, self.method_key, self.file_name)

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
            f.write(self.page_title + "\n")
            f.write("-" * len(self.page_title) + "\n\n")
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
            f.write(self.parameters_subtitle + "\n")
            f.write("~" * len(self.parameters_subtitle) + "\n\n")
            for parameter in self.parameter_names:
                f.write(self.doc_parameter(parameter) + "\n\n")

def combination_methods_doc_main():

    exclude_methods_from_param_doc = [
        "mean", "hmean", "gmean", "min", "sls_i", "sls_h"
    ]

    for method_key in _methods_dict.keys():
        if method_key not in exclude_methods_from_param_doc:
            doc = CombinationMethodsDoc(method_key)
            doc.run(verbose=True)