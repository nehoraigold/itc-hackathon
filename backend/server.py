from bottle import run, get, static_file, request, post, response
import json
from backend.polygon_v3 import report_insert_DB


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="../frontend/js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="../frontend/css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="../frontend/images")


@get("/")
def html():
    return static_file("main.html", root='../frontend')


@get('/get_areas')
def get_polygons():
    with open('./polygons_coordinates/polygons.json') as polygons_file:
        polygons = json.loads(polygons_file.read())
        return json.dumps({"polygons": polygons})


@post('/report')
def report():
    lat = request.POST.get('lat')
    long = request.POST.get('long')
    timestamp = request.POST.get('timestamp')
    is_found = request.POST.get('is_found')
    report_insert_DB(lat, long, timestamp, is_found)
    return json.dumps({"msg": "success"})


def main():
    run(host='localhost', port=7000)


if __name__ == "__main__":
    main()
