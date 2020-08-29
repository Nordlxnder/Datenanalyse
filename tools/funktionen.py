#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung:
'''

### Standard Module ###
from numpy import mean,std

### Funktionen ###

statistikfenster=10


def zeitinterval(daten,interval="jahr"):
    """
    Nimmt alle Daten und gibt die Daten des letzten Monat oder des letzten Jares zurück
    :param daten: [(84.4, 1504888500), (85.72, 1505147820), (85.94, 1505234340),...]
    :param interval: "jahr" oder "monat"
    :return: liefert die Anzahl der letzten Werte die den Zeitbereich enthalten
    """

    if interval== "jahr":
        letzterwert=daten[-1][1]  #letzter Zeitstempel
        ein_jahr=365*24*60*60
        von =letzterwert-ein_jahr

    if interval== "monat":
        letzterwert=daten[-1][1]  #letzter Zeitstempel

        ein_monat=31*24*60*60
        von =letzterwert-ein_monat

    if interval== "max":
        von = 0

    # Filter
    daten_neu=[]
    for e in daten:
        if e[1] > von:
            daten_neu.append(e)

    return len(daten_neu)


def vorjahresmonat(daten):
    '''
    Es wird ein Vorjahresmonat bestimmt
    Referenz Zeit ist 365 bevor den aktuellen Datum
    Fenster des Vorjahresmonat ist 3 Wo. Vorgeschichte vor der Referenzzeit
     und 1. Wo. Nachgeschichte
    :return: daten_vorjahr  [(103.4, 1531501200), (103.9, 1531760400), (107.0, 1531846800),...]
    '''
    akt_wert = daten[-1][1]
    ref_wert = akt_wert - 365*24*60*60

    von = ref_wert - 30*24*60*60  # 21 Tage davor
    bis = ref_wert + 9*24*60*60   # 9 Tage danach

    # Ausschneiden der Daten für den Zeitraum
    daten_vorjahr=[]
    [daten_vorjahr.append(e) for i,e in enumerate(daten) if e[1] > von and e[1] < bis]
    return daten_vorjahr, ref_wert


def gleitender_mittelwert(daten):
    gl_mw=[]
    for i in range(0, len(daten)+1-statistikfenster):
        gl_mw.append(float('{:.2f}'.format(mean(daten[i:i+statistikfenster]))))
    return gl_mw


def gleitende_standardabweichung(daten):
    gl_std = []
    for i in range(0, len(daten)+1 - statistikfenster):
        gl_std.append(float('{:.2f}'.format(std(daten[i:i + statistikfenster]))))
    return gl_std


def x_spur_fuer_gleitendewerte(x_spur):
    ''' Die Werte der X-Spur werden gekürzt auf die Anzahl der Y-Spur
    in Abhängigkeit des Statistikfensters'''
    x_spur = x_spur[statistikfenster - 1:len(x_spur)]
    return x_spur


def hauptprogramm():
    pass


if __name__ == "__main__":
    hauptprogramm()
