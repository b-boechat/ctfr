from setuptools import Extension, setup
from os import getenv
from os.path import splitext

from Cython.Build import cythonize

# Define Cython extensions to build. The pyx files are assumed to be in src/tfrc/methods.
method_cy_names = [
    "swgm_cy",
    "fls_cy", 
    "lt_cy"
]

extensions = [Extension(f"tfrc.methods.{name}", [f"src/tfrc/methods/{name}.pyx"]) for name in method_cy_names]

# Function to call when building from C code (no cythonization)
# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions

CYTHONIZE = bool(int(getenv("CYTHONIZE", 0)))

if CYTHONIZE:
    print("Building from .pyx files.")
    from Cython.Build import cythonize
    compiler_directives = {"language_level": 3}
    ext_modules = cythonize(extensions, compiler_directives=compiler_directives)
    
else:
    print("Building from .c files.")
    ext_modules = no_cythonize(extensions)


setup(
    name="tfrc",
    ext_modules=cythonize(ext_modules)
)
