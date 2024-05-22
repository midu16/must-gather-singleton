# k8s_node_status.py
from kubernetes import client, config
import openshift_client as oc
import os
import sys
import argparse
import tarfile
import re

def get_node_status():
    # Load kube config
    config.load_kube_config()

    # Create API client
    v1 = client.CoreV1Api()

    # Get the list of nodes
    nodes = v1.list_node()

    ready_nodes = []
    not_ready_nodes = []

    # Iterate through nodes and check their status
    for node in nodes.items:
        for condition in node.status.conditions:
            if condition.type == 'Ready':
                if condition.status == 'True':
                    ready_nodes.append(node.metadata.name)
                else:
                    not_ready_nodes.append(node.metadata.name)

    # Create log messages
    #ready_message = "Nodes in Ready state:\n" + "\n".join(ready_nodes)
    #not_ready_message = "Nodes in NotReady state:\n" + "\n".join(not_ready_nodes)

    return ready_nodes, not_ready_nodes

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Get the status of Kubernetes nodes.")
    args = parser.parse_args()

    ready_message, not_ready_message = get_node_status()

    # Print the messages
    print("Nodes in Ready state:\n" + "\n".join(ready_nodes))
    print("Nodes in NotReady state:\n" + "\n".join(not_ready_nodes))

if __name__ == '__main__':
    main()