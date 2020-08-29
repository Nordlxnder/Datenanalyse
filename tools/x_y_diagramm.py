#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung:
'''

### Standard Module ###
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta, datetime


### eigene Skripte ###

from tools.funktionen import gleitender_mittelwert
from tools.funktionen import gleitende_standardabweichung
from tools.funktionen import x_spur_fuer_gleitendewerte
from tools.funktionen import zeitinterval
from tools.funktionen import vorjahresmonat


###  Funktionen ###

def in_x_und_y_spur_aufteilen(daten):
    '''
    Die Liste mit tuple wird in einen Datensatz für die X-Spur und
    einen Datensatz für die Y-Spur aufgeteilt

    Zusätzlich wird die Unixzeit der X_spur in ein Datum umgewandelt
    das Datum Unixzeit=1533141360.0 wird in ein Datetime Objekt konvertiert

    :param daten: [(84.9, 1523210640), (86.0, 1523298060), (85.2, 1523379600), ...]
    :return: liste mit x und y
    '''
    x = []
    y = []
    [(x.append(date.fromtimestamp(e[0])), y.append(e[1])) for e in daten]
    return x,y


def unixzeit_zu_zeit(unixzeit):
    ''' Umrechnung der Unixzeit in das Format Jahr,Monat,Tag,Stunde,Min,Sek
                :type        Beispiel         oder   Beispiel 2
    :return: <class 'str'>   20180409202100          2018-04-09 20:21:00
    '''
    # fmt='%Y%m%d%H%M%S'
    # zeit=datetime.fromtimestamp(unixzeit).strftime(fmt)
    zeit=datetime.fromtimestamp(unixzeit)-timedelta(seconds=3600)
    # Formatierung für die Anzeige , Ausgangswert ist 2019-08-02 18:00:00
    datum=zeit.strftime("%d.%b")
    zeit = str(zeit)
    zeit = zeit[-8:-3] +"\n"+datum
    return zeit


class AktienGraph_test():

    def __init__(self, x_spur ,y_spur, zeitabschnitt="monat" ):   #aktienname, daten, zeitabschnitt):

        # Datenverarbeitung
        # self.daten = daten
        # self.x, self.y = in_x_und_y_spur_aufteilen(daten)
        if zeitabschnitt == "monat":
            # subplots(2, 1,... ) 2 Zeilen und 1 Spalte
            Abbildung, (diagramm1,diagramm2) = plt.subplots(2, 1)

            diagramm1.plot(x_spur, y_spur)
            diagramm2.plot(x_spur, y_spur)

        else:
            Abbildung, diagramm1 = plt.subplots(1, 1)
            diagramm1.plot(x_spur, y_spur)

        plt.show()


class AktienGraph():

    def __init__(self, aktienname, daten, zeitabschnitt):

        self.daten = daten
        self.zeitabschnitt = zeitabschnitt
        self.aktienname = aktienname
        
        # Datenverarbeitung
        self.datenverarbeitung()

        # Diagramm Anzeige
        self.anzeige()

        # Kennwerte
        self.kennwerte_diagramm1()

        # Ausgabe in eine PNG Datei
        self.ausgabe()

        # Um die Fehlermeldung "RuntimeWarning: More than 20 figures have been opened." zuvermeiden
        # plt.close('all')

    def datenverarbeitung(self):

        '''
        Aufbereitung der Daten für die Darstellung
        :return:
        '''
        self.x, self.y = in_x_und_y_spur_aufteilen(self.daten)

        ### Statistikwerte ###

        # gleitende Mittelwert
        self.y_gl_mw = gleitender_mittelwert(self.y)
        # gleitende Standardabweichung
        self.y_gl_std = gleitende_standardabweichung(self.y)

        # angepasste X Spur für die gleitenden Mittel und Standardwerte
        self.x_sta = x_spur_fuer_gleitendewerte(self.x)

        # obere und untere Hüllkurve gl_mw plus gl_std und gl_mw - 2 * gl_std
        self.y_gl_std_mx = [self.y_gl_mw[e] + self.y_gl_std[e] for e in range(0, len(self.y_gl_std))]
        self.y_gl_std_mn = [self.y_gl_mw[e] - 2 * self.y_gl_std[e] for e in range(0, len(self.y_gl_std))]

        # Daten für Diagramm 1 ; monat, jahr oder alles
        # Bestimmung des Index für den Startpunkt ab dem ausgeschnitten wird
        anz_der_werte = zeitinterval(self.daten, self.zeitabschnitt)

        # Ausschneiden der Daten des gewünschten Zeitraumes
        self.x = self.x[-anz_der_werte:]
        self.y = self.y[-anz_der_werte:]
        self.y_gl_mw = self.y_gl_mw[-anz_der_werte:]
        self.y_gl_std = self.y_gl_std[-anz_der_werte:]
        self.x_sta = self.x_sta[-anz_der_werte:]
        self.y_gl_std_mx = self.y_gl_std_mx[-anz_der_werte:]
        self.y_gl_std_mn = self.y_gl_std_mn[-anz_der_werte:]

        # Bestimmung der Daten des Vorjahresmonats
        if self.zeitabschnitt == "monat":
            # Daten für Diagramm 2
            daten_ausschnitt , ref_tag = vorjahresmonat(self.daten)
            self.x2, self.y2 = in_x_und_y_spur_aufteilen(daten_ausschnitt)

            # Senkrachte Linie für den Referenz Tag in der Vergangenheit
            ref_tag = date.fromtimestamp(ref_tag)
            self.x_ref = [ref_tag, ref_tag]
            self.y_ref = [0, 1000]

        # letzter Zeitwert
        self.x_spur_letzter_zeitwert = unixzeit_zu_zeit(self.daten[-1][0])

    def anzeige(self):

        abbildung = plt.figure()

        # Formatierungen

        # Position des Diagramm oder Abstand zum Rand
        plt.subplots_adjust(right=0.87, left=0.1, bottom=0.1)

        # Schriftgröße
        self.fontsize = 10

        if self.zeitabschnitt == "monat":
            #     10 Zeilen x 1 Spalte
            self.diagramm1=plt.subplot2grid((10, 1), (0, 0), rowspan=6, colspan=1)
            self.gestaltung_diagramm1()

            # Nur wenn Daten aus den Vorjahr vorhanden sind
            if len(self.x2) > 0:
                self.diagramm2=plt.subplot2grid((10, 1), (7, 0), rowspan=3, colspan=1)
                self.gestaltung_diagramm2()

        else:
            self.diagramm1 = abbildung.add_subplot(1, 1, 1)
            self.gestaltung_diagramm1()

    def gestaltung_diagramm1(self):

        diagramm=self.diagramm1

        # Kurven zu Diagramm hinzufügen und formatieren
        self.diagramm1_kurven_hinzufuegen()

        # Zoom 0.0 start und endpunkt schliessen ab,
        diagramm.margins(0.01)
        diagramm.use_sticky_edges = True

        # Überschrift
        diagramm.set_title(self.aktienname)

        # Raster
        diagramm.grid(True)
        diagramm.grid(which = 'minor', linestyle = ':', linewidth = '0.5', color = 'grey')

        ### Y Achse ###

        # Maximum und Minimum für die automatische Skalierung
        diagramm.set_ylim(min(self.y) * 0.99, max(self.y) * 1.005)

        # Label
        diagramm.set_ylabel("Wert in €", fontsize=self.fontsize)

        ### X Achse ###

        diagramm.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        diagramm.set_xlabel("Datum", fontsize = self.fontsize)
        if self.zeitabschnitt == "monat":
            # X Achsenunterteilung in Wochen und Tage
            wo = mdates.WeekdayLocator()
            tag = mdates.DayLocator()
            diagramm.xaxis.set_major_locator(wo)
            diagramm.xaxis.set_minor_locator(tag)

        if self.zeitabschnitt == "jahr":
            # X Achsenunterteilung in Wochen und Tage
            wo = mdates.WeekdayLocator()
            monat3 = mdates.MonthLocator(interval=3)
            monat = mdates.MonthLocator()
            diagramm.xaxis.set_major_locator(monat3)
            diagramm.xaxis.set_minor_locator(monat)

        if self.zeitabschnitt == "max":
            # X Achsenunterteilung in Jahr und Monat
            diagramm.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
            jahr = mdates.YearLocator()
            monat4 = mdates.MonthLocator(interval=4)
            monat = mdates.MonthLocator()
            diagramm.xaxis.set_major_locator(monat4)
            diagramm.xaxis.set_minor_locator(monat)

    def gestaltung_diagramm2(self):

        diagramm = self.diagramm2

        # Kurven zu Diagramm hinzufügen und formatieren
        self.diagramm2_kurven_hinzufuegen()

        # Überschrift
        # diagramm.set_title("Überschrift2")

        # Raster
        diagramm.grid(True)

        ### Y Spur ###

        # Maximum und Minimum für die automatische Skalierung
        diagramm.set_ylim(min(self.y2) * 0.995, max(self.y2) * 1.005)
        # diagramm.set_ylim(min(self.y2) , max(self.y2) )

        # Label
        diagramm.set_ylabel("Wert in €", fontsize=self.fontsize)

        ### X Achse ###
        diagramm.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        diagramm.set_xlabel("Datum vor einem Jahr", fontsize=self.fontsize + 2)

        # X Achsenunterteilung in Wochen für jeden Tag
        wo = mdates.WeekdayLocator()
        tag = mdates.DayLocator()
        diagramm.xaxis.set_major_locator(wo)
        diagramm.xaxis.set_minor_locator(tag)

    def diagramm1_kurven_hinzufuegen(self):
        '''
            Auswahl der Kurve die Angezeigt werden sollen und deren Formatierung

        '''
        # Linieart
        linestyles = ['-', '--', '-.', ':']

        # Datenkurve
        self.diagramm1.plot(self.x, self.y, marker="o", linewidth=1, markersize=3,
                            color="b", label='Aktienwert')

        # gleitender Mittelwert
        self.diagramm1.plot(self.x_sta, self.y_gl_mw, linewidth=0.8, linestyle=linestyles[2],
                            color="g", label='gleitender Mittelwert')

        # Standardabweichung Minimum und Maximum
        self.diagramm1.plot(self.x_sta, self.y_gl_std_mx, linewidth=0.8, linestyle=linestyles[3],
                       color="r", label='Standardabweichung')
        self.diagramm1.plot(self.x_sta, self.y_gl_std_mn, linewidth=0.8, linestyle=linestyles[3],
                       color="r")

    def diagramm2_kurven_hinzufuegen(self):
        self.diagramm2.plot(self.x2, self.y2)
        # self.diagramm2.plot(self.x_ref, self.y_ref)

        # Vertikale Linie die den Referenztag vr einem Jahr anzeigt
        self.diagramm2.axvline(x=self.x_ref[0], color="orange")

    def kennwerte_diagramm1(self):
        # Standdardabweichung MAX
        pfeil_breite = 0.08
        kopf_pfeil_breite = 0.2
        text_size = 6
        std_mx = '{:.2f}'.format(self.y_gl_std_mx[-1])

        self.diagramm1.annotate("Std-positiv\n" + std_mx, xy=(self.x[-1], self.y_gl_std_mx[-1]),
                     xytext=(1.15, 0.8), textcoords="axes fraction", arrowprops=dict(facecolor='w',
                     width=pfeil_breite, headwidth=kopf_pfeil_breite, edgecolor="r"),
                     horizontalalignment='right', verticalalignment='top', size=text_size)

        # Aktueller Wert
        akt_wert = '{:.2f}'.format(self.y[-1])
        datum = str(self.x_spur_letzter_zeitwert)

        self.diagramm1.annotate(datum + "\n" + "akt. Wert\n" + akt_wert, xy=(self.x[-1], self.y[-1]),
                     xytext=(1.15, 0.3), textcoords="axes fraction", arrowprops=dict(facecolor='black',
                     width=pfeil_breite, headwidth=kopf_pfeil_breite, edgecolor="b"),
                     horizontalalignment='right', verticalalignment='top', size=text_size)

        # Standdardabweichung MIN
        std_mn = '{:.2f}'.format(self.y_gl_std_mn[-1])
        self.diagramm1.annotate("\n\n\nStd-negativ\n" + std_mn, xy=(self.x[-1], self.y_gl_std_mn[-1]),
                                 xytext=(1.15, 0.2), textcoords="axes fraction",
                                 arrowprops=dict(facecolor='black', width=pfeil_breite,
                                                 headwidth=kopf_pfeil_breite, edgecolor="r"),
                     horizontalalignment='right', verticalalignment='top', size=text_size)

        # gleitender Mittelwert
        mittel_pro = '{:.2f}'.format(((self.y_gl_mw[-1] / self.y_gl_std_mn[-1]) - 1) * 100)
        self.diagramm1.annotate("Mittel " + str(self.y_gl_mw[-1]) + "\n\n" + "Std_n zu MW " + mittel_pro + "%",
                     xy=(self.x[-1], self.y_gl_mw[-1]), xytext=(1.15, 0.5), textcoords="axes fraction",
                     arrowprops=dict(facecolor='black', width=pfeil_breite,
                                     headwidth=kopf_pfeil_breite, edgecolor="g"),
                     horizontalalignment='right', verticalalignment='top', size=text_size)

    def ausgabe_bild(self):
        # dpi=300 1920x1440 ; dpi=200 1280x960 ; dpi=400 2560x1920
        dpi = 400
        zeitabschnitt=self.zeitabschnitt
        if zeitabschnitt == "max":
            plt.savefig("Bilder/max.png", dpi=dpi)
        if zeitabschnitt == "jahr":
            plt.savefig("Bilder/jahr.png", dpi=dpi)
        if zeitabschnitt == "monat":
            plt.savefig("Bilder/monat.png", dpi=dpi)

    def ausgabe(self):
        print("Ausgabe")

        plt.show()
        pass


def hauptprogramm():
    y_spur = [1, 23, 2, 4]
    x_spur = [1, 2, 3, 4]
    # AktienGraph(x_spur,y_spur,zeitabschnitt="monat")
    AktienGraph_test(x_spur,y_spur,zeitabschnitt="jahr")


if __name__ == "__main__":
    hauptprogramm()
