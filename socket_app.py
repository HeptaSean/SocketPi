from socket_switch import send_code

def application(environ, start_response):
    query = environ['QUERY_STRING']
    socket = query.upper()
    if socket == 'A':
        send_code(340)
    elif socket == 'B':
        send_code(1108)
    elif socket == 'C':
        send_code(1348)
    elif socket == 'D':
        send_code(1300)
    else:
        socket == ''
    body = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Socket Switching App</title>
  </head>
  <body>"""
    if socket:
        body += "\n<p>Socket {} switched</p>".format(socket)
    body += """
    <a href="?a">Switch Button A</a>
    <a href="?b">Switch Button B</a>
    <a href="?c">Switch Button C</a>
    <a href="?d">Switch Button D</a>
  </body>
</html>"""
    body = body.encode('utf-8')
    status = '200 OK'
    headers = [ ('Content-Type', 'text/html'),
                ('Content-Length', str(len(body))) ]
    start_response(status, headers)
    return [body]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8080, application)
    httpd.serve_forever()
