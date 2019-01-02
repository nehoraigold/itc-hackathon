from shapely.geometry import Polygon, Point, LinearRing
from shapely.geometry import box
import pyproj as proj
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import spatial
import random
import ast
import json


LATITUDE = 0
LONGITUDE = 1


def points_in_polygons(polygon, points_list):
    """
    Takes a polygon and a list of points and returns a boolean array if the points are in the polygon
    :param polygon:
    :param points_list:
    :return:
    """
    return np.array([polygon.contains(Point(point)) for point in points_list])

def cast_json_into_list(my_json):
    with open("polygons_coordinates/polygons.json", "r") as file:
        data = json.load(file)
        return data

def json_coordinates(json_data):
    return np.array([city["coords"] for city in json_data])

# Transform R. input into list of coordinates
jerusalem_polygon_points = [31.767425, 35.203268, 31.767156, 35.203171, 31.767092, 35.205059, 31.767886, 35.205413,
                            31.768483, 35.205859, 31.768757, 35.20654, 31.768994, 35.207189, 31.769395, 35.208659,
                            31.770061, 35.208557, 31.770043, 35.20809, 31.770312, 35.207897, 31.770162, 35.207135,
                            31.769929, 35.207398, 31.769578, 35.206679, 31.768935, 35.205333, 31.768369, 35.204437]


def coord_in_lat_long(list_lat_long):
    """
    For tuples from lists with successively coordinates [lat, long, lat, long] --> [[lat, long], [lat, long]]
    :param list_lat_long:
    :return:
    """
    mid = len(list_lat_long) // 2
    print("Number of coordinates : {}".format(mid))
    return [[list_lat_long[2 * counter], list_lat_long[2 * counter + 1]] for counter in range(mid)]


def cast_long_lag_coord_into_cartesian(list_lat_long):
    """
    Cast geographic coordinates (long, lat) into cartesian coordinates
    :param list_lat_long:
    :return:
    """
    # setup your projections
    # crs_wgs = proj.Proj(init='epsg:4326')  # assuming you're using WGS84 geographic
    crs_wgs = proj.Proj(init='epsg:3857')  # assuming you're using WGS3857 geographic
    crs_bng = proj.Proj(init='epsg:4326')  # use a locally appropriate projected CRS

    return [(proj.transform(crs_wgs, crs_bng, lat_long[LONGITUDE], lat_long[LATITUDE])) for lat_long in list_lat_long]


def gen_rdm_points_square(polygon, size):
    minx, miny, maxx, maxy = polygon.bounds
    box_points = list(box(minx, miny, maxx, maxy, ccw=True).exterior.coords)
    x = np.random.uniform(low=box_points[0][0], high=box_points[2][0], size=size)
    y = np.random.uniform(low=box_points[0][1], high=box_points[2][1], size=size)
    return np.array(list(zip(x, y)))


def plot_polygon(polygon, size_points_distrib=50):
    # Get the points
    list_points = list(polygon.exterior.coords)
    distances = np.array(scipy.spatial.distance.euclidean([elt[0] for elt in list_points], [elt[1] for elt in list_points]))
    avg_dist = distances.mean()

    # Get the boundaries
    minx, miny, maxx, maxy = polygon.bounds
    box_points = box(minx, miny, maxx, maxy, ccw=True)

    fig, ax = plt.subplots(figsize=(10, 10))

    # Box
    plt.scatter(*zip(*list(box_points.exterior.coords)), color='black', linestyle="--", alpha=0.2)
    plt.plot(*zip(*list(box_points.exterior.coords)), color='black', linestyle="--", alpha=0.2)

    # Polygon
    plt.scatter(*zip(*list_points), color='blue')
    plt.plot(*zip(*list(list_points)), color='blue', linestyle="-.", alpha=0.2)
    ax.set(xlim=[minx-avg_dist/10000, maxx+avg_dist/10000])
    ax.set(ylim=[miny-avg_dist/10000, maxy+avg_dist/10000])

    # Limits
    rdm_points = gen_rdm_points_square(polygon, size_points_distrib)
    # creates mask
    is_in_distrib = points_in_polygons(polygon, rdm_points)
    print(rdm_points[is_in_distrib])

    # Points in
    x_in, y_in = zip(*rdm_points[is_in_distrib])
    plt.scatter(x_in, y_in, color='green', alpha=0.2, marker="+")

    # Points out
    x_out, y_out = zip(*rdm_points[~is_in_distrib])
    plt.scatter(x_out, y_out, color='red', alpha=0.2, marker="+")

    plt.show()



######


def main():
    # User input
    lat_u, long_u = 32.052909,34.772081
    xu, yu = (cast_long_lag_coord_into_cartesian([lat_u, long_u]))
    dist = point.distance(poly)
    >> > print
    dist
    point = Point(0.5, 2)
    polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])

    #assert points_in_polygons(polygon, [(2, 3), (8, 9), (0.5, 0.5)]) == np.array([False, False, True])


    test_inside_outside = [31.768877, 35.20617, 31.768238, 35.205646, 31.769321, 35.207839, 31.76845, 35.206905, 31.768799,
                           35.206951, 31.770379, 35.203011]

    jerusalem_points = coord_in_lat_long(jerusalem_polygon_points)
    jerusalem_polygon = Polygon(cast_long_lag_coord_into_cartesian(jerusalem_points))

    list_test_inside_outside = coord_in_lat_long(test_inside_outside)
    casted_inside_outside = cast_long_lag_coord_into_cartesian(list_test_inside_outside)

    print(jerusalem_polygon)
    print(points_in_polygons(jerusalem_polygon, casted_inside_outside))
    minx, miny, maxx, maxy = jerusalem_polygon.bounds
    print(minx, miny, maxx, maxy)

    print(box(minx, miny, maxx, maxy, ccw=True))

    plot_polygon(jerusalem_polygon)

    poly = Polygon([(0, 0), (2,8), (14, 10), (6,1)])
    point = Point(12,4)

    pol_ext = LinearRing(poly.exterior.coords)
    d = pol_ext.project(point)
    p = pol_ext.interpolate(d)
    closest_point_coords = list(p.coords)[0]

    #2nd example
    poly = Polygon([(0, 0), (2,8), (14, 10), (6,1)])
    point = Point(12,4)

    pol_ext = LinearRing(poly.exterior.coords)
    d = pol_ext.project(point)
    p = pol_ext.interpolate(d)
    closest_point_coords = list(p.coords)[0]

    print(closest_point_coords)




if __name__ == '__main__':
    main()


