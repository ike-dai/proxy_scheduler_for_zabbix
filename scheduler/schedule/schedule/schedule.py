import json
from common.zabbix_api import ZabbixApi

class Schedule(object):

    def __init__(self, host_name, api_url, username, password):
        self.host_name = host_name
        self.api_url = api_url
        self.username = username
        self.password = password

    def attach_proxy(self, proxy_name):
        if proxy_name != '':
            api = ZabbixApi(self.api_url, self.username, self.password)
            api.user_login()
            if api.attach_host_proxy(proxy_name, self.host_name):
                print "host: %s attached to proxy: %s" % (self.host_name, proxy_name)
                return True
            else:
                return False
