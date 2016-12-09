#!/bin/bash

APELLA_SOURCE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p ${APELLA_SOURCE}/pip-deps
pip install --root ${APELLA_SOURCE}/pip-deps -r ${APELLA_SOURCE}/pip_requirements_debian.txt
