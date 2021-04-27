import requests
import time
from os import system

def ejecutaScript():
    url = "http://10.54.158.207:4348/containers/json?all=l"
    res = requests.get(url)
    js = res.json() 

    for service in js:
        if str(service["Names"]) == "['/kapacitor']" and str(service["State"]) != "running":
            system("st2 action execute service_remediations_pack.service_remediations_action message='NEP@L_Monitoring 1'")
while True:
    ejecutaScript()
    time.sleep(300)