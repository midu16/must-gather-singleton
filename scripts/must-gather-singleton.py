#!/usr/bin/env python

from kubernetes import client, config
import openshift_client as oc
import os
import sys
import argparse
import tarfile
import re

def checkKubeConfig():
    """
    Gets the value of KUBECONFIG from the environment and test
    to see if the file is accessible
    Retruns True if found

    Parameters:
        none
    """
    retval = False

    if os.path.isfile( os.environ["KUBECONFIG"]):
      #print("Kubeconfig is a file")
      retval = True

    return retval


def get_csv_related_images_with_keyword(keyword):
    """
    Return a dictionary called matching_csvs mapping the
    csv.metadata.namespace:csv.metadata.name:csv.spec.relatedImages.image
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


def get_cluster_name():
    try:
        # Load Kubernetes configuration
        config.load_kube_config()

        # Create an instance of the Kubernetes API client
        kube_client = client.CoreV1Api()

        # Get the cluster information
        cluster_info = kube_client.list_node().items[0].metadata.labels

        # Retrieve the cluster name from the labels
        cluster_name = cluster_info.get('kubernetes.io/hostname', None)
        
        if cluster_name:
            return cluster_name
        else:
            return "Cluster name not found."

    except Exception as e:
        return f"Error: {str(e)}"


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


def operator_info(input_string):
    """
    Parse the input string to extract operator name and version.

    Parameters:
        input_string (str): The input string containing operator name and version.

    Returns:
        dict: A dictionary containing operator name and version.
    """
    # Define regular expression pattern to match operator name and version
    pattern = r'(?P<operator_name>[\w-]+)\.v(?P<operator_version>\d+\.\d+\.\d+)'

    # Match the pattern in the input string
    match = re.match(pattern, input_string)

    if match:
        # Extract operator name and version from the match object
        operator_name = match.group('operator_name')
        operator_version = match.group('operator_version')

        # Construct and return a dictionary
        return {'operator_name': operator_name, 'operator_version': operator_version}
    else:
        return None


def get_must_gather_url(operator_info):
    """
    Get the registry URL based on the operator name and major version.

    Parameters:
        operator_info (dict): A dictionary containing operator name and major version.

    Returns:
        str: The registry URL corresponding to the operator name and major version and operator version as tag.
    """
    operator_mapping = {
        'lvms-operator': {
            '4.12': 'registry.redhat.io/lvms4/lvms-must-gather-rhel8',
            '4.13': 'registry.redhat.io/lvms4/lvms-must-gather-rhel8',
            '4.14': 'registry.redhat.io/lvms4/lvms-must-gather-rhel9',
            '4.15': 'registry.redhat.io/lvms4/lvms-must-gather-rhel9',
            '4.16': 'registry.redhat.io/lvms4/lvms-must-gather-rhel9'
        },
        'ptp-operator': {
            '4.14': 'registry.redhat.io/openshift4/ptp-must-gather-rhel8',
            '4.15': 'registry.redhat.io/openshift4/ptp-must-gather-rhel8',
            '4.16': 'registry.redhat.io/openshift4/ptp-must-gather-rhel8'
        },
        'cluster-logging': {
            '5.7': 'registry.redhat.io/openshift-logging/cluster-logging-rhel8-operator',
            '5.8': 'registry.redhat.io/openshift-logging/cluster-logging-rhel9-operator'
        },
        'openshift-gitops-operator': {
            '1.11': 'registry.redhat.io/openshift-gitops-1/must-gather-rhel8',
            '1.12': 'registry.redhat.io/openshift-gitops-1/must-gather-rhel8'
        },
        'local-storage-operator': {
            '4.14': 'registry.redhat.io/openshift4/ose-local-storage-mustgather-rhel8',
            '4.15': 'registry.redhat.io/openshift4/ose-local-storage-mustgather-rhel9',
            '4.16': 'registry.redhat.io/openshift4/ose-local-storage-mustgather-rhel9'
        },
        'odf-operator': {
            '4.14': 'registry.redhat.io/odf4/odf-must-gather-rhel9',
            '4.15': 'registry.redhat.io/odf4/odf-must-gather-rhel9',
            '4.16': 'registry.redhat.io/odf4/odf-must-gather-rhel9'
        }
        # Add more operators and versions as needed
    }

    operator_name = operator_info.get('operator_name', '')
    operator_major_version = operator_info.get('operator_major_version', '')
    operator_version = operator_info.get('operator_version', '')
    
    url = operator_mapping.get(operator_name, {}).get(operator_major_version, '')

    if url and operator_version:
        url += f':v{operator_version}'

    return url


def validate_directory_path():
    """
    Validating that the provided directory path exists.

    Returns:
        str: The message of path validation provided.
    """
    parser = argparse.ArgumentParser(description="Validate directory path.")
    parser.add_argument("--path", type=str, help="Full directory path to validate", default='/apps/must-gather/')
    args = parser.parse_args()

    directory_path = args.path

    if os.path.exists(directory_path):
        print(f"The provided path '{directory_path}' is valid.")
        return directory_path
    else:
        print(f"Error: The provided path '{directory_path}' does not exist.")
        return None


def invoke_must_gather(output_list, bundle_must_gather):
    """
    Invoking the must-gather command to OCP.

    Parameters:
        output_list (list): A list containing all the must-gather images provided
        as a pre-requisite in the OfflineRegistry or by quay.io.
        bundle_must_gather (list): A list containing all the must-gather images of the installed operators if available.

    Returns:
        str: The cluster must-gather collection.
    """
    if not output_list and not bundle_must_gather:
        # If both output_list and bundle_must_gather are empty, invoke with default parameters.
        # This ensures that all the available means of collections are performed.
        oc.invoke('adm', ['must-gather', '--',
                          '/usr/bin/gather && /usr/bin/gather_audit_logs',
                          '--image-stream=openshift/must-gather'])
    else:
        # Otherwise, invoke with specified output_list and bundle_must_gather
        oc.invoke('adm', ['must-gather', '--',
                          '/usr/bin/gather && /usr/bin/gather_audit_logs',
                          '--image-stream=openshift/must-gather',
                          set(output_list),
                          set(bundle_must_gather)])


def main():
    keyword = ["must-gather", "cluster-logging-operator", "must_gather_image", "mustgather", "must_gather"]
    # Initialize the
    # output_list, mirror_must_gather and bundle_must_gather variables outside of loop
    bundle_must_gather = []
    mirror_must_gather = []
    output_list = []

    if not checkKubeConfig():
      print("Kubeconfig not found")
      sys.exit(-1)

    for index in keyword:
        matching_csvs = get_csv_related_images_with_keyword(index)

        if len(matching_csvs) == 0:
            print("No CSVs were found with a matching must gather image keyword %s" %(index))
            continue

        print(f"CSVs with related images containing keyword '{index}':")
        for csv in matching_csvs:
            # print(f"\nCSV Name: {csv['csv_name']}")
            operator = operator_info(csv['csv_name'])
            # Append a new entry
            operator['operator_major_version'] = operator['operator_version'].rsplit('.', 1)[0]
            # print(operator)
            # print(operator['operator_major_version'])
            mirror_must_gather.append(get_must_gather_url(operator))
            output_list = [item for item in mirror_must_gather if item != '']
            # print(f"Namespace: {csv['csv_namespace']}")
            # print("Related Images:")
            for image in csv['related_images']:
                if index in image['name']:
                    # print(f"   {image['name']}: {image['image']}")
                    bundle_must_gather.append(f"--image={image['image']}")
    if len(output_list) == 0 or len(bundle_must_gather) == 0:
        print("No values found in one of the must gather lists")
        sys.exit(-1)
    print(f'{set(output_list)}, {set(bundle_must_gather)}')
    current_path = validate_directory_path()
    # print(current_path)
    cluster_name = get_cluster_name()
    print(cluster_name)
    with oc.tls_verify(enable=False):
        invoke_must_gather(output_list, bundle_must_gather)
    directory_path, filename = os.path.split(newest_file_in_current_path())
    create_tar(f'{directory_path}/{filename}', f'{current_path}/{filename}.tar.gz')
    

if __name__ == "__main__":
    main()
