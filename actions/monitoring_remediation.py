import time
from ServiceRemediationsAction import *

def ejecutaScript():
    with open("/opt/stackstorm/packs/my_echo_action/actions/logs.txt", "rb") as f:
            h1 = hashlib.md5(f.read()).hexdigest()
    time.sleep(300)
    with open("/opt/stackstorm/packs/my_echo_action/actions/logs.txt", "rb") as f:
            h2 = hashlib.md5(f.read()).hexdigest()
    if h1 == h2:
        ServiceRemediationsAction.run(message = "NEP@L_Monitoring 0")
        with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                f.write("Monitoring apagado" + "\n")

while True:
    ejecutaScript()