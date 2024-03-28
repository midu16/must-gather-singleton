#!/usr/bin/env python

from kubernetes import client, config
from openshift_client import Result
import openshift_client as oc
import os
import tarfile
from kubernetes.client.rest import ApiException
from openshift.dynamic import DynamicClient

def get_csv_related_images_with_keyword(keyword):
    """
    Return a dictionary called matching_csvs mapping the csv.metadata.namespace:csv.metadata.name:csv.spec.relatedImages.image 
    for further usage. 

    Parameters:
        keyword (str): csv.spec.relatedImages.name keyword must-gather match
    """
    try:
        # Load Kubernetes configuration
        config.load_kube_config()

        # Create an instance of the Kubernetes API client
        kube_client = client.ApiClient()

        # Create instance of the dynamic client
        dyn_client = client.CustomObjectsApi(kube_client)

        # Fetch all CSVs
        csvs = dyn_client.list_cluster_custom_object(
            group="operators.coreos.com",
            version="v1alpha1",
            plural="clusterserviceversions"
        )

        matching_csvs = []

        # Iterate through each CSV
        for csv in csvs["items"]:
            csv_name = csv["metadata"]["name"]
            csv_namespace = csv["metadata"]["namespace"]

            # Check if CSV has related images with the keyword
            related_images = csv.get("spec", {}).get("relatedImages", [])
            for image in related_images:
                if keyword in image.get("name", ""):
                    matching_csvs.append({
                        "csv_name": csv_name,
                        "csv_namespace": csv_namespace,
                        "related_images": related_images
                    })
                    break  # Once a match is found, no need to check other related images

        return matching_csvs

    except Exception as e:
        print("Exception:", e)
        return []

def newest_file_in_current_path():
    """
    Determine the newest file in the current directory.

    Returns:
        str: Path to the newest file.
    """
    current_path = os.getcwd()
    files = os.listdir(current_path)

    if not files:
        return None

    newest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(current_path, f)))
    return os.path.join(current_path, newest_file)


def create_tar(directory_path, tarfile_name):
    """
    Create a tar file from a directory.

    Parameters:
        directory_path (str): Path to the directory to be archived.
        tarfile_name (str): Name of the tar file to be created.
    """
    try:
        with tarfile.open(tarfile_name, "w") as tar:
            tar.add(directory_path, arcname=os.path.basename(directory_path))
        print(f"Tar file '{tarfile_name}' created successfully.")
    except Exception as e:
        print(f"Error occurred while creating tar file: {e}")
        
def main():
    keyword = ["must-gather", "cluster-logging-operator", "must_gather_image", "mustgather"]
    must_gather = []
    
    for index in keyword:
        matching_csvs = get_csv_related_images_with_keyword(index)

        print(f"CSVs with related images containing keyword '{index}':")
        for csv in matching_csvs:
            # print(f"\nCSV Name: {csv['csv_name']}")
            # print(f"Namespace: {csv['csv_namespace']}")
            # print("Related Images:")
            for image in csv['related_images']:
                if index in image['name']:
                    # print(f"   {image['name']}: {image['image']}")
                    must_gather.append(f"--image={image['image']}")
                    # oc adm must-gather
                    #with oc.tls_verify(enable=False):
                    #    oc.invoke('adm', ['must-gather', '--image-stream=openshift/must-gather',f"--image={image['image']}"])
    print(set(must_gather))
    with oc.tls_verify(enable=False):
        oc.invoke('adm', ['must-gather', '--' ,'/usr/bin/gather && /usr/bin/gather_audit_logs', '--image-stream=openshift/must-gather', '--image=registry.redhat.io/openshift4/ose-local-storage-mustgather-rhel8', set(must_gather)])
    directory_path, filename = os.path.split(newest_file_in_current_path())
    create_tar(directory_path, f'{filename}.tar.gz')
    
if __name__ == "__main__":
    main()
