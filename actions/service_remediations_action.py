import sys
sys.path.insert(1, '/opt/stackstorm/service_remediations_pack/actions')
import os
import time
import json

from st2common.runners.base_action import Action

def send_command(remote, io_rule, service, service_data):
    remote_with_service = remote.format(service_data[service]['host'], service_data[service]['username'], service_data[service]['private_key'], '{}')
    os.system(io_rule.format('disable'))    #Disable webhook rule
    for cmd in service_data[service]['cmd']:
        os.system(remote_with_service.format(service_data[service]['cmd'][cmd]))
        time.sleep(30)
    os.system(io_rule.format('enable'))    #Enable webhook rule

class ServiceRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open("logs.txt", "a") as f:
                f.write(message + "\n")

            with open('service_data.json') as file:
                service_data = json.load(file)
            io_rule = service_data['Commands']['IO_rule']
            remote = service_data['Commands']['remote']

            service = message.split()[0]
            try:
                value = int(message[-1])
                if service in service_data and value != 0:
                    send_command(remote, io_rule, service, service_data)
            except ValueError:
                print("No tiene valor")

            return (True, "Success")

        except IOError:
            return (False, "File not accessible")