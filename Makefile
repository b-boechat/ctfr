PROJECT_NAME = tfrc

SOURCE_BASE_FOLDER = src
SOURCE_LOCATION = $(SOURCE_BASE_FOLDER)/$(PROJECT_NAME)
CY_METHODS_LOCATION = $(SOURCE_LOCATION)/methods


CY_METHODS_FILES_NAMES_NO_EXT = swgm_cy fls_cy lt_cy # Possibly read from manifest.
CYTHON_C_FILE_PATHS = $(foreach name, $(CY_METHODS_FILES_NAMES_NO_EXT),$(CY_METHODS_LOCATION)/$(name).c)
CYTHON_SO_FILE_PATHS = $(foreach name, $(CY_METHODS_FILES_NAMES_NO_EXT),$(CY_METHODS_LOCATION)/$(name).so)

RM = rm -f
RMR = $(RM) -r
PYTHON_EXEC ?= python3
PIP = python3 -m pip
BUILD = $(PYTHON_EXEC) -m build
SETUP = $(PYTHON_EXEC) setup.py

TWINE = python3 -m twine
WHEELHOUSE = wheelhouse

install:
	$(PIP) install .

sdist: clean
	USE_CYTHON=1 $(BUILD) --sdist

sdist-ship: sdist
	mv dist/* $(WHEELHOUSE)

wheel:
	USE_CYTHON=1 $(BUILD) --wheel

dev:
	USE_CYTHON=1 $(PIP) install --editable .[dev]

ext:
	USE_CYTHON=1 $(SETUP) build_ext --inplace

uninstall:
	$(PIP) uninstall $(PROJECT_NAME)

clean: clean-dist clean-build clean-cache clean-cy

wheel-manylinux-pipeline: clean
	docker run -ti -v $(shell pwd):/io quay.io/pypa/manylinux_2_28_x86_64 /io/script.sh
#	docker run -ti -v $(shell pwd):/io quay.io/pypa/manylinux_2_28_aarch64 /io/script.sh
#	docker run -ti -v $(shell pwd):/io quay.io/pypa/manylinux_2_28_ppc64le /io/script.sh
#	docker run -ti -v $(shell pwd):/io quay.io/pypa/manylinux_2_28_s390x /io/script.sh

dist-pipeline: sdist-ship wheel-manylinux-pipeline

publish-testpypi:
	$(TWINE) upload --repository testpypi $(WHEELHOUSE)/*
# Install with: pip install --index-url https://test.pypi.org/simple/ tfrc


clean-dist:
	$(RMR) dist

clean-build:
	$(RMR) build $(SOURCE_BASE_FOLDER)/*.egg-info

clean-cache:
	find . -name __pycache__ -exec $(RMR) {} +

clean-cy:
	$(RMR) $(foreach c_file, $(CYTHON_C_FILE_PATHS),$(c_file)) 
	$(RMR) $(foreach so_file, $(CYTHON_SO_FILE_PATHS),$(so_file))

clean-wheelhouse: # This command is not run by make clean.
	$(RMR) $(WHEELHOUSE)/*


