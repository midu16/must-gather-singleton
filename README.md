# must-gather-singleton

`must-gather-singleton` is a tool for collecting entire cluster stack data in a compact aggregated `must-gather` file.

> [!CAUTION]
> Unless specified otherwise, everything contained in this repository is unsupported by Red Hat.

## Container Prerequisites

The Containerfile ensures the following prerequisites installed and configured:

- Python 3.x
- Kubernetes Python client (kubernetes package)
- OpenShift Python client (openshift package)
- Proper access to the Kubernetes or OpenShift cluster

## Container Build Instructions

> [!NOTE]  
> podman build --build-arg OCP_VERSION=stable-4.14 .

Valid values for OCP_VERSION are any listed [HERE](https://mirror.openshift.com/pub/openshift-v4/clients/ocp/).

## Local Container Run Instructions

> podman run --rm -it --name must-gather-singleton-x -v /path/to/target/kubeconfig:/root/.kube/config:z -v /tmp/apps/must-gather-singleton/spoke-1/:/apps/must-gather/:z --pid=host --ipc=host IMAGE_ID

## Prebuilt Container Run Instructions

> podman run --rm -it --name must-gather-singleton-x -v /path/to/target/kubeconfig:/root/.kube/config:z -v /tmp/apps/must-gather-singleton/spoke-1/:/apps/must-gather/:z --pid=host --ipc=host quay.io/midu/must-gather-singleton:version

## Run the container

Data inputs needed:

- Host directory for collected directory output. This will be mapped to /apps/must-gather in the container
- Kubeconfig file to access target cluster. This will be mapped to /root/.kube/config in the container

> podman run --rm -it --name must-gather-singleton-x -v /path/to/target/kubeconfig:/root/.kube/config:z -v /tmp/apps/must-gather-singleton/spoke-1/:/apps/must-gather/:z --pid=host --ipc=host quay.io/namespace/must-gather:version

## Functionality
The script performs the following tasks:

- `Search for CSVs`: It searches for Cluster Service Versions (CSVs) in the Kubernetes or OpenShift cluster.

- `Must-Gather`: It generates a must-gather command based on the related images found and executes it.

- Bundle Output: It compresses the must-gather outputs into a tgz file in the mapped volume 


## Operators 

| Operator Name              | `must-gather` image source  |
|----------------------------|---------------------------|
| cluster-logging-operator   | In operator bundle + demo-imageset.yaml       |
| odf-operator               | In operator bundle + demo-imageset.yaml       |
| ocs-operator               | In operator bundle        |
| lvms-operator              | In operator bundle        |
| sriov-network-operator     | [In cluster release bundle](https://github.com/openshift/must-gather) |
| ptp-operator               | In operator bundle + demo-imageset.yaml       |
| file-integrity-operator    |
| compliance-operator        |
| quay-operator              |
| aap-operator               |
| kernel-module-management-hub |In operator bundle        |
| kernel-module-management   |  In operator bundle        |
| local-storage-operator     | In demo-imageset.yaml      |
| OpenShift                  | [In cluster release bundle](https://github.com/openshift/must-gather) |

[1] : https://docs.openshift.com/container-platform/4.14/support/gathering-cluster-data.html



## Logs inspection

The `must-gather` obtain it relies on the usage of [omc](https://github.com/gmeghnag/omc)  for resource inspection.
