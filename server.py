from bottle import run, get, static_file


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="images")


@get("/")
def html():
    return static_file("index.html", root='')


def main():
    run(host='localhost', port=7000)


if __name__ == "__main__":
    main()