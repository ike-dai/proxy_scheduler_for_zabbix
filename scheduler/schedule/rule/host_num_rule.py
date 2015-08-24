from schedule.schedule.host_num_schedule import HostNumSchedule
from schedule.rule.rule import Rule
from common.zabbix_api import ZabbixApi

class HostNumRule(Rule):
    """
    Controlled host number based Rule class
    """
    def suggest_candidate_proxy(self):
        """
        ToDo
        """
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        proxies = api.get_proxy_list()
        host_count = {}
        for i in range(len(proxies)):
            host_list = api.get_attached_host_list(proxies[i])
            host_count[proxies[i]] = len(host_list)
            print host_list
            print host_count[proxies[i]]
            print host_count
        candidate_proxy = min(host_count, key=(lambda x: host_count[x]))
        print "Proxy: %s" % candidate_proxy
        return candidate_proxy

