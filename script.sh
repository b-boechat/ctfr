#!/bin/bash

project_name="tfrc"
python_versions="cp310-cp310 cp311-cp311 cp312-cp312"

python_install_paths="/opt/python/cp310-cp310/bin/python3 /opt/python/cp311-cp311/bin/python3 /opt/python/cp312-cp312/bin/python3"
python_location="/opt/python"
python_bin="bin/python3"

cd /io
for version in $python_versions; do
    python_path=$python_location/$version/$python_bin
    PYTHON_EXEC=$python_path make wheel
    auditwheel repair dist/$(project_name)*linux*.whl
    make clean
done