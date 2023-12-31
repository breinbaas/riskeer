from typing import Tuple
import shapefile
from math import hypot


def read_shapefile(shpfile: str) -> Tuple[float, float, float]:
    """Read a shapefile and return as a list of chainage, x, y points

    Args:
        shpfile (str): the path to the shapefile

    Raises:
        NotImplementedError: thrown if the geometry is not recognized

    Returns:
        Tuple[float, float, float]: points as [chainage, x, y]
    """
    shape = shapefile.Reader(shpfile)
    feature = shape.shapeRecords()[0]
    first = feature.shape.__geo_interface__
    if not first["type"] == "LineString":
        raise NotImplementedError(
            f"ReferenceLine.from_shape only handles LineString geometries but got a '{first['type']}' geometry."
        )
    points = [(p[0], p[1]) for p in first["coordinates"]]

    dl = 0
    points_with_chainage = []
    for i, p in enumerate(points):
        if i > 0:
            dl += hypot(
                points_with_chainage[-1][1] - p[0], points_with_chainage[-1][2] - p[1]
            )
        points_with_chainage.append((dl, *p))

    return points_with_chainage


def xy_at_chainage(chainage, points_with_chainage) -> Tuple[float, float]:
    """Get the x,y position of a chainage on a referenceline

    Args:
        chainage (_type_): the chainage to look for
        points_with_chainage (_type_): the points of the referenceline

    Raises:
        ValueError: thrown if the chainage is invalid

    Returns:
        Tuple[float, float]: the x, y position of the chainage on the given referenceline
    """
    for i in range(1, len(points_with_chainage)):
        c1, x1, y1 = points_with_chainage[i - 1]
        c2, x2, y2 = points_with_chainage[i]

        if chainage >= c1 and chainage <= c2:
            x = x1 + (chainage - c1) / (c2 - c1) * (x2 - x1)
            y = y1 + (chainage - c1) / (c2 - c1) * (y2 - y1)
            return x, y

    raise ValueError(
        f"Invalid chainage '{chainage}' is not between start and endpoint of the given referenceline"
    )
