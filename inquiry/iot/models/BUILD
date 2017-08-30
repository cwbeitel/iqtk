load("@org_pubref_rules_protobuf//python:rules.bzl", "py_proto_compile")

package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

py_proto_compile(
  name = "protos",
  protos = ["miseq.proto",
            "device_config.proto"]
)

py_library(
    name = "iot_models",
    srcs = glob(
        ["__init__.py"]
    ),
    srcs_version = "PY2AND3",
    deps = [
      ':device_config_pb2',
      ':miseq_pb2'
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "device_config_pb2",
    srcs = ["device_config_pb2.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "device_config_pb2_test",
    size = "small",
    srcs = ["device_config_pb2_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':device_config_pb2',
    ],
)

py_library(
    name = "miseq_pb2",
    srcs = ["miseq_pb2.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "miseq_pb2_test",
    size = "small",
    srcs = ["miseq_pb2_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':miseq_pb2',
    ],
)

py_library(
    name = "agilent_mass_spec_pb2",
    srcs = ["agilent_mass_spec_pb2.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "agilent_mass_spec_pb2_test",
    size = "small",
    srcs = ["agilent_mass_spec_pb2_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':agilent_mass_spec_pb2',
    ],
)

py_library(
    name = "biomek_pb2",
    srcs = ["biomek_pb2.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "biomek_pb2_test",
    size = "small",
    srcs = ["biomek_pb2_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':biomek_pb2',
    ],
)
