# riskeer
Helpful scripts for Riskeer | Dutch levee assessment system

## Creeer vakindeling

Creeer een referentielijn op basis van een vakindeling bestand welke binnen
Riskeer geimporteerd kan worden als een referentielijn voor een specifiek
faalmechanisme

**Werkwijze**

Gebruik de in riskeer aanwezige referentielijn (je kunt deze exporteren via
Traject | Referentielijn (rechtermuisknop) | Exporteren )

Maak een csv bestand met de volgende inhoud;

```
start,vaknaam
0,stph_01
1000,stph_02
5000,stph_03
```

Een header (verplicht) gevolgd door regels met de begin metrering als geheel getal en de vaknaam
De eindmetrering wordt uit de volgende regel gehaald. Bij de laatste record wordt automatisch
de lengte van de referentielijn toegevoegd

**Args:**

* shpfile (str): pad naar de shapefile van de referentielijn (als geexporteerd uit Riskeer)
* csvfile (str): pad naar het csv bestand met metrering en dijkvak naam
* outputfile (str): pad naar het uitvoerbestand (*.shp)

