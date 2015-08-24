from schedule.schedule.agent_ip_schedule import AgentIpSchedule
from schedule.rule.rule import Rule
from common.zabbix_api import ZabbixApi

class AgentIpRule(Rule):
    """
    Agent IP address based Rule class
    """
    def suggest_candidate_proxy(self):
        """
        ToDo
        """
        rule_key = "agent_ip"
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        proxies = api.get_proxy_list()

        agent_ip = api.get_interface_ipaddress(self.host_name, '1')

        if self.rule_data.has_key(rule_key):
            print "error"
                        
        proxy_name = ''
        ip = agent_ip.split(".")
        for proxy_define in self.rule_data[rule_key].keys():
            flag = ''
            if proxy_name != '':
                break
            from_ip = self.rule_data[rule_key][proxy_define]["from"].split(".")
            to_ip = self.rule_data[rule_key][proxy_define]["to"].split(".")
            for i in [0, 1, 2, 3]:
                if flag == 'from' and int(from_ip[i]) < int(ip[i]):
                    proxy_name = proxy_define
                    break
                elif flag == 'from' and int(from_ip[i]) == int(ip[i]):
                    if i == 3:
                        proxy_name = proxy_define
                        break
                    else:
                        flag == 'from'
                        continue
                elif flag == 'from' and int(from_ip[i]) > int(ip[i]):
                    break
                elif flag == 'to' and int(to_ip[i]) < int(ip[i]):
                    break
                elif flag == 'to' and int(to_ip[i]) == int(ip[i]):
                    if i == 3:
                        proxy_name = proxy_define
                        break
                    else:
                        flag == 'to'
                        continue
                elif flag == 'to' and int(to_ip[i]) > int(ip[i]):
                    proxy_name = proxy_define
                    break
                elif i == 3 and int(ip[i]) == int(to_ip[i]):
                    proxy_name = proxy_define
                    break
                elif i == 3 and int(ip[i]) == int(from_ip[i]):
                    proxy_name = proxy_define
                    break
                elif int(from_ip[i]) == int(to_ip[i]) and int(to_ip[i]) == int(ip[i]):
                    continue
                elif int(from_ip[i]) < int(to_ip[i]) and int(from_ip[i]) == int(ip[i]):
                    flag = 'from'
                    continue
                elif int(from_ip[i]) < int(to_ip[i]) and int(to_ip[i]) == int(ip[i]):
                    flag = 'to'
                    continue
                elif int(from_ip[i]) < int(ip[i]) and int(ip[i]) < int(to_ip[i]):
                    proxy_name = proxy_define
                    break
                else:
                    break
        print "Proxy: %s" % proxy_name
        return proxy_name


