#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung:

    Ermittelt die Akien die unter eine Bestimmte Grenze gefallen sind

    und entfernt nicht gewünschte Aktien aus der Liste
'''

from numpy import array, mean, std


### Meine Skripte ###
from tools.funktionen import statistikfenster


def aktie_suche(dict_DB_pro_tag):

    zielaktien = []

    liste_wkns = tuple(dict_DB_pro_tag.keys())

    wkns_mit_werten = dict_DB_pro_tag.items()

    # Auswertung der Aktien
    zielaktien = list(map(auswertung, wkns_mit_werten))

    # Erfernt doppelte Werte wie z.B. None
    zielaktien = list(set(zielaktien))

    # Entfernen bestimmter WKNs, die Liste der WKNs wird in der Funktion definiert
    zielaktien = wkns_entfernen(zielaktien)

    return zielaktien


def auswertung(wkn_mit_werte):
    '''
            :param aktie:  wkn string(wkn='DE0005545503')
            :return: die WKN der Aktie wird in eine Liste self.zielaktien geschrieben
                    z.B.: ['DE0005439004', 'DE000A0S8488', 'DE0006083405', 'DE0006231004', 'DE000A12B8Z4']
            '''
    wkn = wkn_mit_werte[0]
    aktienwerte = wkn_mit_werte[1]

    # Falls nicht genügend Werte vorhanden sind wird die Aktie nicht bewertet
    if len(aktienwerte) > statistikfenster:
        # [die letzten 10 Werte: bis Ende,  1 = der zweite Werte]
        # [-statistikfenster:,1]
        daten = array(aktienwerte)[-statistikfenster:,1]
        # print(aktienwerte)
        # daten = array(aktienwerte)[-statistikfenster:,0]
        # print("Werte", daten)
        mittelwert = mean(daten)
        standardabweichnung = std(daten)

        # Bestimmung der unteren Grenze
        u_Grenze = mittelwert - 2 * standardabweichnung

        # aktueller Wert
        akt_wert = daten[-1]

        # Bewertung des aktuellen Aktienwertes
        if akt_wert < u_Grenze:
            return wkn


def wkns_entfernen(zielaktien):
    '''
    Es gibt Akien die aus dem Dax gefallen sind und immer wieder in der Auswertung erscheinen
    aber aber nicht benötigt werden, darum werden sie entfernt

    Es wird geschaut ob die zuentfernenden Aktien in der Liste enthalten sind und
    dann wird der Index bestimmt und aus der Liste gelöscht.
    die Liste wird im Programm oben festgelegt
    :return:  self.zielaktien (gekürzt)
    '''
    liste_entfernen_aus_zielaktien = ['DE0007251803', None]

    for wkn in liste_entfernen_aus_zielaktien:

        try:
            zielaktien.remove(wkn)

        except ValueError:
            print("Die WKN " + wkn + " ist nicht in der Liste!")

    return zielaktien


def hauptprogramm():
    pass


if __name__ == "__main__":
    hauptprogramm()
