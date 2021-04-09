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

            if service in service_data:
                remote_with_service = remote.format(service_data[service]['host'], service_data[service]['username'], service_data[service]['private_key'], '{}')
                os.system(IO_rule.format('disable'))    #Disable webhook rule
                if service == "NEP@L_Controller" and value != 0:
                    with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                        f.write(remote_with_service + "\n")
                        f.write(IO_rule.format('disable') + "\n")
                        f.write(remote_with_service.format(service_data[service]['cmd']['stop']) + "\n")
                        f.write(remote_with_service.format(service_data[service]['cmd']['up']) + "\n")
                        f.write(remote_with_service.format(service_data[service]['cmd']['systemctl']) + "\n")
                        f.write(IO_rule.format('enable') + "\n")
                    time.sleep(20)
                    #os.system(remote_with_service.format(service_data[service]['cmd']['stop']))
                    #time.sleep(20)
                    #os.system(remote_with_service.format(service_data[service]['cmd']['up']))
                    #time.sleep(20)
                    #os.system(remote_with_service.format(service_data[service]['cmd']['systemctl']))
                os.system(IO_rule.format('enable'))    #Enable webhook rule
            return (True, "Success")

        except IOError:
            return (False, "File not accessible")
        except:
            return (False)