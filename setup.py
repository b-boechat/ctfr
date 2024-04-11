from setuptools import Extension, setup
from os import getenv
from os.path import splitext
from glob import glob

from Cython.Build import cythonize

# Define Cython extensions to build. The pyx files are assumed to be in src/tfrc/methods.
IMPLEMENTATIONS_SOURCE_DIR = "src/tfrc/methods/implementations"
IMPLEMENTATIONS_MODULE = "tfrc.methods.implementations"

def get_cy_extensions():
    method_cy_source_paths = glob(f"{IMPLEMENTATIONS_SOURCE_DIR}/*.pyx")
    return [Extension(f"{IMPLEMENTATIONS_MODULE}.{path.split('/')[-1].split('.')[-1]}", [path]) for path in method_cy_source_paths]

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

extensions = get_cy_extensions()

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
