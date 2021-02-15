#!/usr/bin/env python3
"""Module to discover HP array items and monitor them
with Zabbix"""
import json
from subprocess import run, PIPE
import sys


def run_hpssacli():
    """Run the HP application and return a list of lines"""
    process = run(["/usr/sbin/hpssacli", "ctrl", "all", "show", "config"],
                  universal_newlines=True, check=True, stdout=PIPE)
    return process.stdout.split('\n')

def discover(key):
    """Run the HP application and get the 'key' objects (logical or physical)
    drives"""
    result = []
    for line in run_hpssacli():
        position = line.find(key)
        if position > -1:
            result.append(line[position:].split()[1])
    return result

def discover_logical():
    """Discover the logical drives"""
    return json.dumps(
        {'data': [{"{#ARRAY}": value} for value in discover('logicaldrive')]}
    )

def discover_physical():
    """Discover the physical drives"""
    return json.dumps(
        {'data': [{"{#DISK}": value} for value in discover('physicaldrive')]}
    )

def get(key, num):
    """Run the application and find the status of the object"""
    for line in run_hpssacli():
        position = line.find(key)
        if position > -1:
            values = line[position:].split()
            if values[1] == num:
                if values[-1].startswith('OK'):
                    return 1
                return 0
    return -1

def get_logical(num_array):
    """Get the status of an array"""
    return get('logicaldrive', num_array)


def get_physical(num_disk):
    """Get the status of a disk"""
    return get('physicaldrive', num_disk)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(f'Missing parameter. Usage: ${sys.argv[0]} <physical or logical> [num]')
    if sys.argv[1] == 'logical':
        if len(sys.argv) > 2:
            retcode = get_logical(sys.argv[2])
        else:
            retcode = discover_logical()
    elif sys.argv[1] == 'physical':
        if len(sys.argv) > 2:
            retcode = get_physical(sys.argv[2])
        else:
            retcode = discover_physical()
    if retcode == -1:
        print('ZBX_NOTSUPPORTED')
    else:
        print(retcode)