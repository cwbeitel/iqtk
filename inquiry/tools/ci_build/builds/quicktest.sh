#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/builds_common.sh"

###
# HACK
export PATH=$PATH:/root/bin
###

PIP_BUILD_TARGET="//inquiry/tools/pip_package:build_pip_package"
bazel build ${PIP_BUILD_TARGET} || die "Build failed."

PIP_TEST_ROOT="pip_test"
PIP_WHL_DIR="${PIP_TEST_ROOT}/whl"
PIP_WHL_DIR=$(realpath ${PIP_WHL_DIR})
rm -rf ${PIP_WHL_DIR} && mkdir -p ${PIP_WHL_DIR}

bazel-bin/inquiry/tools/pip_package/build_pip_package ${PIP_WHL_DIR} || \
    die "build_pip_package FAILED"

WHL_PATH=$(ls ${PIP_WHL_DIR}/inquiry*.whl)

if [[ $(echo ${WHL_PATH} | wc -w) -ne 1 ]]; then
  die "ERROR: Failed to find exactly one built Inquiry .whl file in "\
"directory: ${PIP_WHL_DIR}"
fi

"${SCRIPT_DIR}/run_pip_tests.sh" --virtualenv ||
    die "PIP tests-on-install FAILED"
