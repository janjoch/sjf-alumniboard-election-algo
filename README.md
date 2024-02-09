# SJf Evaluation Wahl Alumni-Rat


*Algorithmus zur eindeutigen Wahlevaluation für den Alumni-Rat der Stiftung Schweizer Jugend forscht anhand der bindenden Diversitätskriterien*


(Art. 4 Organisationsreglement des SJf-Alumni-Rates, Version 30.11.2023)


#### Ausführen

`EVALUATION.ipynb`

Online auführen auf Binder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/janjoch/sjf-alumniboard-election-algo/HEAD)

Ansehen auf NBViewer:
[![NBViewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.org/github/janjoch/sjf-alumniboard-election-algo/tree/main/EVALUATION.ipynb)


#### Kriterien

* `A1` Mindestens zwei (2) Personen aus der Deutschschweiz;
* `A2` mindestens eine (1) Person aus der französischen Schweiz;
* `A3` mindestens eine (1) Person aus der italienischen Schweiz. Massgebend ist die Muttersprache. 
* `B` Mindestens drei (3) Personen sind zum Zeitpunkt des Amtsantrittes Alumni bzw. Alumnae durch erstmalige Teilnahme am Nationalen Wettbewerb oder ISTF der letzten drei (3) Kalenderjahren. 
* `C` Mindestens eine (1) Person hat vor mehr als zehn (10) Jahren erstmals an einem Wettbewerb oder ISTF teilgenommen.
* `D` Maximal zwei (2) Personen sind nicht Alumni bzw. Alumnae von SJf. 


#### Rohdaten

Die Ergebnisse der Wahl inkl. Informationen über die erfüllten Diversitätskriterien der Kandidat\*innen sind in der Datei `Wahlergebnisse.xlsx` im vorgegebenen Format abzulegen. Die hier vorhandene Beispieldatei kann ersetzt werden, oder der Dateipfad im Programm angepasst werden. Wird das Skript ohne Änderung der Datei ausgeführt, so werden die Musterdaten ausgewertet.

Kandidat\*innen mit der selben Anzahl Stimmen sollten beim Erfassen per Los sortiert werden. Der Algorithmus evaluiert bei Stimmengleichheit die Einträge von oben nach unten. (Aus Gründen der Reproduzierbarkeit wurde auf zufällige Auslosung im Algorithmus verzichtet.)


#### Algorithmus

##### Motivation

Um die beste Zusammensetzung anhand der Diversitätskriterien eindeutig zu bestimmen, ist eine Gewichtung anhand der Rangliste in Zweierpotenzen unabdingbar. Dabei hat die Person mit den meisten Stimmen Gewicht 1, die nächste 2, die darauffolgende 4, dann 8, usw. Die beste Zusammensetzung *1,2,3,4,5,6,7* hat dann eine gewichtete Summe von 127. Die nächstbeste, *1,2,3,4,5,6,8* zählt 191, dann *1,2,3,4,5,7,8* 223. Je tiefer diese Summe, je besser. Würden lediglich die Anzahl Stimmen aufsummiert, so könnte es zu Stimmengleichheit mehrerer Kombinationen führen. Zudem wäre dies programmatisch weniger eindeutig implementierbar.


##### Ablauf

1. Die Kandidat\*innen werden in einer Rangliste nach Anzahl Stimmen sortiert.
2. Die Kombinationen werden systematisch auf die Erfüllung aller Kriterien geprüft:

    1. Ränge 1-7
    2. Ränge 1-6+8
    3. Ränge 1-5+7-8
    4. ...
    5. Ränge 2-8
    6. Ränge 1-6+9
    7. Ränge 1-5+8-9
    8. Ränge 1-4+7-9
    9. ...


##### Implementierung des Algorithmus

Der Quellcode ist in der Datei `election_algorithm.py` zu finden. Das Programm wurde ausgiebig getestet, es wird jedoch keine Garantie übernommen. Die generierten Resultate sollten auf Plausibilität geprüft werden!

Autor: Janosch Jörg (Arbeitsgruppe Alumni-Rat), 2024, [github.com/janjoch](https://github.com/janjoch), [janjo@duck.com](mailto:janjo@duck.com)

