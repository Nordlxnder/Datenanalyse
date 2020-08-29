#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung:
'''
### Standard Skripte ###

from sys import argv
from os import path, chdir, getcwd

### eigene Skripts ###
from tools.DB_einlesen import Datenbank
from tools.auswertung import aktie_suche
from tools.download_DB import herunterladen
from tools.x_y_diagramm import AktienGraph


# Programmpfad als Arbeitsverzeichnisses setzen
av = path.dirname(argv[0])

if len(av) > 0:
    chdir(av)
    pfad_av = getcwd()
else:
    pfad_av = getcwd()

meineDB = Datenbank()


def grafik(aktie):
    # aktie = 'DE000BASF111'
    # aktienname = meineDB.dict_DB_wkn_und_aktienname[aktie]
    aktienname = meineDB.dict_DB_wkn_und_aktienname[aktie]
    aktienwerte = meineDB.dict_DB_pro_Tag[aktie]
    AktienGraph(aktienname, aktienwerte, "jahr")


def most_wanted():

    datei = "most_wanted.txt"
    with open(datei, "r") as textdatei:
        inhalt = textdatei.read()

    # Namen der Zielaktien
    zielaktien = []
    aktien = inhalt.split("\n")
    [zielaktien.append(e) for e in aktien if len(e) > 0]

    # WKN der Zeilaktien ermitteln
    zielaktien_wkn = []
    for aktie in zielaktien:
        wkn = meineDB.dict_DB_aktienname_zu_wkn[aktie]
        zielaktien_wkn.append(wkn)

    return inhalt, zielaktien_wkn


def check_argumente(argumente):

    for e in argumente:
        flag = False
        if e == "help":
            print("\n\nmögliche Argumente:\n\n"
                  "\thelp\n"
                  "\tdownload   Download der aktuellen Datenbank\n"
                  "\tsuche      Suche nach Aktien in der DB die die Kriterien erfüllen\n"
                  "\tdiagramm   Zeigt die Aktien aus der most_wanted.txt Datei\n"
                  "\tliste      Zeigt die Aktien aus der Aktien die die Kriterien erfüllen nach einander\n"
                  "\nz.B.: programm.py liste oder programm.py DE000A1EWWW0\n\n")
            flag = True

        if e == "download":
            print("Die Datenbank wird heruntergeladen!\n\n Bitte warten Sie!!\n\n")
            herunterladen(pfad_av)
            flag = True

        if e == "suche":
            zielaktien = aktie_suche(meineDB.dict_DB_pro_Tag)
            print("\n\n")
            print("Aktien die das Kriterium erfüllen\n")
            for wkn in zielaktien:
                name = meineDB.dict_DB_wkn_und_aktienname[wkn]
                print(name,":\t", wkn)
            print("\n")
            print("Zum Anzeigen des Verlaufs "
                    "./programm.py DE000A2G8XX3 oder ./programm.py liste eingeben\n\n")
            flag = True

        if e == "diagramm":
            print("\nAktien aus der most Wanted Datei:\n")
            inhalt, zielaktien_wkn = most_wanted()
            print(inhalt)
            for e in zielaktien_wkn:
                grafik(e)
            flag = True

        if e == "liste":
            zielaktien = aktie_suche(meineDB.dict_DB_pro_Tag)
            for aktie in zielaktien:
                grafik(aktie)

            flag = True

        if flag == False:
            try:
                aktienname = meineDB.dict_DB_wkn_und_aktienname[e]
                aktienwerte = meineDB.dict_DB_pro_Tag[e]
                AktienGraph(aktienname, aktienwerte, "jahr")
                print(aktienname)

            except KeyError:
                print("\n")
                print("Die Nummer: ", e," ist keine WKN!!!")
                print("starte - programm.py help - für mehr Information")
                print("\n")

def hauptprogramm():

    argumente = argv[1:]
    check_argumente(argumente)


if __name__ == "__main__":
    hauptprogramm()
