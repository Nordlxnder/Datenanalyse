#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung: Skript zum heruntelader der Datenbank aus dem Internet

    Es wird die Datenbank heruntergeladen
    Das Verzeichnis wird geprüft und der Pfad ggf. gewechselt

    Es wird auch geprüft ob die Dateischon vorhanden ist und falls ja umbenannt

    Dann wird der Download gestartet
'''

### Standard Skripte ###

import sys
from wget import download
from os import chdir, path, sep, mkdir
from os import rename


def herunterladen(pfad_av):

    # # Pfad des Arbeitsverzeichnisses setzen
    chdir(pfad_av)

    dateiname = 'Datenbank.pkl'

    pfad = verzeichnis_check(pfad_av)

    datei_check(pfad, dateiname)

    url = 'https://github.com/Nordlxnder/Daten/raw/master/Datenbank.pkl'

    pfad_mit_dateiname = sep.join([pfad, dateiname])

    download(url, pfad_mit_dateiname)

    chdir("..") # wieder ins Programmverzeichnis wechseln

    return "Die Datenbank wurde \nerfolgreich heruntergeladen \n"


def verzeichnis_check(pfad_av):

    # neuen Pfad setzen
    chdir(pfad_av)

    if not path.isdir("Daten"):
        # Ins übergeordnete Verzeichnis wechseln
        mkdir("Daten")

    # neuen Pfad festlegen
    pfad = sep.join([pfad_av, "Daten"])

    # neuen Pfad setzen
    chdir(pfad)

    return pfad


def datei_check(pfad, dateiname):
    '''
    Es wird geprüft ob die Datei datenbank.pkl schon vorhanden ist
    falls ja wird sie in datenbank_old.pkl umbenannt

    :param pfad: String
    :param dateiname: String
    :return: None
    '''

    if path.isfile(sep.join([pfad , dateiname])):
        rename(dateiname,"Datenbank_old.pkl")
        # print("Datei ist vorhanden")
    else:
        print("Die Messdatei ist nicht vorhanden")


def hauptprogramm():
    herunterladen()
    pass


if __name__ == "__main__":
    hauptprogramm()
