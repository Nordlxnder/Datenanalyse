# Blutdruckmessungen

Erfassung der Messwerte einer Blutdruckmessung


Systemvoraussetzung:

	Python 3.8
	python-kivy 1.11.1-2
	matplotlib

OS: 

	Linux

Beschreibung:

	Die Software bietet eine Oberfläche zur Eingabe der Messwerte
	eines Blutdruck Messgerätes
	
	Es können mehrere Messungen eingetragen werden können
	Alle Messdaten sowie Datum, Zeit und Kommentar werden
	In der Datei messwerte.txt im Ordner Daten gespeichert

	Die Messwerte können in einem Diagramm dargestellt werden,
	wobei die Messwerte eines Tages dann als gemittelter Wert
	angezeit wird.
	
	Falls noch keine Messdaten erfasst wurden, wird beim Aufruf
	eines Diagramms ein Beispieldatensatz angezeigt
