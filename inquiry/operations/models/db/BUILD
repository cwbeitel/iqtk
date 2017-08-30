package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

py_library(
    name = "db_models",
    srcs = glob(
        ["__init__.py"]
    ),
    srcs_version = "PY2AND3",
    deps = [
      ':alignment_pb2',
      ':mass_spec_pb2',
      ':rna_quantification_pb2',
      ':variants_pb2'
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "common_pb2",
    srcs = ["common_pb2.py"],
    srcs_version = "PY2AND3",
    deps = [
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "alignment_pb2",
    srcs = ["alignment_pb2.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':common_pb2'
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "alignment_pb2_test",
    size = "small",
    srcs = ["alignment_pb2_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':alignment_pb2',
    ],
)

py_library(
    name = "mass_spec_pb2",
    srcs = ["mass_spec_pb2.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':common_pb2'
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "mass_spec_pb2_test",
    size = "small",
    srcs = ["mass_spec_pb2_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':mass_spec_pb2',
    ],
)

py_library(
    name = "rna_quantification_pb2",
    srcs = ["rna_quantification_pb2.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':common_pb2'
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "rna_quantification_pb2_test",
    size = "small",
    srcs = ["rna_quantification_pb2_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':rna_quantification_pb2',
    ],
)

py_library(
    name = "variants_pb2",
    srcs = ["variants_pb2.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':common_pb2'
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "variants_pb2_test",
    size = "small",
    srcs = ["variants_pb2_test.py"],
    srcs_version = "PY2AND3",
    deps = [
      ':variants_pb2',
    ],
)
