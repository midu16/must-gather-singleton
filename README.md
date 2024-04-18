# must-gather-singleton

`must-gather-singleton` is a tool for collecting entire cluster stack data in a compact aggregated `must-gather` file.

## Container Prerequisites

The Containerfile ensures the following prerequisites installed and configured:

- Python 3.x
- Kubernetes Python client (kubernetes package)
- OpenShift Python client (openshift package)
- Proper access to the Kubernetes or OpenShift cluster

## Container Build Instructions

> podman build .


## Functionality
The script performs the following tasks:

- `Search for CSVs`: It searches for Cluster Service Versions (CSVs) in the Kubernetes or OpenShift cluster.

- `Must-Gather`: It generates a must-gather command based on the related images found and executes it.


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
