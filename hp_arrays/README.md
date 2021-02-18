# Monitoring HP disk arrays

This module can be used to monitor HP disk arrays in Zabbix using `hpssacli` tool from HP.

## How to use

To use this software, follow this steps:

- Install `hpssacli` from HP (refer to http://downloads.linux.hpe.com/SDR/project/mcp/ for installation instructions);
- copy `hparray.py` to your server (recommended location is `/etc/zabbix/scripts`);
- copy `hparray.conf` to Zabbix agent configuration folder (usually `/etc/zabbix/zabbix_agentd.conf.d`) or paste its contents at the end of the
configuration file;
- restart zabbix agent;
- copy `zabbix_hp_array` to your `sudoers` configuration folder;
- in Zabbix interface, import `disk_value_maps.xml` and `hp_array_template.xml`;
- link the template `Template HP array` to your host.

You can repeat the steps above to monitor other servers.