import os
import time
import json
from datetime import datetime

from st2common.runners.base_action import Action

def send_command(remote, io_rule, service, service_data):
    remote_with_service = remote.format(service_data[service]['host'], service_data[service]['username'], service_data[service]['private_key'], '{}')
    os.system(io_rule.format('disable'))    #Disable webhook rule
    for cmd in service_data[service]['cmd']:
        os.system(remote_with_service.format(service_data[service]['cmd'][cmd]))
        time.sleep(30)
    os.system(io_rule.format('enable'))    #Enable webhook rule

class DockerRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                f.write("{} | {}\n".format(datetime.now().time().strftime("%H:%M:%S"), message))

            with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
                service_data = json.load(file)
            io_rule = service_data['Commands']['IO_rule']["docker"]
            remote = service_data['Commands']['remote']

            service = message.split()[0]

            if service in service_data and int(message[-1]) != 0:
                send_command(remote, io_rule, service, service_data)

            return (True, "Success")

        except IOError:
            return (False, "File not accessible")