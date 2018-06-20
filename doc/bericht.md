# Bericht

## Auftrag
In unserem Projekt geht es darum, dass man im Sonnensystem von der Erde aus eine Raumsonde gezielt auf, bzw in die Umlaufbahn eines anderen Planeten(z.B. Saturn) schiessen kann. Dabei soll ein swing-by Manöver um einen dazwischenliegenden Planeten(z.B. Jupiter) vollführt werden.

## Motivation

Gewählt wurde das Thema, weil es eine Herausforderung darstellt und gleich mehrere zu lösende Probleme auf einmal enthält. Zudem sind wir eine Gruppe aus drei Personen, wodurch es möglich ist, eine Problemstellung mit grösserem Umfang zu bearbeiten. Alle Gruppenmitglieder empfinden das Thema als spannend und interessant zum Bearbeiten.  

## Ziele

- simulieren des Sonnensystems
- manuell steuerbare Raumsonde
- dynamisches swing-by Manöver

## Vorgehen

Als ersten Schritt wurde festgehalten, welche Teilschritte nötig sind. So weiss immer jeder, was es noch zu erledigen gibt und kann sich nach einem abgeschlossenen Schritt sofort dem nächsten widmen. Zu Beginn wurde das Runge-Kutta-Verfahren programmiert und gleichzeitig widmete sich jemand dem Programmieren eines Sonnensystems. Weiter wurde nach Anfangsbedingungen für das Sonnensystem gesucht. Als Schwierigkeit stellte sich dabei die Berechnung der Anfangsgeschwindigkeiten der Planete heraus. Durch Herr Kambors physikalische Untertützung konnten diese jedoch sehr genau berechnet werden. Als nächstes wurde damit begonnen ein Menu zu programmieren und das fertiggestellte Runge-Kutta-Verfahren ins main-Programm zu implementieren. Dadurch gab es auch eine funktionierende Simulation, welche jedoch nicht fehlerfrei war. Der Fehler wurde nicht gleich gefunden, doch konnte festgestellt werden, dass er irgendwo im Programmcode steckt, denn die Anfangsbedingungen wurden alle überprüft und mit den Angaben der NASA verglichen. Herausgestellt hat sich dann, dass es lediglich ein Flüchtigkeitsfehler war und in der Differenzialgleichung auf alte Positionen zugegriffen wurde. Zudem wurde das Menu implementiert, in welchem man auswählen kann, ob man die Rakete selbst steuert oder ob sie simuliert werden soll. Als weitere Funktion kann man im Menu einige wichtige Parameter festsetzen. Dies funktioniert aber noch nicht, denn trotz eingegebenen Daten ändert sich gar nichts an der Simulation. Dann wurde eine Zoom-Funktion geschrieben, mit welcher man direkt auf einen Planeten zoomen kann. Paralell dazu hat man eine Funktion geschrieben, damit man manuell bestimmen kann, wie schnell die Zeit in der Simulation vergeht. Als letzter Schritt wurde der ganz Programmcode nochmals sorgfältig überarbeitet und kommentiert

## Produkt (aktueller Stand)
### Einzelteile
- Runge Kutta
- Programm generell
  - Menu
- Zoom, timespeed, Spur

## Reflexion


## Ausblick

Der nächste Schritt in unserer Arbeit wird sein, die Raumsonde zu simulieren. Dazu wird sie der selben Klasse zugewiesen, wie die anderen Planeten auch. D.h. sie wird wie ein mini Planet behandelt. Die Raumsonde ist mit einem Vulcain 2 Triebwerk ausgestattet und sollte dann auch dementsprechend beschleunigen können. Zudem sollte die Raumsonde gesteuert werden können, indem man den Winkel, in welchem die Rakete fliegt ändern kann. Vorgesehen ist, dass als Anfangswert die Raumsonde direkt an der Erde fixiert wird. Das Wunschziel unserer Gruppe ist es, dann noch ein kleines Programm schreiben, welches direkt die energieefizienteste Route zu einem anderen Planeten berechnet und dies, wenn möglich, auch mit Hilfe eines swing-by Manövers.
