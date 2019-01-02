jerusalem = [ 31.767425,35.203268 , 31.767156,35.203171 , 31.767092,35.205059 , 31.767886,35.205413 , 31.768483,35.205859 , 31.768757,35.20654 , 31.768994,35.207189 , 31.769395,35.208659 , 31.770061,35.208557 , 31.770043,35.20809 , 31.770312,35.207897 , 31.770162,35.207135 , 31.769929,35.207398 , 31.769578,35.206679 , 31.768935,35.205333 , 31.768369,35.204437]
mosachim = [ 32.052389,34.772727 , 32.051462,34.772408 , 32.051067,34.77222 , 32.05073,34.772073 , 32.050054,34.773248 , 32.051075,34.773536 , 32.051586,34.773685 , 32.052091,34.773846 , 32.052282,34.773312]
north_tlv = [ 32.050827,34.776727 , 32.048781,34.776072 , 32.047899,34.778894 , 32.047471,34.781168 , 32.047344,34.782928 , 32.048935,34.783132 , 32.049008,34.781394 , 32.04989,34.78149 , 32.050545,34.779044 ]
shapira = [ 32.050827,34.776727 , 32.048781,34.776072 , 32.047899,34.778894 , 32.047471,34.781168 , 32.047344,34.782928 , 32.048935,34.783132 , 32.049008,34.781394 , 32.04989,34.78149 , 32.050545,34.779044]

def coord_in_lat_long(list_lat_long):
    """
    For tuples from lists with successively coordinates [lat, long, lat, long] --> [(lat, long), (lat, long)]
    :param list_lat_long:
    :return:
    """
    mid = len(list_lat_long) // 2
    print("Number of coordinates : {}".format(mid))
    return [[list_lat_long[2 * counter], list_lat_long[2 * counter + 1]] for counter in range(mid)]

jeru_points = coord_in_lat_long(jerusalem)
mosachim_points = coord_in_lat_long(mosachim)
north_tlv = coord_in_lat_long(north_tlv)
shapira = coord_in_lat_long(shapira)

print(jeru_points)
print(mosachim_points)
print(north_tlv)
print(shapira)