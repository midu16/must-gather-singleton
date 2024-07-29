# Gather SOS from cluser nodes

This playbook will use the must-gather container to do the following:

- collect all node names
- per node delete any existing toolbox-root container
- per node delete pre-existing sos output files (optional)
- per node run the OCP toolbox and execute the sos command
- per node collect the generated sos output 

## Configure playbook variables

- debug: Values: true|false Effect: enable additional data print statements
- cluster_type: Values: ocp|minikube Effect: alter plays to support operating environments
- output_data_dir: Values: valid path Effect: output direction where data products are copied
- image_name: Values: valid container image Effect: container image used by the playbook
- kube_config_path: Values: valid path to cluster kubeconfig Effect: used to map into container environment
- minikube_config_path: Values: valid path to minikube configuration directory Effect: mapped into container environment
- sosreport_args: Values: list of command line arguments passed to the sos report command Effect: alters sos report command
- sosreport_case: Values: support case number (optional) Effect: added to the sos report command line

## Example execution
$ time ansible-playbook gather-sos.yaml 

PLAY [Run Podman gather node SOS] ************************************************************************************************************************************************************************************************************

TASK [Log in and get nodes] ******************************************************************************************************************************************************************************************************************
changed: [localhost]

TASK [Print node names] **********************************************************************************************************************************************************************************************************************
skipping: [localhost] => (item=worker1) 
skipping: [localhost] => (item=worker2) 
skipping: [localhost] => (item=worker3) 
skipping: [localhost]

TASK [Remove old toolbox container] **********************************************************************************************************************************************************************************************************
changed: [localhost] => (item=worker1)
changed: [localhost] => (item=worker2)
changed: [localhost] => (item=worker3)

TASK [delete old sos reports] ****************************************************************************************************************************************************************************************************************
changed: [localhost] => (item=worker1)
changed: [localhost] => (item=worker2)
changed: [localhost] => (item=worker3)

TASK [Run toolbox on host] *******************************************************************************************************************************************************************************************************************
changed: [localhost] => (item=worker1)
changed: [localhost] => (item=worker2)
changed: [localhost] => (item=worker3)

TASK [Collect sosreport names] ***************************************************************************************************************************************************************************************************************
changed: [localhost] => (item=worker1)
changed: [localhost] => (item=worker2)
changed: [localhost] => (item=worker3)

TASK [Print collect file names] **************************************************************************************************************************************************************************************************************
skipping: [localhost] => ( *** trimmed *** ) 
skipping: [localhost] => ( *** trimmed *** ) 
skipping: [localhost] => ( *** trimmed *** ) 
skipping: [localhost]

TASK [Copy sha256 files] *********************************************************************************************************************************************************************************************************************
skipping: [localhost] => ( *** trimmed *** ) 
skipping: [localhost] => ( *** trimmed *** ) 
skipping: [localhost] => ( *** trimmed *** ) 

TASK [Copy tar.xz files] *********************************************************************************************************************************************************************************************************************
skipping: [localhost] => ( *** trimmed *** ) 
skipping: [localhost] => ( *** trimmed *** ) 
skipping: [localhost] => ( *** trimmed *** ) 

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************
localhost                  : ok=7    changed=7    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0   


real	28m53.841s
user	6m26.105s
sys	0m30.592s

$ ls -rt output/sosreport* 
sosreport-worker1-NONE-2024-07-18-qhkyvss.tar.xz.sha256
sosreport-worker2-NONE-2024-07-18-lkjxksd.tar.xz.sha256
sosreport-worker3-NONE-2024-07-18-hltwigr.tar.xz.sha256
sosreport-worker1-NONE-2024-07-18-qhkyvss.tar.xz
sosreport-worker2-NONE-2024-07-18-lkjxksd.tar.xz
sosreport-worker3-NONE-2024-07-18-hltwigr.tar.xz
