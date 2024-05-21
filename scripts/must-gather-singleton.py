#!/usr/bin/env python3

from kubernetes import client, config
import openshift_client as oc
import os
import sys
import argparse
import tarfile
import re

args = None

def checkKubeConfig( debug = False ):
    """
    Checks to see if the kubeconfig file is available.
    The KUBECONFIG environment variable is checked then
    ~/.kube/confg
    KUBECONFIG overrides the default path
    Retruns True if found

    From the kubectl docs:
    By default, kubectl looks for a file named config in the
    $HOME/.kube directory. You can specify other kubeconfig files
    by setting the KUBECONFIG environment variable or by setting
    the --kubeconfig flag.

    Parameters:
        none
    """
    retval = False
    config_file = ""
    if debug: print("checkKubeConfig is called")

    if "KUBECONFIG" in os.environ and os.path.isfile( os.environ["KUBECONFIG"]):
        if debug: print("KUBECONFIG is defined and pointing at a file")
        config_file = os.environ["KUBECONFIG"]
        retval = True
    #this parameter pointing at an invalide file wins over a valid default file
    elif "KUBECONFIG" in os.environ and os.environ["KUBECONFIG"]:
        if debug: print("KUBECONFIG defined but not pointing at a file")
        retval = False
    elif os.path.isfile("/root/.kube/config"):
        if debug: print("Default kube config file found")
        config_file = "/root/.kube/config"
        retval = True
    else:
        if debug: print("No kube config found")

    if debug: print("checkKubeConfig returning:", retval)
    return retval, config_file


def get_csv_related_images_with_keyword(keyword = '', debug = False):
    """
    Return a dictionary called matching_csvs mapping the
    csv.metadata.namespace:csv.metadata.name:csv.spec.relatedImages.image
    for further usage. 

    Parameters:
        keyword (str): csv.spec.relatedImages.name keyword must-gather match
    """

    matching_csvs = []
    ret_str = "Ok"

    if debug: print("get_csv_related_images_with_keyword called for keyword %s" % (keyword))
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

    except Exception as e:
        if debug: print("Exception:", e)
        ret_str = e
        matching_csvs = []

    if debug: print("get_csv_related_images_with_keyword return %d items" % (len(matching_csvs)))
    return matching_csvs, ret_str

def get_cluster_name(config_file = "", debug = False):
    cluster_name = ""
    retval = True

    if debug: print("get_cluster_name called")

    try:
        # Load Kubernetes configuration
        config.load_kube_config(config_file=config_file)

        # Create an instance of the Kubernetes API client
        kube_client = client.CoreV1Api()

        # Get the cluster information
        cluster_info = kube_client.list_node().items[0].metadata.labels

        # Retrieve the cluster name from the labels
        cluster_name = cluster_info.get('kubernetes.io/hostname', None)
        
        if not cluster_name:
            retval = False

    except Exception as e:
        cluster_name = "Error: " + str(e)
        retval = False

    if debug: print("get_cluster_name returning ", retval, " and ", cluster_name )
    return retval, cluster_name

def newest_file_in_current_path( debug = False ):
    """
    Determine the newest file in the current directory.

    Returns:
        str: Path to the newest file.
    """
    if debug: print("newest_file_in_current_path called")
    current_path = os.getcwd()
    files = os.listdir(current_path)

    if not files:
        return None

    newest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(current_path, f)))
    if debug: print("newest_file_in_current_path returning path: %s, file: %s" %(current_path, newest_file))
    return current_path, newest_file


