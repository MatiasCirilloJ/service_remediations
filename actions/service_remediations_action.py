import sys
import os

from st2common.runners.base_action import Action

class MyEchoAction(Action):
    def run(self, message, id="", idTag="", levelTag="", messageField="", durationField=""):
        try:
            with open("logs.txt", "a") as f:
                f.write(message)
                return (True, "Success")
        except IOError:
            return (False, "File not accessible")
        #os.system("st2 run core.remote hosts='10.54.158.243' username='root' password='Cordob12' cmd='cd /root ; echo $HOME")
