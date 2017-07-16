
package(default_visibility = ["//visibility:private"])

filegroup(
    name = "licenses",
    data = [
#        "@curl//:COPYING",
#        "@protobuf//:LICENSE",
#        "@six_archive//:LICENSE",
#        "@zlib_archive//:zlib.h",
    ],
)

sh_binary(
    name = "build_pip_package",
    srcs = ["build_pip_package.sh"],
    data = select({
        "//conditions:default": [
            ":licenses",
            "MANIFEST.in",
            "README",
            "setup.py",
            "//inquiry:inquiry_py",
            "//inquiry/framework",
        ],
    }),
)
