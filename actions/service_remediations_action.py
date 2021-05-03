import os
import time
import json
from datetime import datetime

from st2common.runners.base_action import Action

def send_command(remote, io_rule, service, host, service_data):
    command = "'systemctl restart {}'".format(service)
    os.system(io_rule.format('disable'))
    os.system(remote.format(service_data[host]['host'], service_data[host]['username'], service_data[host]['private_key'], command))
    time.sleep(30)
    os.system(io_rule.format('enable'))

class ServiceRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
                service_data = json.load(file)
            io_rule = service_data['Commands']['IO_rule']["service"]
            remote = service_data['Commands']['remote']
            
            host = message.split()[0]
            service = message.split()[2]

            if host in service_data and int(message[-1]) != 1:
                with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                    f.write("{} | {}\n".format(datetime.now().time().strftime("%H:%M:%S"), message))
                send_command(remote, io_rule, service, hots, service_data)

            return (True, "Success")

        except IOError:
            return (False, "File not accessible")