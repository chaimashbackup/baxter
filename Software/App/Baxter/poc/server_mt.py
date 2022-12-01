#!/bin/python3

import os
import subprocess
import threading
import time

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

hostName = "10.0.0.10"
serverPort = 8080


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class BaxterServer(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.handlers = []
        self.add_handler('/hello2', self.hello2)
        self.add_handler('/hello', self.hello1)
        self.add_handler('/initial', self.initial_position) 
        self.add_handler('/object1', self.object1)
        self.add_handler('/object2', self.object2)
        self.add_handler('/put', self.put) 
        super(BaxterServer, self).__init__(request, client_address, server)

    def add_handler(self, path_prefix, handler):
        self.handlers.append([path_prefix, handler])

    def handle_path(self):
        for handler in self.handlers:
            if self.path.startswith(handler[0]):
                handler[1]()
                break
        else:
            self.default_handler()


    def put(self):
        cmd = "./../detect/put.py"
        proc = subprocess.Popen(
            cmd,
            encoding='utf-8',
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        stdout, stderr = proc.communicate()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Put</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Put.</p>", "utf-8"))
        self.wfile.write(bytes(str(stdout), "utf-8"))
        self.wfile.write(bytes(str(stderr), "utf-8"))
        self.wfile.write(bytes(str(proc.returncode), "utf-8"))
        message = threading.currentThread().getName()
        self.wfile.write(bytes(message, 'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def object1(self):
        cmd = "./../detect/object1.py"
        proc = subprocess.Popen(
            cmd,
            encoding='utf-8',
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        stdout, stderr = proc.communicate()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Object1</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Object1.</p>", "utf-8"))
        self.wfile.write(bytes(str(stdout), "utf-8"))
        self.wfile.write(bytes(str(stderr), "utf-8"))
        self.wfile.write(bytes(str(proc.returncode), "utf-8"))
        message = threading.currentThread().getName()
        self.wfile.write(bytes(message, 'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def object2(self):
        cmd = "./../detect/object2.py"
        proc = subprocess.Popen(
            cmd,
            encoding='utf-8',
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        stdout, stderr = proc.communicate()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Object2</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Object2.</p>", "utf-8"))
        self.wfile.write(bytes(str(stdout), "utf-8"))
        self.wfile.write(bytes(str(stderr), "utf-8"))
        self.wfile.write(bytes(str(proc.returncode), "utf-8"))
        message = threading.currentThread().getName()
        self.wfile.write(bytes(message, 'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def hello1(self):
        cmd = "/home/lev/rethink_ws/hello1.py"
        proc = subprocess.Popen(
            cmd,
            encoding='utf-8',
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        stdout, stderr = proc.communicate()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Right</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Right.</p>", "utf-8"))
        self.wfile.write(bytes(str(stdout), "utf-8"))
        self.wfile.write(bytes(str(stderr), "utf-8"))
        self.wfile.write(bytes(str(proc.returncode), "utf-8"))
        message = threading.currentThread().getName()
        self.wfile.write(bytes(message, 'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def hello2(self):
        cmd = "/home/lev/rethink_ws/hello2.py"
        proc = subprocess.Popen(
            cmd,
            encoding='utf-8',
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        stdout, stderr = proc.communicate()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Left</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Left.</p>", "utf-8"))
        self.wfile.write(bytes(str(stdout), "utf-8"))
        self.wfile.write(bytes(str(stderr), "utf-8"))
        self.wfile.write(bytes(str(proc.returncode), "utf-8"))
        message = threading.currentThread().getName()
        self.wfile.write(bytes(message, 'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def initial_position(self):
        cmd = "/home/lev/rethink_ws/initial_position.py"
        proc = subprocess.Popen(
            cmd,
            encoding='utf-8',
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        stdout, stderr = proc.communicate()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Initial Position</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Initial Position.</p>", "utf-8"))
        self.wfile.write(bytes(str(stdout), "utf-8"))
        self.wfile.write(bytes(str(stderr), "utf-8"))
        self.wfile.write(bytes(str(proc.returncode), "utf-8"))
        message = threading.currentThread().getName()
        self.wfile.write(bytes(message, 'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def default_handler(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Unkown command</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        message = threading.currentThread().getName()
        self.wfile.write(bytes(message, 'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_GET(self):
        self.handle_path()


if __name__ == "__main__":
    webServer = ThreadedHTTPServer((hostName, serverPort), BaxterServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
