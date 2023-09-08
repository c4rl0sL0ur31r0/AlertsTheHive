# AlertsTheHive
Esta es una prueba de concepto que busca integrar feeds de víctimas de grupos de ramsomware y de urlhaus droppers en casos de TheHive.
Esta prueba de concepto fue motivo de charla en la conferencia C1b3rwall y también en Intelcon 2023.
Se actualiza cada 15 minutos y crea un caso único conteniendo en el título día, mes y año para evitar duplicados.

This is a proof of concept that seeks to integrate feeds of victims of ransomware groups and urlhaus droppers in TheHive cases.
This proof of concept was talked about at the C1b3rwall conference and also at Intelcon 2023.
It is updated every 15 minutes and creates a unique case containing the day, month and year in the title to avoid duplicates.

## Configure and install
First of all install and configure your TheHive
Remember change in src/config/config.ini your TheHive url and TheHive token
make a pip install requirements.txt
launch python3 alertMonitor.py

