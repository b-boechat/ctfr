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

        self.init_defaults(page_title, parameters_subtitle, combination_methods_doc_folder, file_name)
        self.method_key = method_key
        self.method_entry = _methods_dict[method_key]
        self.parameter_names = list(self.method_entry.get("parameters", {}).keys())
        self.output_path = os.path.join(self.combination_methods_doc_folder, self.method_key, self.file_name)

    def init_defaults(self, page_title, parameters_subtitle, combination_methods_doc_folder, file_name):
        self.page_title = page_title
        self.parameters_subtitle = parameters_subtitle
        self.combination_methods_doc_folder = combination_methods_doc_folder
        self.file_name = file_name

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
            f.write(f'.. function:: ctfr.methods.{self.method_key}(signal, sr, *, <shared parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write(f'.. function:: ctfr.methods.{self.method_key}_from_specs(specs, *, <shared parameters>')
            f.write(self.signature_end() + "\n" + "   :noindex:" + "\n\n")
            f.write(f'.. note::' + "\n" + "   " + "As with all combination methods, you can also use :func:`ctfr.ctfr` or :func:`ctfr.ctfr_from_specs`." "\n\n")
            f.write("See :func:`ctfr.ctfr` and :func:`ctfr.ctfr_from_specs` for more details on the shared parameters for computing CTFRs with this package.")
            if self.parameter_names:
                f.write(" The parameters specific to this method (passed as keyword arguments) are described below." + "\n\n")
                f.write(self.parameters_subtitle + "\n")
                f.write("~" * len(self.parameters_subtitle) + "\n\n")
                for parameter in self.parameter_names:
                    f.write(self.doc_parameter(parameter) + "\n\n")

class CombinationMethodsWithVariantsDoc(CombinationMethodsDoc):
    # TODO implement this class if more methods with variants are added.

    def __init__(
        self, 
        method_keys, 
        page_title="Calling signature", 
        parameters_subtitle="Parameters", 
        combination_methods_doc_folder="combination_methods", 
        file_name="calling.rst"
    ):
        self.init_defaults(page_title, parameters_subtitle, combination_methods_doc_folder, file_name)

        self.method_keys_iter = list(method_keys)
        self.method_entries_map = {key: _methods_dict[key] for key in self.method_keys_iter}
        self.parameter_names_map = {key: list(self.method_entries_map[key].get("parameters", {}).keys()) for key in self.method_keys_iter}
        self.output_path = os.path.join(self.combination_methods_doc_folder, self.method_key, self.file_name)

    def get_parameter_names_map(self):
        pass
        

def combination_methods_doc_main():

    exclude_methods_from_param_doc = [
        "mean", "hmean", "gmean", "min", "sls_i", "sls_h"
    ]

    for method_key in _methods_dict.keys():
        if method_key not in exclude_methods_from_param_doc:
            doc = CombinationMethodsDoc(method_key)
            doc.run(verbose=True)