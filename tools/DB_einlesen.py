#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung:

    Einlesen der Werte aus der Datenbank

'''

### Standard Module ###
from os import getcwd as arbeitsverzeichnis
from os import path, chdir, sep
import pickle
### eigene Module ###

### eigene Variablen ###


class Datenbank:
    '''
     Datenbankpkl ist eine Pickledatei in der Verschieden Werte

     DB_alle sind Werte mit den Raster von ca 1h
     DB_min ist der minimal Werte jedes Tages
     DB_max ist der maximal Werte jedes Tages
     wkn_und_aktienname enthält die Aktinenamen zu den WKNs
     DB_pro_Tag ist des letzte Wert jedes Tages

     Ist ein Objekt und bestehen aus einem Dictionary für alle Werte, einem Dict für alle Minima
     und ein Dict für alle Maxima und weitere wie unten zu sehen

     DB
      |-- dict_DB_alle = {WKN1: [(Zeitstempel1, Aktiewert),(Zeitstempel2, Aktiewert),...],
      |                   WKN2: [(Zeitstempel1, Aktiewert),...}
      |-- dict_DB_min  = {WKN1: [(Zeitstempel1, Minimum),(Zeitstempel2, Minimum),...],
      |                   WKN2: [(Zeitstempel1, Minimum),...}
      |-- dict_DB_max  = {WKN1: [(Zeitstempel1, Maximum),(Zeitstempel2, Maximum),...],
      |                   WKN2: [(Zeitstempel1, Maximum),...}
      |-- wkn_und_aktienname = {'DE0005545503': '1&1 Drillisch',
      |                         'LU1250154413': 'ADO Properties', ...}
      |-- daxwerte_zuletzt_erfasst = ['SDAX_201808061800.html', 'MDAX_201808061800.html',
      |                               'TECDAX_201808061800.html'...]
      |-- einzelwerte_zuletzt_erfasst = ['Porsche-Aktie_201808061800.html',
      |                                  'airbus-Aktie_201808061800.html', ...]
      |-- dict_DB_max_sync = gleiche Länge wie dict_DB_alle und zeitlich synchronisiert
      |-- dict_DB_min_sync = gleiche Länge wie dict_DB_alle und zeitlich synchronisiert
      |-- dict_DB_pro_Tag = {WKN1: [(Zeitstempel1, Aktiewert),(Zeitstempel2, Aktiewert),...],
                             WKN2: [(Zeitstempel1, Aktiewert),...}
    '''

    def __init__(self):

        # self.dict_DB_alle = {}
        # self.dict_DB_max = {}
        # self.dict_DB_min = {}
        # self.dict_DB_max_sync = {}
        # self.dict_DB_min_sync = {}
        # self.dict_DB_wkn_und_aktienname = {}
        self.dict_DB_aktienname_zu_wkn = {}
        # self.dict_DB_pro_Tag = {}
        # self.db_zuletzt_aktualisiert = []
        self.dateiname_DB = 'Datenbank.pkl'

        self.datenbank_check()
        self.wkn_und_aktienname_drehen()


    def datenbank_check(self):
        '''
        Funktion: Es wird geprüft ob eine Datenbank im aktuellen Pfad oder im Unterverzeichnis daten
                  existiert und ggf. eingelsen
                  Falls sie nicht existiert wird eine Fehlermeldung ausgegeben.

        :return: None
        '''

        pfad = arbeitsverzeichnis()

        if path.isfile(sep.join([pfad ,"Daten", self.dateiname_DB])):
            print("Die Datenbank ist vorhanden!")
            self.pfad_mit_dateiname = pfad + "/Daten/" + self.dateiname_DB
            self.datenbank_einlesen()
        else:
            chdir("../")
            pfad = arbeitsverzeichnis()
            if path.isfile(sep.join([pfad ,"Daten", self.dateiname_DB])):
                print("Die Datenbank ist vorhanden!")
                self.pfad_mit_dateiname = sep.join([pfad, "Daten", self.dateiname_DB])
                self.datenbank_einlesen()
            else:
                print("Die Datenbank ist nicht da!")

    ### Auslesen aus der Datenbank
    def datenbank_einlesen(self):

        '''
        Funktion: Die Datenbank wird eingelesen und die Werte den Variablen zugeordnet
        :return: None
        '''

        pkl_file = open(self.pfad_mit_dateiname, 'rb')
        liste_alle_min_max = pickle.load(pkl_file)
        self.dict_DB_alle = liste_alle_min_max[0]
        self.dict_DB_min = liste_alle_min_max[1]
        self.dict_DB_max = liste_alle_min_max[2]
        self.dict_DB_wkn_und_aktienname = liste_alle_min_max[3]
        self.db_zuletzt_aktualisiert = liste_alle_min_max[4]
        self.dict_DB_max_sync = liste_alle_min_max[5]
        self.dict_DB_min_sync = liste_alle_min_max[6]
        self.dict_DB_pro_Tag = liste_alle_min_max[7]

    def wkn_und_aktienname_drehen(self):

        for wkn, name in self.dict_DB_wkn_und_aktienname.items():
            self.dict_DB_aktienname_zu_wkn.update({name: wkn})


def hauptprogramm():
    meineDB=Datenbank()
    print(meineDB.dict_DB_wkn_und_aktienname['DE000A1EWWW0'])
    print(meineDB.dict_DB_pro_Tag['DE000A1EWWW0'])
    pass


if __name__ == "__main__":
    hauptprogramm()
