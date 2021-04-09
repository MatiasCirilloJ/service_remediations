import sys
import os
import time
import json

from st2common.runners.base_action import Action

remote = "st2 run core.remote "

class ServiceRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                f.write(message + "\n")

            IO_rule = "st2 rule {} service_remediations_pack.service_remediations_rule"
            remote = "st2 run core.remote hosts={} username={} private_key={} cmd={}"
            with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
                service_data = json.load(file)

            service = message.split()[0]
            value = int(message[-1])

            remote_with_service = remote.format(service_data[service]['host'], service_data[service]['username'], service_data[service]['private_key'], '{}')
                
            if service == "NEP@L_Controller" and value != 0:
                os.system(IO_rule.format('disable'))    #Disable webhook rule
                os.system(remote_with_service.format(service_data[service]['cmd']['stop']))
                time.sleep(20)
                os.system(remote_with_service.format(service_data[service]['cmd']['up']))
                time.sleep(20)
                os.system(remote_with_service.format(service_data[service]['cmd']['systemctl']))
                os.system(IO_rule.format('enable'))    #Enable webhook rule
            elif service == "NEP@L_SysLog" and value != 0:
                os.system(IO_rule.format('disable'))    #Disable webhook rule
                os.system(remote_with_service.format(service_data[service]['cmd']['stop']))
                time.sleep(20)
                os.system(remote_with_service.format(service_data[service]['cmd']['up']))
                os.system(IO_rule.format('enable'))    #Enable webhook rule

            return (True, "Success")

        except IOError:
            return (False, "File not accessible")
        except:
            return (False)