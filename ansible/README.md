# must-gather-singleton ansible-playbook role

How to run `must-gather-singleton` using ansible-playbook for more than 1 OpenShift Clusters at the same time?

```bash
$ ansible-playbook must-gather-singleton-playbook.yml 
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [Run Podman must-gather-singleton] ******************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************
ok: [localhost]

TASK [Ensure podman is installed] ************************************************************************************************************************************************************************************************************
ok: [localhost]

TASK [Start Podman must-gather-singleton container(s)] ***************************************************************************************************************************************************************************************
changed: [localhost] => (item={'name': 'must-gather-singleton-1', 'image': 'quay.io/midu/must-gather-singleton.x86_64:4.14', 'volume_src': '/apps/must-gather-singleton/spoke-1/', 'container_dest': '/apps/must-gather/'})
changed: [localhost] => (item={'name': 'must-gather-singleton-2', 'image': 'quay.io/midu/must-gather-singleton.x86_64:4.14', 'volume_src': '/apps/must-gather-singleton/spoke-2/', 'container_dest': '/apps/must-gather/'})
changed: [localhost] => (item={'name': 'must-gather-singleton-3', 'image': 'quay.io/midu/must-gather-singleton.x86_64:4.14', 'volume_src': '/apps/must-gather-singleton/spoke-3/', 'container_dest': '/apps/must-gather/'})

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

Once the `ansible-playbook` run its finished, the `spoke-X` directory structure will contain a `.tar.gz` file containing a `must-gather` of the Cluster:

```bash
$ tree /apps/must-gather-singleton/spoke-1/
/apps/must-gather-singleton/spoke-1/
├── kubeconfig
└── must-gather.local.8341206907120259733.tar.gz

0 directories, 2 files
```

Below we are checking the file sizes:

```bash
$ ls -lh /apps/must-gather-singleton/spoke-1/
total 1.8G
-rw-r----- 1 root root  12K Mar 30 18:25 kubeconfig
-rw-r--r-- 1 root root 1.8G Mar 30 18:31 must-gather.local.8341206907120259733.tar.gz
```
As it can be observed, the `.tar.gz` file has a considerable size collecting the entire OCP software stack logs.
