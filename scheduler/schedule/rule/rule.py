import json

class Rule(object):

    """
    Rule class is Abstract object class.
    """

    def __init__(self, host_name, api_url, username, password):
        self.host_name = host_name
        self.rule_definition = None
        self.api_url = api_url
        self.username = username
        self.password = password
        self.rule_data = ""

    def read_definition(self, filepath):
        file = open(filepath, 'r')
        self.rule_data = json.load(file)

    def check_current_settings(self):
        pass
