package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

py_library(
    name = "genotyper_gatk",
    srcs = glob(
        ["toolkit/genotyper_gatk/**/*.py"],
        exclude = [
            "toolkit/genotyper_gatk/**/*_test.py",
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
      ':operations'
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "operations",
    srcs = ["operations.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)
