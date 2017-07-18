# ci_build

** Forked from the [tensorflow project](github.com/tensorflow/tensorflow), see [their LICENSE](https://github.com/tensorflow/tensorflow/blob/master/LICENSE). **

See [circle.yaml](https://github.com/iqtk/iqtk/blob/master/circle.yml) for where this is primarily used.

```bash
export BASE_BUILD_TAG=iqtk-base
export BUILD_TAG=iqtk:0.0.1

# Builds the `iqtk-base` container and within that bazel builds inquiry
# and runs all tests with local codebase (i.e. WORKSPACE dir) mounted to
# container /workspace. Produces .whl and .tar.gz python builds in
# pip_test/whl.
sh inquiry/tools/ci_build/ci_build.sh inquiry/tools/ci_build/builds/pip.sh
```

Once the python package has built and has passed tests we can pass that to the build of a leaner container that will be deployed with the `iqtk:version` tag to our container registries.

```bash
sh inquiry/tools/ci_build/builds/build_release_container.sh
```

As in `circle.yml` make sure you have gcloud and bazel tools installed and credentials for the target container repositories are available in the working environment using the appropriate variables.
