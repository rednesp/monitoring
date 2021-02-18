# Monitoring Intel disk arrays

This module can be used to monitor Intel disk arrays in Zabbix using `sas2ircu` tool.

## How to use

To use this software, follow this steps:

- Install `sas2ircu` (refer to http://hwraid.le-vert.net/wiki/DebianPackages for installation instructions for Debian/Ubuntu);
- copy `intelarray.py` to your server (recommended location is `/etc/zabbix/scripts`);
- copy `intelarray.conf` to Zabbix agent configuration folder (usually `/etc/zabbix/zabbix_agentd.conf.d`) or paste its contents at the end of the
configuration file;
- restart zabbix agent;
- copy `zabbix_intel_array` to your `sudoers` configuration folder;
- in Zabbix interface, import `intel_value_maps.xml` and `intel_array_template.xml`;
- link the template `Template Intel array` to your host.

You can repeat the steps above to monitor other servers.