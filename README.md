[![Stories in Ready](https://badge.waffle.io/EN152/dcp.png?label=ready&title=Ready)](https://waffle.io/EN152/dcp)
[![Build Status](https://travis-ci.org/EN152/dcp.svg?branch=master)](https://travis-ci.org/EN152/dcp)

# Disaster Communication Platform
<img src="https://raw.githubusercontent.com/EN152/dcp/master/Sprint%203/Zwischenpr%C3%A4sentation/dcp.png" width="100px" alt=""/>

## Dokumentation
Alle Funktionen und technische Hintergründe sind im [Wiki](https://github.com/EN152/dcp/wiki) beschrieben. Technische und inhaltliche (laufende) [Diskussionen](http://elias.xyz/pad/p/ppsn) finden sich im Pad. Den aktuellen Stand einzelner Funktionalitäten entnimmt man dem [Waffle-Board](https://waffle.io/EN152/dcp).


## Installation
`sudo apt-get install python3`<br />
`sudo apt-get install python3-pip`<br />
`git clone https://github.com/EN152/dcp` <br />
`pip install -r "Disaster Communication Platform/requirements.txt"`

## Einrichtung
`sh clear_database.sh`<br />
Hiermit wird eine funktionierende Datenbank mit untenstehendem Administrator angelegt und der Server direkt gestartet. <b>Vorsicht:</b> Das Skript löscht die gesamte Datenbank (falls SQLite eingestellt ist).


### Serverstart
`python3 manage.py runserver`<br />

###lokale Erreichbarkeit
[http://localhost:8000/](http://localhost:8000/)<br />

## Zugangsdaten
### superuser
Benutzername: `admin`<br />
Emailadresse: `admin@dcp.org`<br />
Passwort: `disaster2016`<br />

## Programmierpraktikum: Soziale Netzwerke
Sommersemester 2016<br />
Fachgebiet CIT<br />
Technische Universität Berlin<br />
