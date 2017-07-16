#!/bin/bash

# To be able to build source distribution from location other than project root.
# Welcome alternatives.

pushd $(dirname "${0}") > /dev/null
basedir=$(pwd -L)
popd > /dev/null

cd $basedir/../

python setup.py sdist --format=gztar --dist-dir=${1}

