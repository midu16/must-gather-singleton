#!/usr/bin/env python3
"""
This script will query the nodes of a OCP cluster and print
their status as read/not_ready
"""
# k8s_node_status.py
import argparse
import os
import sys
from kubernetes import client, config # pylint: disable=import-error

ARGS = None

def process_arguments():
  """
  Process the command line arguments
  Updates the ARGS global
  """
  global ARGS
  parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
            "--config", type = str,
            help = "Full directory path to validate",
            default = '/path/to/kubeconfig',
            required = False)
  parser.add_argument(
            "--debug", action = "store_true",
            help = "Enable Debug",
            default = 'Not enabled',
            required = False)
  ARGS = parser.parse_args()

def get_node_status( config_file="", debug = False ):
  """
  This fuction uses the passed in config file to query the OCP cluster
  for a nodes list. 
  Returns:
  ready_nodes: a list of nodes in a Ready state
  not_ready_nodes: a list of nodes in NotReady state
  """
  ready_nodes = []
  not_ready_nodes = []

  # Load kube config
  if debug:
    print(f"get_node_status called with config file {config_file}")

  config.load_kube_config(config_file=config_file)

  # Create API client
  v1 = client.CoreV1Api()

  # Get the list of nodes
  nodes = v1.list_node()

  # Iterate through nodes and check their status
  for node in nodes.items:
    for condition in node.status.conditions:
      if condition.type == 'Ready':
        if condition.status == 'True':
          ready_nodes.append(node.metadata.name)
        else:
          not_ready_nodes.append(node.metadata.name)

  if debug:
    print(f"Ready nodes: {ready_nodes}")
    print(f"Not ready nodes: {not_ready_nodes}")
    print("get_node_status finished")

  return ready_nodes, not_ready_nodes

def check_debug(debug = None):
  """
  Checks to see if the --debug parameter is passed on the command line

  Returns:
    True: If debugging is enabled
    False: If debugging is not enabled
  """
  retval = False

  #print("check_debug called")
  if debug != "Not enabled":
    retval = True
    if retval:
      print("Debug printing enabled by command line")

  if "DEBUG" in  os.environ:
    retval = True
    if retval:
      print("Debug printing enabled by environtment variable")

  return retval

def check_kube_config(check_config = "", debug = False ):
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
  if debug:
    print("check_kube_config is called")

  if "KUBECONFIG" in os.environ and os.path.isfile( os.environ["KUBECONFIG"]):
    if debug:
      print("KUBECONFIG is defined and pointing at a file")
    config_file = os.environ["KUBECONFIG"]
    retval = True
  #this parameter pointing at an invalide file wins over a valid default file
  elif "KUBECONFIG" in os.environ and not os.path.isfile(os.environ["KUBECONFIG"]):
    if debug:
      print("KUBECONFIG defined but not pointing at a file")
    retval = False
  elif os.path.isfile(check_config):
    if debug:
      print("Default kubeconfig file the command line")
    config_file = check_config
    retval = True
  elif os.path.isfile("/root/.kube/config"):
    if debug:
      print("Default kube config file found")
    config_file = "/root/.kube/config"
    retval = True
  else:
    if debug:
      print("No kube config found")

  if debug:
    print(f"check_kube_config returning: {retval} with config file: {config_file}")
  return retval, config_file

def main():
  ready_nodes = []
  not_ready_nodes = []

  # Parse command line arguments
  process_arguments()
  debug = check_debug(debug = ARGS.debug)
  retval, config_file = check_kube_config( check_config = ARGS.config, debug = debug )
  if not retval:
    print("Error finding a suitable kube config file")
    sys.exit(-1)

  ready_nodes, not_ready_nodes = get_node_status( config_file = config_file, debug = debug )

  if not ready_nodes and not not_ready_nodes:
    print("No nodes were returned")
    sys.exit(-1)

  # Print the messages
  print("Nodes in Ready state:\n" + "\n".join(ready_nodes))
  print("Nodes in NotReady state:\n" + "\n".join(not_ready_nodes))

if __name__ == '__main__':
  main()
