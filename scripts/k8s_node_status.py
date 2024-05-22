# k8s_node_status.py

from kubernetes import client, config  # pylint: disable=import-error

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
    return ready_nodes, not_ready_nodes

def main():

    ready_nodes, not_ready_nodes = get_node_status()

    # Print the messages
    print("Nodes in Ready state:\n" + "\n".join(ready_nodes))
    print("Nodes in NotReady state:\n" + "\n".join(not_ready_nodes))

if __name__ == '__main__':
    main()
