# operations

![**Status: Prototype**](https://img.shields.io/badge/status-prototype-red.svg)

Refactor of Apache beam-centric architecture for Fission/lowercase-serverless. The key goals are to reduce dependency complexity, simplify debugging and development, and simplify and accelerate deployment among other things.

Initially the focus is on porting over the -omics analysis workflows which focus primarily on analysis of file globs. The plan is to have a single function for each analysis tool (e.g. bwa sequence aligner) as well as for each higher-level workflow that ties these together (e.g. complex GATK genotyping workflow). Unclear yet whether it would be better to have a single master function with a different config structure for each of these or even finer granularity of functions down to each capability of each tool. Also unclear thus far whether workflows should be externally managed (a parent function running continuously to wait for child operations to complete) or whether to represent the operation graph in a context object that gets passed (and subset by) operations as they are performed - in the process triggering responder functions (or modes thereof) in place of returning to a parent caller.

### Design

Substantial work in progress...

```python
from inquiry.framework.v1 import Operation
from inquiry.operations.models.db import alignment_pb2

# TODO

# Fission functions require a main() function
def main():
    ...?

```

Issues and tentative plans:

1. Partition of functions and dependencies: Should each operation and its DB models have its own module?

2. How are dependencies outside of the function file shipped with functions when other functions are already deployed and making use of the environment that needs to be updated (i.e. in case of including proto-generated objects with those that are not)? ```fission env update --name [runtime name] --image [runtime image]```

3. How do we verify updates won't break previous deployment? An appropriate complement of tests.

4. Is it helpful to define the interface to various operations with protocol buffers? Perhaps for various reasons including initially the ability to share validation logic and have crossover between transmitted objects and those that are easily storable in a database.

### Development

Tests can be run in the following way

```bash

bazel test //inquiry/operations/...

```

### Deployment

Operations are intended to be deployed to a kubernetes cluster running fission so start by deploying a [kubernetes cluster](https://github.com/iqtk/iqtk/tree/master/inquiry/tools/deploy/scripts/deploy_kube.sh) and [ fission](https://github.com/iqtk/iqtk/tree/master/inquiry/tools/deploy/scripts/deploy_fission.sh).

Per the fission docs, a single operation can be deployed in the following way:

```bash

# TODO

```

All operations can be deployed at once with the following

```bash

# TODO

```


(TODO: Plan for how deployment can be made contingent on passing tests as well as only on which have actually had dependency changes.)


#### Acknowledgments

Licensed under a BSD-3 open source [license](https://github.com/iqtk/iqtk/blob/master/LICENSE), please see [acknowledgments of support](https://github.com/iqtk/iqtk/tree/master/inquiry/docs/support.md).
