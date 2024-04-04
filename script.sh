#!/bin/bash

project_name="tfrc"

python_install_paths="/opt/python/cp310-cp310/bin/python3 /opt/python/cp311-cp311/bin/python3 /opt/python/cp312-cp312/bin/python3"

cd /io
for python_path in $python_install_paths; do
    #echo $project_name
    PYTHON_EXEC=$python_path make wheel
    auditwheel repair dist/$(tfrc)*linux*.whl
    make clean
done