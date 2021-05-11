# service_remediations
Service remediation action in StackStorm

La instalación del entorno de trabajo se hace en Docker mediante la documentacion presentada en la página de StackStorm (https://docs.stackstorm.com/install/docker.html)

1 - Una vez realizada la intalacion del entorno, se debe configurar los puertos para comunicarnos con SS. Para ello, dentro del documento docker-compose se debe agregar dentro de "ports":
- "${ST2_EXPOSE_HTTP:-0.0.0.0:80}:80"
Luego comentar (si se agrego una nueva linea) el puerto por defecto con "#"

2 - Antes de realizar configuraciones dentro de SS, debemos cambiar la clave de usuario dentro de st2-docker/files/htpasswd

3 - Entramos al entorno de SS con el comando "docker-compose exec st2actionrunner bash" y nos paramos en el directorio "/home/stanley/.ssh" para generar las claves ssh:
a) ssh-keygen -t rsa
b) ssh-copy-id -f -i /home/stanley/.ssh/id_rsa.pub host_name@host_ip  --> completa con nombre e IP de la VM con la que se quiera comunicar. Una vez finalizado salimos del SS con "exit"

4 - Entramos al entorno de SS con el comando "docker-compose exec st2client bash", iniciamos sesion con "st2 login st2admin -p 'passwrd_pto2'" y con "st2 apikey create -k -m '{"NEP@L": "Remediation"}'" generamos la API_KEY_VALUE para enviar los POST a SS.

5 - Dentro del entorno "client" y parados en "/opt/stackstorm" instalamos el packete de remediation:
-  st2 pack install https://git_user:git_passwrd@github.com/escrimaglia/Remediation.git

6 - Al instalar el paquete en SS se debe inicializar el "Monitoring remediation":
- nohup python3 /opt/stackstorm/packs/service_remediations_pack/actions/scripts/monitoring_remediation.py &
