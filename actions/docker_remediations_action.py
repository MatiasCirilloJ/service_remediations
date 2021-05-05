import os
import time
import json
import subprocess
from datetime import datetime

from st2common.runners.base_action import Action

def send_command(remote, io_rule, service, service_data):
    remote_with_service = remote.format(service_data[service]['host'], service_data["Commands"]['username'], service_data["Commands"]['private_key'], '{}')
    os.system(io_rule.format('disable'))    #Disable webhook rule
    for cmd in service_data[service]['cmd']:
        os.system(remote_with_service.format(service_data[service]['cmd'][cmd]))
        time.sleep(30)
    os.system(io_rule.format('enable'))    #Enable webhook rule

class DockerRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
                service_data = json.load(file)
            service = message.split()[0]
            
            if service in service_data and 'cmd' in service_data[service] and int(message[-1]) != 0:
                #ith open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                #    f.write("{} | {}\n".format(datetime.now().time().strftime("%H:%M:%S"), message))
                
                io_rule = service_data['Commands']['IO_rule']["docker"]
                remote = service_data['Commands']['remote']
                local = service_data['Commnads']['local']

                execution = subprocess.check_output("st2 execution list -n 1 -j", shell=True)
                id_execution = json.loads(execution)[0]["id"]
                
                send_command(remote, io_rule, service, service_data)

                output = subprocess.check_output("st2 execution get {}".format(id_), shell=True)
                with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                    f.write("-----------\n" + output.decode("utf-8") + "\n" + "-----------\n")
                return (True, "Success")

            return (False, "Message doesn't match")

        except IOError:
            return (False, "File not accessible")