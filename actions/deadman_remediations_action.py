from time import sleep
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from functions import send_email, syslog, vm_remed

from st2common.runners.base_action import Action

class DeadmanRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
                service_data = json.load(file)
            service = message.split()[0]
            if 'deadman' in service and 'CRITICAL' in message:
                with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                    f.write("{} | {}\n".format(datetime.now().time().strftime("%H:%M:%S"), message))
                host = service.split(sep="=")[1]
                vm_status = vm_remed(service_data[host]['VM'])
                while not vm_status:
                    send_email(host)
                    syslog("[Subtype]: {}, [Host]: {}, [Error]: {}, [Remediation]: {} [Status]: {}".format("Deadman", service_data[host]['host'], message, "Send email", "succeeded"))
                    sleep(180)
                    vm_status = vm_remed(service_data[host]['VM'])
                send_email(host, True)
                syslog("[Subtype]: {}, [Host]: {}, [Error]: {}, [Remediation]: {} [Status]: {}".format("Deadman", service_data[host]['host'], message, "Reboot VM", "succeeded"))

                return (True, "Success")

            return (False, "Message doesn't match")

        except IOError:
            return (False, "File not accessible")