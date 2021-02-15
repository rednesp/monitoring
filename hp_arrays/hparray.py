"""Module to discover HP array items and monitor them
with Zabbix"""
import json
from subprocess import run, PIPE
import sys


def discover(key):
    """Run the HP application and get the 'key' objects (logical or physical)
    drives"""
    process = run(["/usr/sbin/hpssacli", "ctrl", "all", "show", "config"],
                  universal_newlines=True, check=True, stdout=PIPE)
    output = process.stdout.split('\n')
    result = []
    for line in output:
        position = line.find(key)
        if position > -1:
            result.append(line[position:].split()[1])
    return result

def discover_logical():
    """Discover the logical drives"""
    return json.dumps([{"{#ARRAY}": value} for value in discover('logicaldrive')])

def discover_physical():
    """Discover the physical drives"""
    return json.dumps([{"{#DISK}": value} for value in discover('physicaldrive')])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(f'Missing parameter. Usage: ${sys.argv[0]} <physical or logical>')
    if sys.argv[1] == 'logical':
        print(discover_logical())
    elif sys.argv[1] == 'physical':
        print(discover_physical())
