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

@app.route("/wikipedia/python-25k")
def hello_world():
    # response = Response('Flask Python!')
    # del response.headers['Connection']
    SearchProcess()
    return "Flask wikipedia python-25k!"

# app.run()

# hello.py
@app.route("/wikipedia/python-25k")
def application(environ, start_response):
    # 设置响应头
    headers = [('Content-Type', 'text/html')]
    # 调用 start_response 函数来发送响应头
    start_response('200 OK', headers)
    # 返回响应体
    return [b'wsgi']


# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('0.0.0.0', 5000, application)
# 开始监听HTTP请求:
httpd.serve_forever()