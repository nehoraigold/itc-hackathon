import json

FILE = r"polygons_coordinates/polygons.json"


def coord_in_lat_long(list_lat_long):
    """
    For tuples from lists with successively coordinates [lat, long, lat, long] --> [(lat, long), (lat, long)]
    :param list_lat_long:
    :return:
    """
    mid = len(list_lat_long) // 2
    print("Number of coordinates : {}".format(mid))
    return [[list_lat_long[2 * counter], list_lat_long[2 * counter + 1]] for counter in range(mid)]


def insert_to_json(coords, name):
    """
    :param coords: list of coords
    :param name: name of polygone
    :return:
    """
    with open(FILE, 'r') as f:
        data = json.load(f)
    poly = {'Name': str(name), 'coords': coords}
    data.append(poly)

    with open(FILE, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':

    polygon_points = [] #input coordinates
    name = ''  #input name

    c_coords = coord_in_lat_long(polygon_points)

    insert_to_json(c_coords, name)
