package(default_visibility = [":internal"])

licenses(["notice"])  # BSD-3

exports_files([
  "LICENSE"
])

package_group(
  name = "internal",
  packages = ["//inquiry/..."],
)

filegroup(
    name = "all_files",
    srcs = glob(
        ["**/*"],
        exclude = [
        ],
    ),
    visibility = ["//inquiry:__subpackages__"],
)

py_library(
    name = "inquiry_py",
    srcs = ["__init__.py"],
    srcs_version = "PY2AND3",
    visibility = ["//visibility:public"],
    deps = ["//inquiry/framework", "//inquiry/toolkit"],
)

filegroup(
    name = "docs_src",
    data = glob(["docs/**/*.md"]),
)
