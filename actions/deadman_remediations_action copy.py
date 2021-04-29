import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from st2common.runners.base_action import Action

def send_email(host):
    with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
        service_data = json.load(file)
    data_email = service_data["Email"]

    mail_content = "El host %s se encuentra apagado." % host
    #The mail addresses and password
    sender_address = data_email['sender']
    sender_pass = data_email['sender_pass']
    receiver_address = data_email['receiver']
    cc = data_email['cc']
    rcpt = [receiver_address] + cc
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = "Remediation SS <%s>" % sender_address
    message['To'] = receiver_address
    message['CC'] = "%s\r\n" % ",".join(cc)
    message['Subject'] = data_email['subject'] #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, rcpt, text)
    session.quit()

class ServiceRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                f.write("{} | {}\n".format(datetime.now().time().strftime("%H:%M:%S"), message))

            service = message.split()[0]
            if 'deadman' in service and 'CRITICAL' in message:
                host = service.split(sep="=")[1]
                send_email(host, service_data['Email'])

            return (True, "Success")

        except IOError:
            return (False, "File not accessible")