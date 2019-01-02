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
import os

import sqlite3
DB_FILENAME = 'available_log.db'

LATITUDE = 0
LONGITUDE = 1
SCALING_FACTOR = 82247

cwd = os.getcwd()


def point_in_polygons(user_point, polygons_list):
    """
    Takes a polygon and a list of points and returns a boolean array if the points are in the polygon
    :param user_point:
    :param polygons_list:
    :return:
    """
    arr = np.array([polygon.contains(user_point) for polygon in polygons_list])
    try:
        poly_id = np.where(arr == True)[0][0] + 1
        return poly_id
    except IndexError:
        print("not in the polygon")

def cast_json_into_list():
    try:
        with open("polygons_coordinates/polygons.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("file not found !")


def json_coordinates(json_data):
    return np.array([city["coords"] for city in json_data])


def coord_in_lat_long(list_lat_long):
    """
    For tuples from lists with successively coordinates [lat, long, lat, long] --> [[lat, long], [lat, long]]
    :param list_lat_long:
    :return:
    """
    mid = len(list_lat_long) // 2
    print("Number of coordinates : {}".format(mid))
    return [[list_lat_long[2 * counter], list_lat_long[2 * counter + 1]] for counter in range(mid)]


def project_long_lag_coord_into_cartesian(list_lat_long):
    """
    Cast geographic coordinates (long, lat) into cartesian coordinates
    :param list_lat_long:
    :return:
    """
    # setup your projections
    # crs_wgs = proj.Proj(init='epsg:4326')  # assuming you're using WGS84 geographic
    crs_wgs = proj.Proj(init='epsg:3857')  # assuming you're using WGS3857 geographic
    crs_bng = proj.Proj(init='epsg:2039')  # use a locally appropriate projected CRS

    return [(proj.transform(crs_wgs, crs_bng, lat_long[LONGITUDE], lat_long[LATITUDE])) for lat_long in list_lat_long]


def gen_rdm_points_square(polygon, size):
    """
    Generate rdm points within a square box
    :param polygon:
    :param size:
    :return:
    """
    minx, miny, maxx, maxy = polygon.bounds
    box_points = list(box(minx, miny, maxx, maxy, ccw=True).exterior.coords)
    x = np.random.uniform(low=box_points[0][0], high=box_points[2][0], size=size)
    y = np.random.uniform(low=box_points[0][1], high=box_points[2][1], size=size)
    return np.array(list(zip(x, y)))


def plot_polygon(polygon, size_points_distrib=50):
    """
    Plots polygon with bound box and sample distribution
    :param polygon:
    :param size_points_distrib:
    :return:
    """
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
    ax.set(xlim=[minx, maxx])
    ax.set(ylim=[miny, maxy])

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


def distance_user_point_to_polygons(user_point, polygon_list):
    """
    Takes a position of a user and returns a list of sorted distance with corresponding polygons
    :param lat_u:
    :param long_u:
    :param polygon_list:
    :return:
    """
    list_polygons_distances = []

    for polygon in polygon_list:
        dist = user_point.distance(polygon)
        list_polygons_distances.append(dist)

    #return sorted(list_polygons_distances, key=lambda x: x[1], reverse=True)
    return list_polygons_distances


def insert_rows_to_available_log(poly_id, time, found, n):
    """
    poly_id: to polygon id
    time: a float 0 <= time <= 24
    found: boolean
    n: number of duplicate rows we want to add
    """
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        data = (list(zip(n*[poly_id], n*[time], n*[1.0*found])))
        stmt = "INSERT INTO log_tbl (area_id, time, found) VALUES (?, ?, ?)"
        cur.executemany(stmt, data)
        cur.close()

def report_insert_DB(lat_u, long_u, timestamp, is_found):
    """
    Takes the latitude & longitude, timestamp, is found, and inserts into the database
    :param lat:
    :param long:
    :param timestamp:
    :param is_found:
    :return:
    """

    coord_u = project_long_lag_coord_into_cartesian([[lat_u, long_u]])
    xu, yu = coord_u[0][0], coord_u[0][1]
    user_point = Point(xu, yu)

    # Create my list of polygons from json
    json_data = cast_json_into_list()
    polygons_lat_long_coord = json_coordinates(json_data)

    # project lat-long to a plan
    polygons_cartesians_coord = [project_long_lag_coord_into_cartesian(_) for _ in polygons_lat_long_coord]

    # creates a list of polygons
    polygons_list = np.array([Polygon(_) for _ in polygons_cartesians_coord])

    # list of distances
    distances_list = np.array([distance_user_point_to_polygons(user_point, polygons_list)])
    distances_list_scaled = np.array([np.round(SCALING_FACTOR*elt, 0).astype(int) for elt in distances_list])

    # Returns ID of the polygon
    poly_id = point_in_polygons(user_point, polygons_list)
    #print("id is : {}".format(poly_id))

    # Insert into the DB the ID of the polygon
    insert_rows_to_available_log(poly_id, timestamp, is_found, n=100)


def main():
    #plot_polygon(jerusalem_polygon)

    # Find scaling factor for distance
    coord_p1 = project_long_lag_coord_into_cartesian([[32.052909,34.772081]])
    coord_p2 = project_long_lag_coord_into_cartesian([[31.968647,34.800475]])
    x1, y1 = coord_p1[0][0], coord_p1[0][1]
    x2, y2 = coord_p2[0][0], coord_p2[0][1]
    dist_two_points = Point(x1, y1).distance(Point(x2, y2))

    factor_value = 9470/dist_two_points
    print(factor_value)

    # scaling factor * projected distance = real distance
    SCALING_FACTOR = 82247

    # User input
    #lat_u, long_u = 32.052909, 34.772081 point next to ITC

    lat_u, long_u = 31.76851105490533, 35.2048945426941

    coord_u = project_long_lag_coord_into_cartesian([[lat_u, long_u]])
    xu, yu = coord_u[0][0], coord_u[0][1]
    user_point = Point(xu, yu)

    # Create my list of polygons from json
    json_data = cast_json_into_list()
    polygons_lat_long_coord = json_coordinates(json_data)

    # project lat-long to a plan
    polygons_cartesians_coord = [project_long_lag_coord_into_cartesian(_) for _ in polygons_lat_long_coord]

    # creates a list of polygons
    polygons_list = np.array([Polygon(_) for _ in polygons_cartesians_coord])

    # list of distances
    distances_list = np.array([distance_user_point_to_polygons(user_point, polygons_list)])
    distances_list_scaled = np.array([np.round(SCALING_FACTOR*elt, 0).astype(int) for elt in distances_list])

    # Returns ID of the polygon
    poly_id = point_in_polygons(user_point, polygons_list)
    print("id is : {}".format(poly_id))

    # Insert into the DB the ID of the polygon
    #insert_rows_to_available_log(poly_id, )


    print(distances_list_scaled)

    #print(polygons_list)
    #print(distances_list)

    #plot_polygon(polygons_list[3])




if __name__ == '__main__':
    main()

report_insert_DB(31.76851105490533, 35.2048945426941, 12.5, True)
