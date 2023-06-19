from helpers import read_referenceline, xy_at_chainage
import numpy as np
from math import sin, cos, pi
import shapefile


def creeer_ahn_dwarsprofielen(
    shpfile: str,
    start_metrering: int,
    eind_metrering: int,
    hoh_afstand: int,
    m_naar_rivier: int,
    m_naar_polder: int,
    output_shp: str,
    output_dir: str,
):
    refline = read_referenceline(shpfile)

    chainages = np.arange(start_metrering, eind_metrering + hoh_afstand, hoh_afstand)

    with shapefile.Writer(output_shp) as w:
        w.field("Metrering", "C")
        for chainage in chainages:
            x, y, a = xy_at_chainage(chainage, refline, include_alpha=True)
            x1 = x + m_naar_rivier * cos(a - pi / 2.0)
            y1 = y + m_naar_rivier * sin(a - pi / 2.0)
            x2 = x - m_naar_polder * cos(a - pi / 2.0)
            y2 = y - m_naar_polder * sin(a - pi / 2.0)
            w.record(f"{chainage:5d}")  # * for unpacking tuple
            w.line([[[x1, y1], [x2, y2]]])


# test
if __name__ == "__main__":
    creeer_ahn_dwarsprofielen(
        shpfile="testdata/referentielijn.shp",
        start_metrering=0,
        eind_metrering=1000,
        hoh_afstand=100,
        m_naar_rivier=20,
        m_naar_polder=50,
        output_shp="testdata/output/dwarsprofielen.shp",
        output_dir="testdata/output/dwarsprofielen",
    )
