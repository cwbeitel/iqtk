
die() {
  # Print a message and exit with code 1.
  #
  # Usage: die <error_message>
  #   e.g., die "Something bad happened."

  echo $@
  exit 1
}

realpath() {
  # Get the real path of a file
  # Usage: realpath <file_path>

  if [[ $# != "1" ]]; then
    die "realpath: incorrect usage"
  fi

  [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

to_lower () {
  # Convert string to lower case.
  # Usage: to_lower <string>

  echo "$1" | tr '[:upper:]' '[:lower:]'
}

calc_elapsed_time() {
  # Calculate elapsed time. Takes nanosecond format input of the kind output
  # by date +'%s%N'
  #
  # Usage: calc_elapsed_time <START_TIME> <END_TIME>

  if [[ $# != "2" ]]; then
    die "calc_elapsed_time: incorrect usage"
  fi

  START_TIME=$1
  END_TIME=$2

  if [[ ${START_TIME} == *"N" ]]; then
    # Nanosecond precision not available
    START_TIME=$(echo ${START_TIME} | sed -e 's/N//g')
    END_TIME=$(echo ${END_TIME} | sed -e 's/N//g')
    ELAPSED="$(expr ${END_TIME} - ${START_TIME}) s"
  else
    ELAPSED="$(expr $(expr ${END_TIME} - ${START_TIME}) / 1000000) ms"
  fi

  echo ${ELAPSED}
}

run_in_directory() {
  # Copy the test script to a destination directory and run the test there.
  # Write test log to a log file.
  #
  # Usage: run_in_directory <DEST_DIR> <LOG_FILE> <TEST_SCRIPT>
  #                         [ARGS_FOR_TEST_SCRIPT]

  if [[ $# -lt "3" ]]; then
    die "run_in_directory: incorrect usage"
  fi

  DEST_DIR="$1"
  LOG_FILE="$2"
  TEST_SCRIPT="$3"
  shift 3
  SCRIPT_ARGS=("$@")

  # Get the absolute path of the log file
  LOG_FILE_ABS=$(realpath "${LOG_FILE}")

  cp "${TEST_SCRIPT}" "${DEST_DIR}"/
  SCRIPT_BASENAME=$(basename "${TEST_SCRIPT}")

  if [[ ! -f "${DEST_DIR}/${SCRIPT_BASENAME}" ]]; then
    echo "FAILED to copy script ${TEST_SCRIPT} to temporary directory "\
"${DEST_DIR}"
    return 1
  fi

  pushd "${DEST_DIR}" > /dev/null

  "${TIMEOUT_BIN}" --preserve-status ${TIMEOUT} \
    "${PYTHON_BIN_PATH}" "${SCRIPT_BASENAME}" ${SCRIPT_ARGS[@]} 2>&1 \
    > "${LOG_FILE_ABS}"

  rm -f "${SCRIPT_BASENAME}"
  popd > /dev/null

  if [[ $? != 0 ]]; then
    echo "Test \"${SCRIPT_BASENAME}\" FAILED"
    return 1
  fi

  return 0
}

upsearch () {
  test / == "$PWD" && return || \
      test -e "$1" && echo "$PWD" && return || \
      cd .. && upsearch "$1"
}
