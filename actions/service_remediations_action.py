import os
import time
import json
from datetime import datetime

from st2common.runners.base_action import Action

class ServiceRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                f.write("{} | {}\n".format(datetime.now().time().strftime("%H:%M:%S"), message))

            with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
                service_data = json.load(file)
            io_rule = service_data['Commands']['IO_rule']["service"]
            remote = service_data['Commands']['remote']
            
            host = message.split()[0]
            service = message.split()[2]

            if int(message[-1]) != 1:
                command = "'systemctl {} restart'".format(service)
                os.system(io_rule.format('disable'))
                os.system(remote.format("'10.54.158.95'", "'root'", "'/home/stanley/.ssh/id_rsa'", command))
                time.sleep(30)
                os.system(io_rule.format('enable'))

            return (True, "Success")

        except IOError:
            return (False, "File not accessible")