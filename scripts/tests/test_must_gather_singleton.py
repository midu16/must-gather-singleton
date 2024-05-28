# tests/test_must_gather_singleton.py

import pytest
from unittest.mock import patch
from must_gather_singleton import (
    check_kube_config,
    get_csv_related_images_with_keyword,
    get_cluster_name,
    newest_file_in_current_path,
    create_tar,
    operator_info,
    get_must_gather_url,
    check_debug,
    validate_directory_path,
)

@pytest.mark.parametrize("debug, expected", [
    (True, True),
    (False, False)
])
def test_check_debug(debug, expected):
  assert check_debug(str(debug)) == expected

@pytest.mark.parametrize("directory_path, expected", [
    ("/apps/must-gather/", "/apps/must-gather/"),
    ("/invalid/path", None)
])
@patch('must_gather_singleton.os.path.exists', side_effect=lambda x: x == "/apps/must-gather/")
def test_validate_directory_path(mock_exists, directory_path, expected):
  assert validate_directory_path(directory_path) == expected

def test_check_kube_config():
  assert check_kube_config()[0] is True

def test_get_csv_related_images_with_keyword():
  matching_csvs, _ = get_csv_related_images_with_keyword("must-gather", debug=True)
  assert isinstance(matching_csvs, list)

def test_get_cluster_name():
  assert get_cluster_name()[0] is True

def test_newest_file_in_current_path():
  assert isinstance(newest_file_in_current_path(), tuple)

@pytest.mark.parametrize("directory_path, tarfile_name", [
("/test/path", "test.tar.gz"),
("/invalid/path", "test.tar.gz")
])
@patch('must_gather_singleton.os.path.exists', side_effect=lambda x: x == "/test/path")
@patch('must_gather_singleton.tarfile.open')
def test_create_tar(mock_tarfile_open, mock_exists, directory_path, tarfile_name):
    mock_tar = mock_tarfile_open.return_value.__enter__.return_value
    retval, _ = create_tar(directory_path, tarfile_name)
    assert retval is True

def test_operator_info():
  input_string = "lvms-operator.v4.14"
  assert operator_info(input_string) == {'operator_name': 'lvms-operator',
    'operator_version': '4.14'}

def test_get_must_gather_url():
  info = {'operator_name': 'lvms-operator',
  'operator_major_version': '4', 'operator_version': '4.14'}
  assert get_must_gather_url(info) == 'registry.redhat.io/lvms4/lvms-must-gather-rhel9:v4.14'

