package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

py_library(
    name = "services",
    srcs = glob(
        ["__init__.py"]
    ),
    srcs_version = "PY2AND3",
    deps = [
      ":api",
      ":flow",
      ":iot",
      ":run",
      ":base"
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "run",
    srcs = ["run.py"],
    srcs_version = "PY2AND3",
    deps = [
      ":api",
      ":flow",
      ":iot",
      ":base"
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "run_test",
    size = "small",
    srcs = ["test/run_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':run',
    ],
)

py_library(
    name = "base",
    srcs = ["base.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "base_test",
    size = "small",
    srcs = ["test/base_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':base',
    ],
)

py_library(
    name = "api",
    srcs = ["api.py"],
    srcs_version = "PY2AND3",
    deps = [
      ":base"
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "api_test",
    size = "small",
    srcs = ["test/api_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':api',
    ],
)

py_library(
    name = "flow",
    srcs = ["flow.py"],
    srcs_version = "PY2AND3",
    deps = [
      ":base",
      "//inquiry/toolkit"
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "flow_test",
    size = "small",
    srcs = ["test/flow_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':flow',
    ],
)

py_library(
    name = "iot",
    srcs = ["iot.py"],
    srcs_version = "PY2AND3",
    deps = [
      ":base"
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "iot_test",
    size = "small",
    srcs = ["test/iot_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':iot',
    ],
)
