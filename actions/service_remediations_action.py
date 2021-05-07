import os
import subprocess
import time
import json
from scripts.syslogs import syslog
from datetime import datetime
from pytz import timezone
tz = timezone("America/Buenos_Aires")

from st2common.runners.base_action import Action

def send_command(remote, io_rule, service, host, service_data):
    command = service_data["Commands"]["systemctl"].format(service)
    os.system(io_rule.format('disable'))
    os.system(remote.format(service_data[host]['host'], service_data["Commands"]['username'], service_data["Commands"]['private_key'], command))
    time.sleep(30)
    if "Controller" in host:
        os.system(remote.format(service_data[host]['host'], service_data["Commands"]['username'], service_data["Commands"]['private_key'], service_data[host]['cmd']["systemctl"]))
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

            if host in service_data and int(message[-1]) not in (1,2):
                with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                    f.write("{} | {}\n".format(tz.localize(datetime.now()).strftime("%D-%H:%M:%S"), message))
                send_command(remote, io_rule, service, host, service_data)
                return (True, "Success")

            return (False, "Message doesn't match")
        
        except IOError:
            return (False, "File not accessible")