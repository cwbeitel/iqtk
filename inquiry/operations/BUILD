
load("@org_pubref_rules_protobuf//python:rules.bzl", "py_proto_compile")

package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

py_proto_compile(
  name = "protos",
  protos = ["protos/alignment.proto",
            "protos/mass_spec.proto",
            "protos/rna_quantification.proto",
            "protos/variants.proto"]
)

py_library(
    name = "operations",
    srcs = glob(
        ["__init__.py"]
    ),
    srcs_version = "PY2AND3",
    deps = [
      ":protos"
    ],
    visibility = ["//visibility:public"],
)
