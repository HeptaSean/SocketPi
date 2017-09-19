from wsgiref.simple_server import make_server

def application(environ, start_response):
    body = 'Test'.encode('utf-8')
    status = '200 OK'
    headers = [ ('Content-Type', 'text/plain'),
                ('Content-Length', str(len(body))) ]
    start_response(status, headers)
    return [body]

if __name__ == '__main__':
    httpd = make_server('', 8080, application)
    httpd.serve_forever()
