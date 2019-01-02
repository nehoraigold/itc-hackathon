from bottle import run, get, static_file, request, response


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="../frontend/js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="../frontend/css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="images")


@get("/")
def html():
    return static_file("main.html", root='../frontend')


@get('/get_areas')
def get_polygons():
    return "ok"


def main():
    run(host='localhost', port=7000)


if __name__ == "__main__":
    main()
