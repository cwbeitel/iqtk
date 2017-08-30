package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

py_library(
    name = "framework",
    srcs = glob(
        ["__init__.py"]
    ),
    srcs_version = "PY2AND3",
    deps = [
      ':util',
      ':gcp',
      ':local',
      ':task',
      ':workflow',
      ':bq',
      ':cli'
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "cli",
    srcs = ["cli.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "bq",
    srcs = ["bq.py"],
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
    name = "gcp",
    srcs = ["gcp.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':util'
    ],
)

py_test(
    name = "gcp_test",
    srcs = ["test/gcp_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':gcp'
    ],
)

py_library(
    name = "local",
    srcs = ["local.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':gcp',
      ':util'
    ],
)

py_test(
    name = "local_test",
    srcs = ["test/local_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':local',
      ':gcp',
      ':util',
      ':workflow',
      ':task'
    ],
)

py_library(
    name = "task",
    srcs = ["task.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':gcp',
      ':local',
      ':util'
    ],
)

py_test(
    name = "task_test",
    srcs = ["test/task_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':task'
    ],
)

py_library(
    name = "workflow",
    srcs = ["workflow.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':task'
    ],
)

py_test(
    name = "workflow_test",
    size = "small",
    srcs = ["test/workflow_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':workflow'
    ],
)
