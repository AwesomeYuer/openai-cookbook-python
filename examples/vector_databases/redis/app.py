from flask import Flask, Response
import time
from http.server import SimpleHTTPRequestHandler
import socketserver
from a import *
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

# def application(environ, start_response):
#     status = '200 OK'
#     headers = [('Content-type', 'text/plain')]
#     start_response(status, headers)
#     return [b'Python, WSGI!']

# with make_server('', 5000, application) as httpd:
#     print('Serving on port 5000...')
#     httpd.serve_forever()



app = Flask(__name__)

@app.route("/wikipedia")
def hello_world():
    # response = Response('Flask Python!')
    # del response.headers['Connection']
    return "Flask Python!"

app.run()


PORT = 5000

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = "python"
        print(message)
        # SearchProcess()
        
        self.wfile.write(bytes(message, "utf8"))
        

# with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()
