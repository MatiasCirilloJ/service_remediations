import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from scripts.functions import send_email, syslog

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
                send_email(host)
                syslog("[Host]: {}, [Error]: {}, [Remediation]: {} [Status]: {}".format(service_data[host]['host'], message, "Send email", "succeeded"))
                return (True, "Success")

            return (False, "Message doesn't match")

        except IOError:
            return (False, "File not accessible")