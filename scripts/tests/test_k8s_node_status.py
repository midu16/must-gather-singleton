# tests/test_k8s_node_status.py

from unittest.mock import patch, MagicMock
import pytest
from k8s_node_status import get_node_status

@patch('k8s_node_status.client.CoreV1Api')
@patch('k8s_node_status.config.load_kube_config')
def test_get_node_status(mock_load_kube_config, mock_core_v1_api):
  # Mock the Kubernetes API response
  mock_node_1 = MagicMock()
  mock_node_1.metadata.name = 'node1'
  mock_node_1.status.conditions = [
    MagicMock(type='Ready', status='True')
  ]

  mock_node_2 = MagicMock()
  mock_node_2.metadata.name = 'node2'
  mock_node_2.status.conditions = [
    MagicMock(type='Ready', status='False')
  ]

  mock_core_v1_api.return_value.list_node.return_value.items = [mock_node_1, mock_node_2]

  # Call the function
  ready_nodes, not_ready_nodes = get_node_status()

  # Assert the results
  assert ready_nodes == ['node1']
  assert not_ready_nodes == ['node2']
