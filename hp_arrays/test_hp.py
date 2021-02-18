"""Test the application"""
from unittest.mock import PropertyMock, patch
import pytest
import json
from hparray import (discover_logical, discover_physical, get_logical,
                     get_physical)

HPSSACLI_OUTPUT = """
Smart Array P410i in Slot 0 (Embedded)    (sn: 50123456789ABCDE)

   Port Name: 1I

   Port Name: 2I

   Internal Drive Cage at Port 1I, Box 1, OK

   Internal Drive Cage at Port 2I, Box 1, OK
   array A (SAS, Unused Space: 0  MB)


      logicaldrive 1 (683.5 GB, RAID 5, OK)

      physicaldrive 1I:1:5 (port 1I:box 1:bay 5, SAS, 146 GB, OK)
      physicaldrive 1I:1:6 (port 1I:box 1:bay 6, SAS, 146 GB, OK)
      physicaldrive 2I:1:1 (port 2I:box 1:bay 1, SAS, 146 GB, OK)
      physicaldrive 2I:1:2 (port 2I:box 1:bay 2, SAS, 146 GB, OK)
      physicaldrive 2I:1:3 (port 2I:box 1:bay 3, SAS, 146 GB, Failed)
      physicaldrive 2I:1:4 (port 2I:box 1:bay 4, SAS, 146 GB, OK)

   SEP (Vendor ID PMCSIERA, Model  SRC 8x6G) 250  (WWID: 50123456789ABCED)
    """


@pytest.fixture
def default_output():
    return PropertyMock(return_value=HPSSACLI_OUTPUT)


@patch('hparray.run')
def test_discover_logical(run_mock, default_output):
    """Test method that discover logical drives (arrays)"""
    type(run_mock.return_value).stdout = default_output
    result = discover_logical()
    assert result == json.dumps({'data': [{"{#ARRAY}": "1"}]})


@patch('hparray.run')
def test_discover_physical(run_mock, default_output):
    """Test method that discover physical drives"""
    type(run_mock.return_value).stdout = default_output
    result = discover_physical()
    assert result == json.dumps({'data': [
        {"{#DISK}": "1I:1:5"}, {"{#DISK}": "1I:1:6"}, {"{#DISK}": "2I:1:1"},
        {"{#DISK}": "2I:1:2"}, {"{#DISK}": "2I:1:3"}, {"{#DISK}": "2I:1:4"}
    ]})


@patch('hparray.run')
def test_get_logical1(run_mock, default_output):
    """Test method that get the status of an array"""
    type(run_mock.return_value).stdout = default_output
    result = get_logical('1')
    assert result == 1


@patch('hparray.run')
def test_get_logical2(run_mock, default_output):
    """Test method that get the status of an array"""
    type(run_mock.return_value).stdout = default_output
    result = get_logical('2')
    assert result == -1


@patch('hparray.run')
def test_get_physical1(run_mock, default_output):
    """Test method that get the status of a disk"""
    type(run_mock.return_value).stdout = default_output
    result = get_physical('1I:1:6')
    assert result == 1


@patch('hparray.run')
def test_get_physical2(run_mock, default_output):
    """Test method that get the status of a disk"""
    type(run_mock.return_value).stdout = default_output
    result = get_physical('2I:1:3')
    assert result == 0


@patch('hparray.run')
def test_get_physical3(run_mock, default_output):
    """Test method that get the status of a disk"""
    type(run_mock.return_value).stdout = default_output
    result = get_physical('2I:1:7')
    assert result == -1
