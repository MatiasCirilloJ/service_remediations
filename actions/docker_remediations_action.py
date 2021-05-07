import os
import subprocess
import time
import json
from scripts.syslogs import syslog
from datetime import datetime
from pytz import timezone
tz = timezone("America/Buenos_Aires")

from st2common.runners.base_action import Action

def exec(id_exec = None):
    if id_exec == None:
        execution = subprocess.check_output("st2 execution list -n 1 -j", shell=True)
        id_execution = json.loads(execution)[0]["id"]
        return id_execution
    else:
        jstatus = subprocess.check_output("st2 execution get {} --attr 'status' -j".format(id_exec), shell=True)
        status = json.loads(jstatus)["status"]
        return status

def send_command(remote, io_rule, host, message, service_data):
    remote_with_service = remote.format(service_data[host]['host'], service_data["Commands"]['username'], service_data["Commands"]['private_key'], '{}')
    os.system(io_rule.format('disable'))    #Disable webhook rule
    for cmd in service_data[host]['cmd']:
        os.system(remote_with_service.format(service_data[host]['cmd'][cmd]))
        id_exec = exec()
        time.sleep(30)
        status = exec(id_exec)
        syslog("[Host]: {}, [Error]: {}, [Remediation]: {} [Status]: {}".format(service_data[host]['host'], message, service_data[host]['cmd'][cmd], status))
    os.system(io_rule.format('enable'))    #Enable webhook rule

class DockerRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
                service_data = json.load(file)
            host = message.split()[0]

            if host in service_data and 'cmd' in service_data[host] and int(message[-1]) != 0:
                with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                    f.write("{} | {}\n".format(tz.localize(datetime.now()).strftime("%D-%H:%M:%S"), message))
                io_rule = service_data['Commands']['IO_rule']["docker"]
                remote = service_data['Commands']['remote']

                send_command(remote, io_rule, host, message, service_data)
                return (True, "Success")

            return (False, "Message doesn't match")

        except IOError:
            return (False, "File not accessible")