def create_tar(directory_path = "", tarfile_name = "", debug = False):
    """
    Create a tar file from a directory.

    Parameters:
        directory_path (str): Path to the directory to be archived.
        tarfile_name (str): Name of the tar file to be created.
    """
    retval = False
    message = ""
    if debug: print("create_tar called")
    try:
        with tarfile.open(tarfile_name, "w") as tar:
            tar.add(directory_path, arcname=os.path.basename(directory_path))
        print(f"Tar file '{tarfile_name}' created successfully.")
        retval = True
        message = tarfile_name
    except Exception as e:
        print(f"Error occurred while creating tar file: {e}")
        message = e

    return retval, message

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
            '4.12': 'registry.redhat.io/openshift4/ptp-must-gather-rhel8',
            '4.13': 'registry.redhat.io/openshift4/ptp-must-gather-rhel8',
            '4.14': 'registry.redhat.io/openshift4/ptp-must-gather-rhel8',
            '4.15': 'registry.redhat.io/openshift4/ptp-must-gather-rhel8',
            '4.16': 'registry.redhat.io/openshift4/ptp-must-gather-rhel8'
        },
        'cluster-logging': {
            '5.5': 'registry.redhat.io/openshift-logging/cluster-logging-rhel8-operator',
            '5.6': 'registry.redhat.io/openshift-logging/cluster-logging-rhel8-operator',
            '5.7': 'registry.redhat.io/openshift-logging/cluster-logging-rhel8-operator',
            '5.8': 'registry.redhat.io/openshift-logging/cluster-logging-rhel9-operator'
        },
        'openshift-gitops-operator': {
            '1.9': 'registry.redhat.io/openshift-gitops-1/must-gather-rhel8',
            '1.10': 'registry.redhat.io/openshift-gitops-1/must-gather-rhel8',
            '1.11': 'registry.redhat.io/openshift-gitops-1/must-gather-rhel8',
            '1.12': 'registry.redhat.io/openshift-gitops-1/must-gather-rhel8'
        },
        'local-storage-operator': {
            '4.12': 'registry.redhat.io/openshift4/ose-local-storage-mustgather-rhel8',
            '4.13': 'registry.redhat.io/openshift4/ose-local-storage-mustgather-rhel8',
            '4.14': 'registry.redhat.io/openshift4/ose-local-storage-mustgather-rhel8',
            '4.15': 'registry.redhat.io/openshift4/ose-local-storage-mustgather-rhel9',
            '4.16': 'registry.redhat.io/openshift4/ose-local-storage-mustgather-rhel9'
        },
        'odf-operator': {
            '4.12': 'registry.redhat.io/odf4/ocs-must-gather-rhel8',
            '4.13': 'registry.redhat.io/odf4/odf-must-gather-rhel9',
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

def checkDebug(debug = None):
    """
    Checks to see if the --debug parameter is passed on the command line

    Returns:
        True: If debugging is enabled
        False: If debugging is not enabled
    """
    retval = False

    #print("checkDebug called")
    if debug != "Not enabled":
        retval = True
        if retval: print("Debug printing enabled by command line")

    if "DEBUG" in  os.environ:
        retval = True
        if retval: print("Debug printing enabled by environtment variable")

    return retval

def validate_directory_path(directory_path = "", debug = False):
    """
    Validating that the provided directory path exists.

    Returns:
        str: The message of path validation provided.
    """

    retval = None

    if debug: print("validate_directory_path called")
    if os.path.exists(directory_path):
        if debug: print(f"The provided path '{directory_path}' is valid.")
        retval =  directory_path
    else:
        print(f"Error: The provided path '{directory_path}' does not exist.")

    if debug: print("validate_directory_path returning:", retval )
    return retval

def processArguments():
    """
    Process the command line arguments
    """
    args = None
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--path", type = str, help = "Full directory path to validate", default = '/apps/must-gather/', required = False)
    parser.add_argument("--debug", action = "store_true", help = "Enable Debug", default = 'Not enabled', required = False)
    args = parser.parse_args()

    return args

def invoke_must_gather(output_list = [], bundle_must_gather = [], debug = False):
    """
    Invoking the must-gather command to OCP.

    Parameters:
        output_list (list): A list containing all the must-gather images provided
        as a pre-requisite in the OfflineRegistry or by quay.io.
        bundle_must_gather (list): A list containing all the must-gather images of the installed operators if available.

    Returns:
        str: The cluster must-gather collection.
    """
    retval = True
    message = "Success"
    if debug: print("invoke_must_gather called")

    try:
        #Note: openshift_client.invoke() uses the OS installed oc command. 
        #Ref: https://github.com/openshift/openshift-client-python?tab=readme-ov-file#something-missing
        if not output_list and not bundle_must_gather:
            if debug: print("Using the OCP default must gather")
            # If both output_list and bundle_must_gather are empty, invoke with default parameters.
            # This ensures that all the available means of collections are performed.
            oc.invoke('adm', ['must-gather', '--',
                            '/usr/bin/gather && /usr/bin/gather_audit_logs',
                            '--image-stream=openshift/must-gather'])
        else:
            if debug: print("Calling found must gather")
            # Otherwise, invoke with specified output_list and bundle_must_gather
            oc.invoke('adm', ['must-gather', '--',
                            '/usr/bin/gather && /usr/bin/gather_audit_logs',
                            '--image-stream=openshift/must-gather',
                            set(output_list),
                            set(bundle_must_gather)])
    except Exception as e:
        message = e.args
        retval = False
        if debug: print(f"Error occurred while running must-gather: {message}")

    if debug: print("invoke_must_gather finished")
    return retval, message

def main():
    keyword = ["must-gather", "cluster-logging-operator", "must_gather_image", "mustgather", "must_gather"]
    # Initialize the
    # output_list, mirror_must_gather and bundle_must_gather variables outside of loop
    bundle_must_gather = []
    mirror_must_gather = []
    output_list = []
    print_debug = False

    args = processArguments()
    print_debug = checkDebug( args.debug )

    retval, config_file = checkKubeConfig( debug = print_debug )
    if not retval:
      print("Kubeconfig not found")
      sys.exit(-1)

    output_path = validate_directory_path( directory_path = args.path, debug = print_debug)
    if output_path == None:
        print("Output directory path not found.")
        sys.exit(-1)

    retval, cluster_name = get_cluster_name(config_file = config_file, debug = print_debug)
    if not retval:
        print("Could not find cluster name: %s" %(cluster_name))
        sys.exit(-1)
    if print_debug: print("Cluster name: %s" % (cluster_name))

    for index in keyword:
        matching_csvs, message = get_csv_related_images_with_keyword(keyword = index, debug = print_debug)

        if len(matching_csvs) == 0:
            if print_debug: print("No CSVs were found with a matching must gather image keyword %s" %(index))
            continue
        else:
            if print_debug: print("Returned %d CSVs for image keyword %s" %(len(matching_csvs),index))

        print(f"Found CSVs with related images containing keyword '{index}'.")
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

    if len(output_list) or len(bundle_must_gather):
        print("Image list:", " ".join(set(output_list)), " ".join(set(bundle_must_gather)))
    
    with oc.tls_verify(enable=False):
        retval, message = invoke_must_gather(output_list = output_list, bundle_must_gather = bundle_must_gather, debug = print_debug)

    if retval == False:
        print("Error collecting must-gather data: %s" % (message))
        sys.exit(-1)

    directory_path, filename = newest_file_in_current_path(debug = print_debug)

    retval, message = create_tar( directory_path = f'{directory_path}/{filename}', tarfile_name = f'{output_path}/{filename}.tar.gz', debug = print_debug)

    if retval:
        print("Successfully compressed must gather data to %s" %( message ) )
    else:
        print("Error compressing must gather data: %s" % ( message ) )
    

if __name__ == "__main__":
    main()
