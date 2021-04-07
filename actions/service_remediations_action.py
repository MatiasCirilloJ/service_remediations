import sys
import os
import time

from st2common.runners.base_action import Action

class MyEchoAction(Action):
    def run(self, message, id="", idTag="", levelTag="", messageField="", durationField=""):
        service = message.split()[0]
        value = int(message[-1])
        if service == "NEP@L_Monitoring" and value != 0:
            os.system("st2 run core.remote hosts='10.54.158.194' username='root' private_key='/home/stanley/.ssh/id_rsa' cmd='cd /opt/django-nepal-be && docker-compose stop)
            time.sleep(30)
            os.system("st2 run core.remote hosts='10.54.158.194' username='root' private_key='/home/stanley/.ssh/id_rsa' cmd='cd /opt/django-nepal-be && docker-compose up -d)
            time.sleep(30)
            os.system("st2 run core.remote hosts='10.54.158.194' username='root' private_key='/home/stanley/.ssh/id_rsa' cmd='cd /opt/django-nepal-be && systemctl stop nodeserver && systemctl start nodeserver)
        try:
            with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                f.write(message + "\n")
        except IOError:
            return (False, "File not accessible")
        
        return (True, "Success")
        #os.system("st2 run core.remote hosts='10.54.158.243' username='root' password='Cordob12' cmd='cd /root ; echo $HOME")
