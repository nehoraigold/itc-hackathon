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
    polygon_points = [32.101537, 34.78054, 32.101464, 34.779741, 32.099883, 34.779811, 32.09976, 34.780551, 32.099469,
                      34.780717, 32.099142, 34.780674, 32.09897, 34.781774, 32.099142, 34.782085, 32.100192, 34.781887,
                      32.100174, 34.781372, 32.101542, 34.780889]  # input coordinates
    name = 'north_tlv'  # input name

    c_coords = coord_in_lat_long(polygon_points)

    insert_to_json(c_coords, name)
