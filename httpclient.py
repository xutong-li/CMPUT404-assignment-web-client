#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# Edited by Xutong Li for CMPUT404 Winter2021 Assignment 2
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
import urllib
from urllib.parse import urlparse

def help():
    print("httpclient.py [GET/POST] [URL]\n")


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    def get_host_port(self, url):
        return urlparse(url)

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        list = data.split("\r\n")
        status = list[0]
        code = int(status.split()[1])
        return code

    def get_headers(self, data):
        list = data.split("\r\n\r\n")
        header = list[0]
        return header

    def get_body(self, data):
        list = data.split("\r\n\r\n")
        body = list[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        urlparse = self.get_host_port(url)
        host = urlparse.hostname
        port = urlparse.port
        path = urlparse.path

        if path == "":
            path = "/"
        if port == "":
            port = 80

        self.connect(host, port)
        self.sendall("GET " + path + " HTTP/1.1\r\n" +
                     "Host: " + host + "\r\n" +
                     "User-Agent: Python-urllib\r\n" +
                     "Accept: */*\r\n" +
                     "Connection: close\r\n\r\n")

        response = self.recvall(self.socket)
        self.close()
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        urlparse = self.get_host_port(url)
        host = urlparse.hostname
        port = urlparse.port
        path = urlparse.path

        if path == "":
            path = "/"
        if port == "":
            port = 80

        content = ""
        if args is not None:
            content = urllib.parse.urlencode(args)

        self.connect(host, port)
        self.sendall("POST " + path + " HTTP/1.1\r\n" +
                     "Host: " + host + "\r\n" +
                     "User-Agent: Python-urllib\r\n"
                     "Accept: */*\r\n" +
                     "Content-Length: " + str(len(content)) + "\r\n" +
                     "Content-Type: application/x-www-form-urlencoded\r\n" +
                     "Connection: close\r\n\r\n" + content)

        response = self.recvall(self.socket)
        self.close()
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
