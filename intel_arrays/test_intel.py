"""Test the application"""
from unittest.mock import PropertyMock, patch
import pytest
import json
from intelarray import (discover_logical, discover_physical, get_logical,
                        get_physical)

SAS2IRCU_OUTPUT = """
LSI Corporation SAS2 IR Configuration Utility.
Version 16.00.00.00 (2013.03.01)
Copyright (c) 2009-2013 LSI Corporation. All rights reserved.

Read configuration has been initiated for controller 0
------------------------------------------------------------------------
Controller information
------------------------------------------------------------------------
  Controller type                         : SAS2308_2
  BIOS version                            : 7.39.00.00
  Firmware version                        : 20.00.02.00
  Channel description                     : 1 Serial Attached SCSI
  Initiator ID                            : 0
  Maximum physical devices                : 255
  Concurrent commands supported           : 8192
  Slot                                    : Unknown
  Segment                                 : 0
  Bus                                     : 8
  Device                                  : 0
  Function                                : 0
  RAID Support                            : Yes
------------------------------------------------------------------------
IR Volume information
------------------------------------------------------------------------
IR volume 1
  Volume ID                               : 328
  Status of volume                        : Degraded (DGD)
  Volume wwid                             : 04f9d0fa34f56e84
  RAID level                              : RAID10
  Size (in MB)                            : 1714706
  Physical hard disks                     :
  PHY[0] Enclosure#/Slot#                 : 1:0
  PHY[1] Enclosure#/Slot#                 : 1:1
  PHY[2] Enclosure#/Slot#                 : 1:2
  PHY[3] Enclosure#/Slot#                 : 0:0
------------------------------------------------------------------------
Physical device information
------------------------------------------------------------------------
Initiator at ID #0

Device is a Hard disk
  Enclosure #                             : 0
  Slot #                                  : 0
  SAS Address                             : 0000000-0-0000-0000
  State                                   : Missing (MIS)
  Manufacturer                            : SEAGATE
  Model Number                            :
  Firmware Revision                       :
  Serial No                               : 6XS1TT9M0000B229
  GUID                                    : N/A
  Protocol                                : SAS
  Drive Type                              : SAS_HDD

Device is a Hard disk
  Enclosure #                             : 1
  Slot #                                  : 0
  SAS Address                             : 5000c50-0-4815-3789
  State                                   : Optimal (OPT)
  Size (in MB)/(in sectors)               : 858483/1758174767
  Manufacturer                            : SEAGATE
  Model Number                            : ST9900805SS
  Firmware Revision                       : 0002
  Serial No                               : 6XS1TK8W0000B2289SU2
  GUID                                    : 5000c5004815378b
  Protocol                                : SAS
  Drive Type                              : SAS_HDD

Device is a Hard disk
  Enclosure #                             : 1
  Slot #                                  : 1
  SAS Address                             : 5000c50-0-4814-b2f5
  State                                   : Optimal (OPT)
  Size (in MB)/(in sectors)               : 858483/1758174767
  Manufacturer                            : SEAGATE
  Model Number                            : ST9900805SS
  Firmware Revision                       : 0002
  Serial No                               : 6XS1TK2K0000B228C31E
  GUID                                    : 5000c5004814b2f7
  Protocol                                : SAS
  Drive Type                              : SAS_HDD

Device is a Hard disk
  Enclosure #                             : 1
  Slot #                                  : 2
  SAS Address                             : 5000c50-0-4815-b13d
  State                                   : Optimal (OPT)
  Size (in MB)/(in sectors)               : 858483/1758174767
  Manufacturer                            : SEAGATE
  Model Number                            : ST9900805SS
  Firmware Revision                       : 0002
  Serial No                               : 6XS1TT6V0000B228AWSA
  GUID                                    : 5000c5004815b13f
  Protocol                                : SAS
  Drive Type                              : SAS_HDD
------------------------------------------------------------------------
Enclosure information
------------------------------------------------------------------------
  Enclosure#                              : 1
  Logical ID                              : 5001e674:5c01c000
  Numslots                                : 8
  StartSlot                               : 0
------------------------------------------------------------------------
SAS2IRCU: Command DISPLAY Completed Successfully.
SAS2IRCU: Utility Completed Successfully.
    """


@pytest.fixture
def default_output():
    return PropertyMock(return_value=SAS2IRCU_OUTPUT)


@patch('intelarray.run')
def test_discover_logical(run_mock, default_output):
    """Test method that discover logical drives (arrays)"""
    type(run_mock.return_value).stdout = default_output
    result = discover_logical()
    assert result == json.dumps({'data': [{"{#ARRAY}": "328"}]})


@patch('intelarray.run')
def test_discover_physical(run_mock, default_output):
    """Test method that discover physical drives"""
    type(run_mock.return_value).stdout = default_output
    result = discover_physical()
    assert result == json.dumps({'data': [
        {"{#ENCLOSURE}": "0", "{#SLOT}": "0"},
        {"{#ENCLOSURE}": "1", "{#SLOT}": "0"},
        {"{#ENCLOSURE}": "1", "{#SLOT}": "1"},
        {"{#ENCLOSURE}": "1", "{#SLOT}": "2"}
    ]})


@patch('intelarray.run')
def test_get_logical1(run_mock, default_output):
    """Test method that get the status of an array"""
    type(run_mock.return_value).stdout = default_output
    result = get_logical('328')
    assert result == 3


@patch('intelarray.run')
def test_get_logical2(run_mock, default_output):
    """Test method that get the status of an array"""
    type(run_mock.return_value).stdout = default_output
    result = get_logical('2')
    assert result == -1


@patch('intelarray.run')
def test_get_physical1(run_mock, default_output):
    """Test method that get the status of a disk"""
    type(run_mock.return_value).stdout = default_output
    result = get_physical(('0', '0'))
    assert result == 3


@patch('intelarray.run')
def test_get_physical2(run_mock, default_output):
    """Test method that get the status of a disk"""
    type(run_mock.return_value).stdout = default_output
    result = get_physical(('1', '2'))
    assert result == 1


@patch('intelarray.run')
def test_get_physical3(run_mock, default_output):
    """Test method that get the status of a disk"""
    type(run_mock.return_value).stdout = default_output
    result = get_physical(('1', '3'))
    assert result == -1
