#!/usr/bin/env python

from kubernetes import client, config
from openshift_client import Result
import openshift_client as oc
from kubernetes.client.rest import ApiException
from openshift.dynamic import DynamicClient

def get_csv_related_images_with_keyword(keyword):
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

def main():
    # keyword identificator for the must-gather operator bundle image
    keyword = ["must-gather", "cluster-logging-operator", "must_gather_image"]
    must_gather = []
    
    for index in keyword:
        matching_csvs = get_csv_related_images_with_keyword(index)

        print(f"CSVs with related images containing keyword '{index}':")
        for csv in matching_csvs:
            # For debugging
            # print(f"\nCSV Name: {csv['csv_name']}")
            # print(f"Namespace: {csv['csv_namespace']}")
            # print("Related Images:")
            for image in csv['related_images']:
                if index in image['name']:
                    # print(f"   {image['name']}: {image['image']}")
                    must_gather.append(f"--image={image['image']}")
    print(set(must_gather))
    with oc.tls_verify(enable=False):
        oc.invoke('adm', ['must-gather', '--' ,'/usr/bin/gather && /usr/bin/gather_audit_logs', '--image-stream=openshift/must-gather', set(must_gather)])

if __name__ == "__main__":
    main()
