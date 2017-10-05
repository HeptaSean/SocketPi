from socket_switch import SocketRemote


def application(environ, start_response):
    query = environ['QUERY_STRING']
    socket = query.upper()
    if socket:
        remote = SocketRemote()
        success = remote.switch_socket(socket)
        remote.close()
        if not success:
            socket = ''
    body = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Socket Switching App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
body {
    margin: 0;
    font-family: sans-serif;
    font-weight: bold;
    font-size: 20px;
}
a.button {
    display: block;
    box-sizing: border-box;
    width: 80%;
    padding: 6px;
    margin: 10px 10%;
    border-radius: 10px;
    border-style: solid;
    border-width: 4px;
    border-color: #aaaaff;
    background-color: #aaaaff;
    color: #000000;
    text-decoration: none;
    text-align: center;
}
a.button:hover {
    border-color: #0000ff;
}
a.button:visited {
}
p.status {
    box-sizing: border-box;
    width: 80%;
    padding: 10px;
    margin: 10px 10%;
    background-color: #aaffaa;
}
    </style>
    <script>
history.replaceState(
    null,
    "Socket Switching App",
    location.href.split('?')[0]
);
    </script>
  </head>
  <body>
    <a class="button" href="?a">Switch Socket A</a>
    <a class="button" href="?b">Switch Socket B</a>
    <a class="button" href="?c">Switch Socket C</a>
    <a class="button" href="?d">Switch Socket D</a>"""
    if socket:
        body += """
    <p class="status">Socket {} switched.</p>""".format(socket)
    body += """
  </body>
</html>"""
    body = body.encode('utf-8')
    status = '200 OK'
    headers = [('Content-Type', 'text/html'),
               ('Content-Length', str(len(body)))]
    start_response(status, headers)
    return [body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8080, application)
    httpd.serve_forever()
