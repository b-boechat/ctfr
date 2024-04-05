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
PIP = pip3
BUILD = $(PYTHON_EXEC) -m build
SETUP = $(PYTHON_EXEC) setup.py

install:
	$(PIP) install .

sdist:
	USE_CYTHON=1 $(BUILD) --sdist

sdist-ship: clean sdist
	mv dist/* wheelhouse

wheel:
	USE_CYTHON=1 $(BUILD) --wheel

dev:
	USE_CYTHON=1 $(PIP) install --editable .

ext:
	USE_CYTHON=1 $(SETUP) build_ext --inplace

uninstall:
	$(PIP) uninstall $(PROJECT_NAME)

clean: clean_dist clean_build clean_cache clean_cy




clean_dist:
	$(RMR) dist

clean_build:
	$(RMR) build $(SOURCE_BASE_FOLDER)/*.egg-info

clean_cache:
	find . -name __pycache__ -exec $(RMR) {} +

clean_cy:
	$(RMR) $(foreach c_file, $(CYTHON_C_FILE_PATHS),$(c_file)) 
	$(RMR) $(foreach so_file, $(CYTHON_SO_FILE_PATHS),$(so_file))

clean_wheelhouse: # This command is not run by make clean.
	$(RMR) wheelhouse