package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

py_library(
    name = "toolkit",
    srcs = glob(
        ["__init__.py"]
    ),
    srcs_version = "PY2AND3",
    deps = [
      '//inquiry/toolkit/alignment:workflow',
      '//inquiry/toolkit/genotyper_gatk:workflow',
      '//inquiry/toolkit/rna_quantification:workflow',
      '//inquiry/toolkit/metabolomics:workflow'
    ],
    visibility = ["//visibility:public"],
)
