PROJECT_NAME = ctfr

SOURCE_BASE_FOLDER = src
SOURCE_LOCATION = $(SOURCE_BASE_FOLDER)/$(PROJECT_NAME)
CY_IMPLEMENTATIONS_LOCATIONS = $(SOURCE_LOCATION)/implementations

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

dev:
	$(PIP) install --editable .[dev]

ext:
	$(SETUP) build_ext --inplace

uninstall:
	$(PIP) uninstall $(PROJECT_NAME)

clean: clean-dist clean-build clean-cache clean-cy

wheel:
	CYTHONIZE=1 $(BUILD) --wheel

publish-testpypi:
	$(TWINE) upload --repository testpypi $(DIST)/*/*
# Install with: pip install --extra-index-url https://test.pypi.org/simple/ ctfr

clean-dist:
	$(RMR) $(DIST)

clean-build:
	$(RMR) build $(SOURCE_BASE_FOLDER)/*.egg-info

clean-cache:
	find . -name __pycache__ -exec $(RMR) {} +

clean-cy: # Note: this could be rewriten using the .pyx files as reference, so it's possible to add .c extensions in the future.
	$(RMR) $(CY_IMPLEMENTATIONS_LOCATIONS)/*.c
	$(RMR) $(CY_IMPLEMENTATIONS_LOCATIONS)/*.so
	$(RMR) $(CY_IMPLEMENTATIONS_LOCATIONS)/*.html

clean-wheelhouse: # This command is not run by make clean.
	$(RMR) $(WHEELHOUSE)/*


