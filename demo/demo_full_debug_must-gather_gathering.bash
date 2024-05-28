[root@INBACRNRDL0102 acm-4.14]# podman run --rm -it --name must_gather_singleton-spoke-1 --env DEBUG="" -v /root/.kcli/clusters/hub/auth/kubeconfig:/root/.kube/config:z -v /tmp/apps/must_gather_singleton/spoke-1/:/apps/must-gather/:z quay.io/midu/must-gather-singleton:1716903584
Trying to pull quay.io/midu/must-gather-singleton:1716903584...
Getting image source signatures
Copying blob c479c64bacc4 done
Copying blob b311ed48f8e8 done
Copying blob 9d49001ad6c5 skipped: already exists
Copying blob 969a5b0faa3e done
Copying config a43e2657b1 done
Writing manifest to image destination
Debug printing enabled by environtment variable
check_kube_config is called
Default kube config file found
check_kube_config returning: True
validate_directory_path called
The provided path '/apps/must-gather/' is valid.
validate_directory_path returning: /apps/must-gather/
get_cluster_name called
get_cluster_name returning  True  and  hub-ctlplane-0.5g-deployment.lab
Cluster name: hub-ctlplane-0.5g-deployment.lab
get_csv_related_images_with_keyword called for keyword 'must-gather
get_csv_related_images_with_keyword return '1' items.
Returned 1 CSVs for image keyword must-gather
Found CSVs with related images containing keyword 'must-gather'.
get_csv_related_images_with_keyword called for keyword 'cluster-logging-operator
get_csv_related_images_with_keyword return '0' items.
No CSVs with a matching must gather image keyword cluster-logging-operator
get_csv_related_images_with_keyword called for keyword 'must_gather_image
get_csv_related_images_with_keyword return '76' items.
Returned 76 CSVs for image keyword must_gather_image
Found CSVs with related images containing keyword 'must_gather_image'.
get_csv_related_images_with_keyword called for keyword 'mustgather
get_csv_related_images_with_keyword return '0' items.
No CSVs with a matching must gather image keyword mustgather
get_csv_related_images_with_keyword called for keyword 'must_gather
get_csv_related_images_with_keyword return '77' items.
Returned 77 CSVs for image keyword must_gather
Found CSVs with related images containing keyword 'must_gather'.
Image list: --image=registry.redhat.io/lvms4/lvms-must-gather-rhel9:v4.14.5  --image=registry.redhat.io/openshift-gitops-1/must-gather-rhel8:v1.12.3 --image=registry.redhat.io/kmm/kernel-module-management-must-gather-rhel9@sha256:6a94b2a799ef7d7b0b616b4cb3ef133f04af712ff8895c9aa0bab62342aeb5de --image=registry.redhat.io/lvms4/lvms-must-gather-rhel9@sha256:03d672ebd6dec17319f2445606f8365d63e6cf81927f69ee6c72460cdf035873 --image=registry.redhat.io/openshift-gitops-1/must-gather-rhel8@sha256:cbe88ac35fb4539287859801a4843948b4d50496ff67cfd189a16c0b45bd0d65
invoke_must_gather called
Ready nodes: ['hub-ctlplane-0.5g-deployment.lab', 'hub-ctlplane-1.5g-deployment.lab', 'hub-ctlplane-2.5g-deployment.lab']
Not ready nodes: []
Calling found must gather
invoke_must_gather finished
newest_file_in_current_path called
newest_file_in_current_path returning path: '/', file: 'must-gather.local.8136091764756208842'
create_tar called
Tar file '/apps/must-gather//must-gather.local.8136091764756208842.tar.gz' created successfully.
Successfully compressed must gather data to /apps/must-gather//must-gather.local.8136091764756208842.tar.gz
[root@INBACRNRDL0102 acm-4.14]# ls -l /tmp/apps/must_gather_singleton/spoke-1/
-rw-r--r-- 1 root root 194795520 May 28 09:48 must-gather.local.8136091764756208842.tar.gz