#!/usr/bin/python
# -*- encoding: iso-8859-1 -*-

import os
import subprocess
import socket
import time
import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
try:
    from pyVim.connect import SmartConnect, Disconnect
except:
    os.system("/opt/stackstorm/st2/bin/pip install pyvmomi")
    from pyVim.connect import SmartConnect, Disconnect

LEVEL = {
    'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
    'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}

def syslog(message, level=LEVEL['notice'],
    host='10.54.158.25', port=5000):
    """
    Send syslog TCP packet to given host and port.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host,port))
        data = '<%d> %s' % (level, message)
        sock.send(data.encode())
        sock.close()
    except:
        pass

def exec_status(id_exec = None):
    if id_exec == None:
        execution = subprocess.check_output("st2 execution list -n 1 -j", shell=True)
        id_execution = json.loads(execution)[0]["id"]
        return id_execution
    else:
        jstatus = subprocess.check_output("st2 execution get {} --attr 'status' -j".format(id_exec), shell=True)
        status = json.loads(jstatus)["status"]
        return status

def send_service_command(remote, io_rule, service, host, message, service_data):
    command = service_data["Commands"]["systemctl"].format(service)
    os.system(io_rule.format('disable'))
    os.system(remote.format(service_data[host]['host'], service_data["Commands"]['username'], service_data["Commands"]['private_key'], command))
    id_exec = exec_status()
    time.sleep(30)
    status = exec_status(id_exec)
    syslog("[Host]: {}, [Error]: {}, [Remediation]: {} [Status]: {}".format(service_data[host]['host'], message, command, status))
    if "Controller" in host:
        os.system(remote.format(service_data[host]['host'], service_data["Commands"]['username'], service_data["Commands"]['private_key'], service_data[host]['cmd']["systemctl"]))
        id_exec = exec_status()
        time.sleep(30)
        status = exec_status(id_exec)
        syslog("[Subtype]: {}, [Host]: {}, [Error]: {}, [Remediation]: {} [Status]: {}".format("Service", service_data[host]['host'], message, service_data[host]['cmd']["systemctl"], status))
    os.system(io_rule.format('enable'))

def send_docker_command(remote, io_rule, host, message, service_data):
    remote_with_service = remote.format(service_data[host]['host'], service_data["Commands"]['username'], service_data["Commands"]['private_key'], '{}')
    os.system(io_rule.format('disable'))    #Disable webhook rule
    for cmd in service_data[host]['cmd']:
        os.system(remote_with_service.format(service_data[host]['cmd'][cmd]))
        id_exec = exec_status()
        time.sleep(30)
        if "SysLog" in host:
            time.sleep(90)
        status = exec_status(id_exec)
        syslog("[Subtype]: {}, [Host]: {}, [Error]: {}, [Remediation]: {} [Status]: {}".format("Docker", service_data[host]['host'], message, service_data[host]['cmd'][cmd], status))
    os.system(io_rule.format('enable'))    #Enable webhook rule

def send_email(host, poweron=False):
    with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
        service_data = json.load(file)
    data_email = service_data["Email"]

    if poweron:
        mail_content = "El host %s se encendió." % host
    else:
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

def vm_remed(vm):
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE

    c = SmartConnect(host="10.54.153.150", user="vagrant@vsphere.local", pwd='V1w2e3r4t5$', sslContext=s)
    
    datacenter = c.content.rootFolder.childEntity
    for i in datacenter:
        if i.name == 'HYPERFLEX-INNO-ARG':
            for j in i.vmFolder.childEntity:
                if j.name == vm:
                    if j.guestHeartbeatStatus == "gray":
                        j.PowerOffVM_Task()
                        time.sleep(10)
                        j.PowerOnVM_Task()
                        return False
                    elif j.guestHeartbeatStatus == "green":
                        return True
                elif j.name == 'David_VMs':
                    for k in j.childEntity:
                        if k.name == vm:
                            if k.guestHeartbeatStatus == "gray":
                                k.PowerOffVM_Task()
                                time.sleep(10)
                                k.PowerOnVM_Task()
                                return False
                            elif k.guestHeartbeatStatus == "green":
                                return True
    Disconnect(c)