#!/usr/bin/env bash
# Copyright 2017 The Regents of the University of California
#
# Licensed under the BSD-3-clause license (the "License"); you may not
# use this file except in compliance with the License.
# You are provided a copy of the license in LICENSE.md at the root of
# this project.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Helper function: Strip leading and trailing whitespaces
str_strip () {
  echo -e "$1" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'
}

###
# HACK
export PATH=$PATH:/root/bin
###

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/builds_common.sh"

echo "Performing 'bazel clean'"
bazel clean

DO_INTEGRATION_TESTS=0
BAZEL_FLAGS=""
while true; do
  if [[ "${1}" == "--integration_tests" ]]; then
    DO_INTEGRATION_TESTS=1
  else
    BAZEL_FLAGS="${BAZEL_FLAGS} ${1}"
  fi

  shift
  if [[ -z "${1}" ]]; then
    break
  fi
done

BAZEL_FLAGS=$(str_strip "${BAZEL_FLAGS}")

echo "Using Bazel flags: ${BAZEL_FLAGS}"

PIP_BUILD_TARGET="//inquiry/tools/pip_package:build_pip_package"
bazel build ${BAZEL_FLAGS} ${PIP_BUILD_TARGET} || \
      die "Build failed."

# If still in a virtualenv, deactivate it first
if [[ -n "$(which deactivate)" ]]; then
  echo "It appears that we are already in a virtualenv. Deactivating..."
  source deactivate || die "FAILED: Unable to deactivate from existing virtualenv"
fi

# Obtain the path to Python binary
#source tools/python_bin_path.sh
PYTHON_BIN_PATH=`which python` #idk not working currently..... hack

# Assume: PYTHON_BIN_PATH is exported by the script above
if [[ -z "$PYTHON_BIN_PATH" ]]; then
  die "PYTHON_BIN_PATH was not provided. Did you run configure?"
fi

# Determine the major and minor versions of Python being used (e.g., 2.7)
# This info will be useful for determining the directory of the local pip
# installation of Python
PY_MAJOR_MINOR_VER=$(${PYTHON_BIN_PATH} -V 2>&1 | awk '{print $NF}' | cut -d. -f-2)
if [[ -z "${PY_MAJOR_MINOR_VER}" ]]; then
  die "ERROR: Unable to determine the major.minor version of Python"
fi

echo "Python binary path to be used in PIP install: ${PYTHON_BIN_PATH} "\
"(Major.Minor version: ${PY_MAJOR_MINOR_VER})"

# Build PIP Wheel file
PIP_TEST_ROOT="pip_test"
PIP_WHL_DIR="${PIP_TEST_ROOT}/whl"
PIP_WHL_DIR=$(realpath ${PIP_WHL_DIR})  # Get absolute path
rm -rf ${PIP_WHL_DIR} && mkdir -p ${PIP_WHL_DIR}
bazel-bin/inquiry/tools/pip_package/build_pip_package ${PIP_WHL_DIR} || \
    die "build_pip_package FAILED"

WHL_PATH=$(ls ${PIP_WHL_DIR}/inquiry*.whl)
if [[ $(echo ${WHL_PATH} | wc -w) -ne 1 ]]; then
  die "ERROR: Failed to find exactly one built Inquiry .whl file in "\
"directory: ${PIP_WHL_DIR}"
fi

# Print the size of the PIP wheel file.
echo
echo "Size of the PIP wheel file built: $(ls -l ${WHL_PATH} | awk '{print $5}')"
echo

# Rename the whl file properly so it will have the python
# version tags and platform tags that won't cause pip install issues.
if [[ $(uname) == "Linux" ]]; then
  PY_TAGS=${WHL_TAGS[${PY_MAJOR_MINOR_VER}]}
  PLATFORM_TAG=$(to_lower "$(uname)_$(uname -m)")
# MAC has bash v3, which does not have associative array
elif [[ $(uname) == "Darwin" ]]; then
  if [[ ${PY_MAJOR_MINOR_VER} == "2.7" ]]; then
    PY_TAGS="py2-none"
  elif [[ ${PY_MAJOR_MINOR_VER} == "3.5" ]]; then
    PY_TAGS="py3-none"
  elif [[ ${PY_MAJOR_MINOR_VER} == "3.6" ]]; then
    PY_TAGS="py3-none"
  fi
  PLATFORM_TAG="any"
fi

WHL_DIR=$(dirname "${WHL_PATH}")
WHL_BASE_NAME=$(basename "${WHL_PATH}")


# Perform installation
echo "Installing pip whl file: ${WHL_PATH}"

# Create virtualenv directory for install test
VENV_DIR="${PIP_TEST_ROOT}/venv"

if [[ -d "${VENV_DIR}" ]]; then
  rm -rf "${VENV_DIR}" && \
      echo "Removed existing virtualenv directory: ${VENV_DIR}" || \
      die "Failed to remove existing virtualenv directory: ${VENV_DIR}"
fi

mkdir -p ${VENV_DIR} && \
    echo "Created virtualenv directory: ${VENV_DIR}" || \
    die "FAILED to create virtualenv directory: ${VENV_DIR}"

# Verify that virtualenv exists
if [[ -z $(which virtualenv) ]]; then
  die "FAILED: virtualenv not available on path"
fi


virtualenv --system-site-packages -p "${PYTHON_BIN_PATH}" "${VENV_DIR}" || \
    die "FAILED: Unable to create virtualenv"

source "${VENV_DIR}/bin/activate" || \
    die "FAILED: Unable to activate virtualenv"


# Install the pip file in virtual env (plus missing dependencies)

# Upgrade pip so it supports tags such as cp27mu, manylinux1 etc.
echo "Upgrade pip in virtualenv"
pip install --upgrade pip==8.1.2

# Force tensorflow reinstallation. Otherwise it may not get installed from
# last build if it had the same version number as previous build.
#PIP_FLAGS="--upgrade --force-reinstall"
pip install -v ${PIP_FLAGS} ${WHL_PATH} || \
    die "pip install (forcing to reinstall) FAILED"
echo "Successfully installed pip package ${WHL_PATH}"

if [[ -n "${NO_TEST_ON_INSTALL}" ]] &&
   [[ "${NO_TEST_ON_INSTALL}" != "0" ]]; then
  echo "NO_TEST_ON_INSTALL=${NO_TEST_ON_INSTALL}:"
  echo "  Skipping ALL Python unit tests on install"
else
  # Call run_pip_tests.sh to perform test-on-install
  "${SCRIPT_DIR}/run_pip_tests.sh" --virtualenv ||
      die "PIP tests-on-install FAILED"
fi

# Optional: Run integration tests
if [[ "${DO_INTEGRATION_TESTS}" == "1" ]]; then
  "${SCRIPT_DIR}/integration_tests.sh" --virtualenv || \
      die "Integration tests on install FAILED"
fi

deactivate || \
    die "FAILED: Unable to deactivate virtualenv"
