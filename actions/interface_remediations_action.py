import re
from functions import send_interface_command, syslog
from datetime import datetime
from pytz import timezone
tz = timezone("America/Buenos_Aires")

from st2common.runners.base_action import Action

class InterfaceRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None, host="10.54.158.243"):
        try:            
            interface = message.split(',')[0].split()[4]

            if 'down' in message:
                with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                    f.write("{} | {}, {}\n".format(tz.localize(datetime.now()).strftime("%D-%H:%M:%S"), message,host))
                
                ans_stat = send_interface_command(interface, host)
                status = re.sub('\s+',' ', ans_stat.split('\n')[3]).split()[3]
                syslog("Interface", host, message, "no shut", status)

            return (False, "Message doesn't match")
        
        except IOError:
            return (False, "File not accessible")