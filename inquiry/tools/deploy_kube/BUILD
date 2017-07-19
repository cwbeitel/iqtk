
package(default_visibility = ["//visibility:private"])

filegroup(
  name = "configs",
  srcs = ["configs/iqtk.yaml"]
)

sh_binary(
    name = "deploy_kube",
    srcs = ["deploy_kube.sh"],
    data = [
      ":configs"
    ],
)
