#!/usr/bin/env python3
"""Module to discover HP array items and monitor them
with Zabbix"""
import json
try:
    from subprocess import run, PIPE
    check_output = None  # pylint: disable=invalid-name
except ImportError:
    from subprocess import check_output, PIPE
    run = None
import sys

RAID_STATUS = {
    None: -1,
    'Failed (FLD)': 0,
    'Okay (OKY)': 1,
    'Online (ONL)': 2,
    'Degraded (DGD)': 3,
    'Missing (MIS)': 4,
    'Initializing (INIT)': 5
}

DISK_STATUS = {
    None: -1,
    'Failed (FLD)': 0,
    'Optimal (OPT)': 1,
    'Online (ONL)': 2,
    'Missing (MIS)': 3,
    'Hot Spare (HSP)': 4,
    'Ready (RDY)': 5,
    'Available (AVL)': 6,
    'Standby (SBY)': 7,
    'Out of Sync (OSY)': 8,
    'Degraded (DGD)': 9,
    'Rebuilding (RBLD)': 10
}


def run_sas2ircu():
    """Run the Intel application to get information from the raid array"""
    if run is None:
        output = check_output(["/usr/sbin/sas2ircu", "0", "display"],
                              universal_newlines=True)
    else:
        output = run(["/usr/sbin/sas2ircu", "0", "display"],
                     universal_newlines=True, check=True, stdout=PIPE).stdout
    return output.split('\n')


def discover_logical():
    """Discover the arrays"""
    arrays = []
    for line in run_sas2ircu():
        if line.find('Volume ID') > -1:
            arrays.append(line.split(': ')[1])
    return json.dumps(
        {'data': [{"{#ARRAY}": value} for value in arrays]}
    )


def discover_physical():
    """Discover the physical disks"""
    disks = []
    found = False
    for line in run_sas2ircu():
        if line.find('Device is a Hard disk') > -1:
            found = True
            continue
        if found and line.find('Enclosure #') > -1:
            enclosure = line.split(': ')[1]
            continue
        if found and line.find('Slot #') > -1:
            slot = line.split(': ')[1]
            disks.append((enclosure, slot))
            found = False
    return json.dumps(
        {'data': [{'{#ENCLOSURE}': enc, '{#SLOT}': slot}
         for enc, slot in disks]}
    )


def get_logical(num_array):
    """Get the status of an array"""
    status = None
    found = False
    for line in run_sas2ircu():
        if line.find('Volume ID') > -1:
            if line.split(': ')[1] == num_array:
                found = True
                continue
        if found and line.find('Status of volume') > -1:
            status = line.split(': ')[1]
            break
    return RAID_STATUS[status]


def get_physical(num_disk):
    """Get the status of a disk"""
    status = None
    found_enclosure = False
    found_slot = False
    for line in run_sas2ircu():
        if not found_enclosure and line.find('Enclosure #') > -1:
            if line.split(': ')[1] == num_disk[0]:
                found_enclosure = True
                continue
        if found_enclosure and line.find('Slot #') > -1:
            if line.split(': ')[1] == num_disk[1]:
                found_slot = True
            else:
                found_enclosure = False
            continue
        if found_slot and line.find('State') > -1:
            status = line.split(': ')[1]
            break
    return DISK_STATUS[status]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Missing parameter. Usage: %s'
                 '<physical or logical> [num]' % sys.argv[0])
    if sys.argv[1] == 'logical':
        if len(sys.argv) > 2:
            retcode = get_logical(sys.argv[2])
        else:
            retcode = discover_logical()
    elif sys.argv[1] == 'physical':
        if len(sys.argv) > 3:
            retcode = get_physical(sys.argv[2:4])
        else:
            retcode = discover_physical()
    if retcode == -1:
        print('ZBX_NOTSUPPORTED')
    else:
        print(retcode)
