PROJECT_NAME = ctfr

SOURCE_BASE_FOLDER = src
SOURCE_LOCATION = $(SOURCE_BASE_FOLDER)/$(PROJECT_NAME)
CY_IMPLEMENTATIONS_LOCATIONS = $(SOURCE_LOCATION)/methods/implementations

RM = rm -f
RMR = $(RM) -r
PYTHON_EXEC ?= python3
PIP = python3 -m pip
BUILD = $(PYTHON_EXEC) -m build
SETUP = $(PYTHON_EXEC) setup.py
DIST = dist

TWINE = python3 -m twine
WHEELHOUSE = wheelhouse

install:
	$(PIP) install .

sdist: clean
	CYTHONIZE=1 $(BUILD) --sdist

sdist-ship: sdist
	mv dist/* $(WHEELHOUSE)

wheel:
	CYTHONIZE=1 $(BUILD) --wheel

dev:
	CYTHONIZE=1 $(PIP) install --editable .[dev]

ext:
	CYTHONIZE=1 $(SETUP) build_ext --inplace

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
	$(TWINE) upload --repository testpypi $(DIST)/*/*
# Install with: pip install --extra-index-url https://test.pypi.org/simple/ ctfr


clean-dist:
	$(RMR) $(DIST)

clean-build:
	$(RMR) build $(SOURCE_BASE_FOLDER)/*.egg-info

clean-cache:
	find . -name __pycache__ -exec $(RMR) {} +

clean-cy: # TODO rewrite this using the .pyx files as reference, so it's possible to add .c extensions.
	$(RMR) $(CY_IMPLEMENTATIONS_LOCATIONS)/*.c
	$(RMR) $(CY_IMPLEMENTATIONS_LOCATIONS)/*.so
	$(RMR) $(CY_IMPLEMENTATIONS_LOCATIONS)/*.html

clean-wheelhouse: # This command is not run by make clean.
	$(RMR) $(WHEELHOUSE)/*


