import shapefile
from shapely.geometry import Polygon

from helpers import xy_at_chainage, read_shapefile


def get_points_from_start_to_end(start, end, points_with_chainage):
    pts = [p for p in points_with_chainage if p[0] > start and p[0] < end]
    p_start = (start, *xy_at_chainage(start, points_with_chainage))
    p_end = (end, *xy_at_chainage(end, points_with_chainage))
    return [p_start] + pts + [p_end]


def creeer_vakindeling(shpfile: str, csvfile: str, outputfile: str):
    """Creeer een referentielijn op basis van een vakindeling bestand welke binnen
    Riskeer geimporteerd kan worden als een referentielijn voor een specifiek`
    faalmechanisme

    Werkwijze:

    Gebruik de in riskeer aanwezige referentielijn (je kunt deze exporteren via
    Traject | Referentielijn (rechtermuisknop) | Exporteren )

    Maak een csv bestand met de volgende inhoud;

    start,vaknaam
    0,stph_01
    1000,stph_02
    5000,stph_03

    Een header (verplicht) gevolgd door regels met de begin metrering als geheel getal en de vaknaam
    De eindmetrering wordt uit de volgende regel gehaald. Bij de laatste record wordt automatisch
    de lengte van de referentielijn toegevoegd

    Args:
        shpfile (str): pad naar de shapefile van de referentielijn (als geexporteerd uit Riskeer)
        csvfile (str): pad naar het csv bestand met metrering en dijkvak naam
        outputfile (str): pad naar het uitvoerbestand (*.shp)

    Raises:
        NotImplementedError: Melding als de geometrie van de invoer shapefile niet ondersteund is
    """
    lines = [
        s.strip() for s in open(csvfile, "r").readlines()[1:] if len(s.strip()) > 0
    ]

    points_with_chainage = read_shapefile(shpfile)

    with shapefile.Writer(outputfile) as w:
        w.field("Vaknaam", "C")
        end, xp, yp = 0, points_with_chainage[0][1], points_with_chainage[0][2]
        for i, line in enumerate(lines):
            args = line.split(",")
            start = int(args[0])
            name = args[1]

            if i == len(lines) - 1:
                end = points_with_chainage[-1][0]
            else:
                args = lines[i + 1].split(",")
                end = int(args[0])

            pts = get_points_from_start_to_end(start, end, points_with_chainage)

            w.record(name)  # * for unpacking tuple
            w.line([[p[1:] for p in pts]])


# test
if __name__ == "__main__":
    creeer_vakindeling(
        "testdata/referentielijn.shp",
        "testdata/stph_vakindeling.csv",
        "testdata/output/stph_vakindeling.shp",
    )
