import sys
import os
import time

from st2common.runners.base_action import Action

class MyEchoAction(Action):
    def run(self, message, id="", idTag="", levelTag="", messageField="", durationField=""):
        try:
            
            with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                f.write(message + "\n")
            
            os.system("st2 run core.remote hosts='10.54.158.194' username='root' private_key='/home/stanley/.ssh/id_rsa' cmd='cd /opt/django-nepal-be && docker-compose stop && docker-compose up -d)
            time.sleep(30)
            os.system("st2 run core.remote hosts='10.54.158.194' username='root' private_key='/home/stanley/.ssh/id_rsa' cmd='cd /opt/django-nepal-be && systemctl stop nodeserver && systemctl start nodeserver)
            return (True, "Success")
        except IOError:
            return (False, "File not accessible")
        #os.system("st2 run core.remote hosts='10.54.158.243' username='root' password='Cordob12' cmd='cd /root ; echo $HOME")
