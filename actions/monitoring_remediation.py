import sys
sys.path.insert(1, '/opt/stackstorm/packs/service_remediations_pack/actions')
import time
from os import system

def ejecutaScript():
    with open("logs.txt", "rb") as f:
        h1 = hashlib.md5(f.read()).hexdigest()
    time.sleep(300)
    with open("logs.txt", "rb") as f:
        h2 = hashlib.md5(f.read()).hexdigest()
    if h1 == h2:
        system("st2 action execute service_remediations_pack.service_remediations_action message='NEP@L_Monitoring 1'")

while True:
    ejecutaScript()