# must-gather-singleton

`must-gather-singleton` is a tool for collecting entire cluster stack data in a compact aggregated `must-gather` file.

## Prerequisites

Ensure that you have the following prerequisites installed and configured:

- Python 3.x
- Kubernetes Python client (kubernetes package)
- OpenShift Python client (openshift package)
- Proper access to the Kubernetes or OpenShift cluster


## Functionality
The script performs the following tasks:

- `Search for CSVs`: It searches for Cluster Service Versions (CSVs) in the Kubernetes or OpenShift cluster.

- `Must-Gather`: It generates a must-gather command based on the related images found and executes it.


## Operators 

| Operator Name              | `must-gather` image source  |
|----------------------------|---------------------------|
| cluster-logging-operator   | In operator bundle        |
| odf-operator               | In operator bundle        |
| ocs-operator               | In operator bundle        |
| lvms-operator              | In operator bundle        |
| sriov-network-operator     | [In cluster release bundle](https://github.com/openshift/must-gather) |
| ptp-operator               | 
| file-integrity-operator    |
| compliance-operator        |
| quay-operator              |
| aap-operator               |
| kernel-module-management-hub |
| kernel-module-management   |
| OpenShift                  | [In cluster release bundle](https://github.com/openshift/must-gather) |

[1] : https://docs.openshift.com/container-platform/4.14/support/gathering-cluster-data.html



## Logs inspection

The `must-gather` obtain it relies on the usage of [omc](https://github.com/gmeghnag/omc)  for resource inspection.
