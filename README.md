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

Valid values for OCP_VERSION are any listed below:


## Local Container Run Instructions

> podman run --rm -it --name must-gather-singleton-spoke-1 -v /path/to/target/kubeconfig:/root/.kube/config:z -v /tmp/apps/must-gather-singleton/spoke-1/:/apps/must-gather/:z IMAGE_ID

## Prebuilt Container Run Instructions

> podman run --rm -it --name must-gather-singleton-spoke-1 -v /path/to/target/kubeconfig:/root/.kube/config:z -v /tmp/apps/must-gather-singleton/spoke-1/:/apps/must-gather/:z quay.io/namespace/must-gather-singleton.x86_64:latest

Supported OCP versions:
- 4.16
- 4.15
- 4.14
- 4.13
- 4.12


## Run the container

Data inputs needed:

- Host directory for collected directory output. This will be mapped to /apps/must-gather in the container
- Kubeconfig file to access target cluster. This will be mapped to /root/.kube/config in the container

Data outputs:
- The compressed must gather data is written to the mapped host directory. 

To run the container and wait for completion

> podman run --rm -d --name must-gather-singleton-x -v /path/to/target/kubeconfig:/root/.kube/config:z -v /tmp/apps/must-gather-singleton/spoke-1/:/apps/must-gather/:z quay.io/namespace/must-gather:VERSION

To run the container and return to the command line

> podman run --rm -d --name must-gather-singleton-x -v /path/to/target/kubeconfig:/root/.kube/config:z -v /tmp/apps/must-gather-singleton/spoke-1/:/apps/must-gather/:z quay.io/namespace/must-gather:VERSION

The progress can be monitored with the podman logs command

> podman logs -f must-gather-singleton-x

To run the container based must gather script interactivly:

> podman run --rm -it --name must-gather-singleton-x -v /path/to/target/kubeconfig:/root/.kube/config:z -v /tmp/apps/must-gather-singleton/spoke-1/:/apps/must-gather/:z quay.io/namespace/must-gather:version

## Debug output.

The container supports printing extra deubg output. The interactive script supports the `--debug` command line argument. The container and script also support passing `DEBUG=""` as an environment variable. 

Example: 

> podman run --rm -it --name must-gather-singleton-x --env DEBUG="" -v /path/to/target/kubeconfig:/root/.kube/config:z -v /tmp/apps/must-gather-singleton/spoke-1/:/apps/must-gather/:z quay.io/namespace/must-gather:version


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
