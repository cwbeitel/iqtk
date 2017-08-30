
package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

py_library(
    name = "iot",
    srcs = glob(
        ["__init__.py"]
    ),
    srcs_version = "PY2AND3",
    deps = [

    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "util",
    srcs = ["util.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "util_test",
    size = "small",
    srcs = ["test/util_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':util',
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
    name = "miseq",
    srcs = ["miseq.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':base',
      ':util',
      '//inquiry/iot/models:iot_models'
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "miseq_test",
    size = "small",
    srcs = ["test/miseq_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':miseq',
    ],
)
