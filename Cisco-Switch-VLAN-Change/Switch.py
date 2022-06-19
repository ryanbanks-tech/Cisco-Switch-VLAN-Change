import re
from ntc_templates.parse import parse_output
from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException 

class Switch():

    def __init__(self, device_type, host, username, password, port):
        
        self.device_type = device_type
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.handle = {
            'device_type': self.device_type,
            'host': self.host,
            'username': self.username,
            'password': self.password,
            'port': self.port,
        }
        
    def get_prompt(self):
        with ConnectHandler(**self.handle) as remote_into_that:
            hash_prompt = remote_into_that.find_prompt()
            re_hash_prompt = re.findall('\W$', hash_prompt)
            if re_hash_prompt[0] == '#':
                prompt = re.sub("#", "", hash_prompt)
            elif re_hash_prompt[0] != '#':
                prompt = re_hash_prompt
            return prompt

    def show_int_switchport(self):
        with ConnectHandler(**self.handle) as remote_into_that:
            interfaces = remote_into_that.send_command('show interfaces switchport')
            int_parse = parse_output(platform = 'cisco_ios', command = 'show interfaces switchport', data = interfaces)
            return int_parse

    def send_instructions(self, instructions):
        with ConnectHandler(**self.handle) as command_thou:
            command_thee = command_thou.send_config_set(instructions)
            command_thou.save_config()
            return command_thee
