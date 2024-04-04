from setuptools import Extension, setup
#import os.path
from Cython.Build import cythonize

method_cy_names = ["fls_cy", "swgm_cy"]
extensions = [Extension(f"tfrc.methods.{name}", [f"src/tfrc/methods/{name}.pyx"]) for name in method_cy_names]

setup(
    name="tfrc",
    ext_modules=cythonize(extensions)
)