package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

py_library(
    name = "simple",
    srcs = glob(
        ["toolkit/simple/**/*.py"],
        exclude = [
            "toolkit/simple/**/*_test.py",
        ],
    ),
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "workflow_test",
    srcs = ["workflow_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      '//inquiry/framework',
      ':workflow'
    ],
)

py_library(
    name = "workflow",
    srcs = ["workflow.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)
