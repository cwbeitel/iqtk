PROTOBUF_VERSION="3.2.0"
protobuf_ver_flat=$(echo $PROTOBUF_VERSION | sed 's/\.//g' | sed 's/^0*//g')
local_protobuf_ver=$(protoc --version | awk '{print $2}')
local_protobuf_ver_flat=$(echo $local_protobuf_ver | sed 's/\.//g' | sed 's/^0*//g')
if [[ -z $local_protobuf_ver_flat ]]; then
  local_protobuf_ver_flat=0
fi
if (( $local_protobuf_ver_flat < $protobuf_ver_flat )); then
  set -e
  PROTOBUF_URL="https://github.com/google/protobuf/releases/download/v${PROTOBUF_VERSION}/protoc-${PROTOBUF_VERSION}-linux-x86_64.zip"
  PROTOBUF_ZIP=$(basename "${PROTOBUF_URL}")
  UNZIP_DEST="google-protobuf"

  wget -q "${PROTOBUF_URL}"
  unzip "${PROTOBUF_ZIP}" -d "${UNZIP_DEST}"
  cp "${UNZIP_DEST}/bin/protoc" /usr/local/bin/

  rm -f "${PROTOBUF_ZIP}"
  rm -rf "${UNZIP_DEST}"
fi
