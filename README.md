Proxy Scheduler for Zabbix
====

#Overview

This is the Zabbix proxy setting controlling tool.

# How to use ?

## Requirement

- Zabbix Server/Agent/Proxy (over ver.2.0)
- Permit "EnableRemoteCommands" in the target zabbix agent conf(zabbix_agentd.conf)

e.g.)
EnableRemoteCommands=1

- Register the host for Zabbix proxy and set the agent interface.

e.g.)
Host name: proxy-01
Agent interface: 10.1.1.100

- Register the proxy at [Administration]->[DM]

e.g.)
Proxy name: proxy-01
Proxy mode: Active/Passive

  
## Execution

If Zabbix Agent(agent-01) is started and is registered by host (agent-01), please execute the caller_schedule.py python script.

e.g.)

     /user/bin/python scheduler/caller_schedule.py -r agent_ip -t agent-01 -a http://localhost/zabbix/api_jsonrpc.php -u Admin -p zabbix -f scheduler/conf/rule.json

- The following processing is performed by the command execution
1. Dirive the target proxy of the candidate from rule.json
2. Attach the proxy to the host for Zabbix Agent
3. Modify the Zabbix Agent configuration file (Server= and ServerActive=) via zabbix_get system.run command
4. Restart Zabbix Agent via zabbix_get system.run command

## Rule file

Proxy scheduler rule definition file is written by JSON format.

e.g.)

```
{
    "ipmi_ip": {
        "proxy-01": {
            "from": "10.1.1.1",
            "to": "10.1.2.20"
        },
        "proxy-02": {
            "from": "10.1.2.21",
            "to": "10.2.1.40"
        }
    },
    "agent_ip": {
        "proxy-01": {
            "from": "10.2.1.1",
            "to": "10.2.2.20"
        },
        "proxy-02": {
            "from": "10.2.2.21",
            "to": "10.2.1.40"
        }
    }
}
```


# Contact

Please send feedback to us.

Daisuke IKEDA
<dai.ikd123@gmail.com>.


#License

Proxy scheduler is released under the Apache License version2.0. The Apache License version2.0 official full text is published at this
[link](http://www.apache.org/licenses/LICENSE-2.0.html).

# Thanks

This tool is forked [Baremetal AD](https://github.com/tech-sketch/baremetal_ad)
Baremetal AD is created by TIS Inc.
Copyright 2015 TIS Inc.

