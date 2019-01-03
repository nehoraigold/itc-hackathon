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
    try:
        with open(FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        with open(FILE, 'x') as f:
            data = []

    index = len(data) + 1

    poly = {'Name': str(name), 'index': index, 'coords': coords}
    data.append(poly)

    with open(FILE, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    polygon_points = [32.051354, 34.771843, 32.051518, 34.77194, 32.051591, 34.77165, 32.052473, 34.771682, 32.05245,
                      34.772112, 32.052655, 34.772096, 32.052677, 34.771752, 32.053259, 34.771795, 32.053605, 34.770894,
                      32.053741, 34.770712, 32.053878, 34.770776, 32.05405, 34.768373, 32.052232, 34.767804, 32.051823,
                      34.769209, 32.051513, 34.770046, 32.050859, 34.771484]

    name = 'gina'  # input name

    c_coords = coord_in_lat_long(polygon_points)

    insert_to_json(c_coords, name)
