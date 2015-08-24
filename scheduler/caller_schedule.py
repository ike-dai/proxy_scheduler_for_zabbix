#!/bin/env python

# Run when the Proxy schedule
#
# Usages:
#
#   caller_schedule <hostname>
#
import os.path
import sys
import argparse
import subprocess

from common.zabbix_api import ZabbixApi

def get_args():
    parser = argparse.ArgumentParser(description='Zabbix Proxy Scheduling script.')
    parser.add_argument('-r', '--rule', required=True)
    parser.add_argument('-t', '--hostname', required=True)
    parser.add_argument('-a', '--apiurl', default='http://localhost/zabbix/api_jsonrpc.php')
    parser.add_argument('-u', '--user', default='Admin')
    parser.add_argument('-p', '--password', default='zabbix')
    parser.add_argument('-f', '--file', default='rules.json')

    return parser.parse_args()

def get_class(module_name, class_name):
    module = __import__(module_name, globals(), locals(), [class_name], -1)
    return getattr(module, class_name)

def update_agent_conf(api_url, username, password, host_name, proxy_name):
    api = ZabbixApi(api_url, username, password)
    api.user_login()
    agent_ipaddress = api.get_interface_ipaddress(host_name, '1')
    proxy_ipaddress = api.get_interface_ipaddress(proxy_name, '1')

    cmd = "/bin/sh %s/action/update_agent_conf.sh %s %s" % (os.path.abspath(os.path.dirname(__file__)), agent_ipaddress, proxy_ipaddress)
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return True

if __name__ == "__main__":
    args = get_args()

# Name translate
#   Rule name: ipmi_ip
#   rule_module_name: schedule.rule.ipmi_ip_rule
#   rule_class_name: IpmiIpRule
#   schedule_module_name: schedule.schedule.ipmi_ip_schedule
#   schedule_class_name: IpmiIpSchedule

    rule_module_name = "schedule.rule." + args.rule + "_rule"
    rule_class_name = args.rule.title().replace("_", "") + "Rule"
    RuleKlass = get_class(rule_module_name, rule_class_name)
    schedule_module_name = "schedule.schedule." + args.rule + "_schedule"
    schedule_class_name = args.rule.title().replace("_", "") + "Schedule"
    ScheduleKlass = get_class(schedule_module_name, schedule_class_name)

    rule = RuleKlass(args.hostname, args.apiurl, args.user, args.password) 
    rule.read_definition(args.file)
    proxy_name = rule.suggest_candidate_proxy()
    schedule = ScheduleKlass(args.hostname, args.apiurl, args.user, args.password) 
    result = schedule.attach_proxy(proxy_name)

    if result:
        update_agent_conf(args.apiurl, args.user, args.password, args.hostname, proxy_name)
        print "OK"


