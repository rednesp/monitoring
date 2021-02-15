"""Test the application"""
from unittest.mock import PropertyMock, patch
from io import StringIO
import json
from hparray import discover_logical, discover_physical

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
      physicaldrive 2I:1:3 (port 2I:box 1:bay 3, SAS, 146 GB, OK)
      physicaldrive 2I:1:4 (port 2I:box 1:bay 4, SAS, 146 GB, OK)

   SEP (Vendor ID PMCSIERA, Model  SRC 8x6G) 250  (WWID: 50123456789ABCED)
    """


@patch('hparray.run')
def test_discover_logical(run_mock):
    """Test method that discover logical drives (arrays)"""
    type(run_mock.return_value).stdout = PropertyMock(return_value=HPSSACLI_OUTPUT)
    result = discover_logical()
    assert result == json.dumps([{"{#ARRAY}": "1"}])

@patch('hparray.run')
def test_discover_physical(run_mock):
    """Test method that discover physical drives"""
    type(run_mock.return_value).stdout = PropertyMock(return_value=HPSSACLI_OUTPUT)
    result = discover_physical()
    assert result == json.dumps([
        {"{#DISK}": "1I:1:5"}, {"{#DISK}": "1I:1:6"}, {"{#DISK}": "2I:1:1"},
        {"{#DISK}": "2I:1:2"}, {"{#DISK}": "2I:1:3"}, {"{#DISK}": "2I:1:4"}
    ])
