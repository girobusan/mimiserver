#!/usr/bin/env python3
"""
Very simple HTTP server in python for saving tiddly wiki
Usage:
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os , mimetypes , re

# File to serve
tw_file = "test.html"
#File, which serves by default
default_file = "root.html"
default_port = 9889

cnt_parts_re = re.compile("(\w+)=([\+\-.a-zA-Z0-9\\\/\"]+)")
tw_headers = {"none":"null"}



def parse_tw_header(txt):
    result = {}
    start = "<html>"
    si = int(str.find(txt, start))
    current_name = "untitled"
    matches = cnt_parts_re.findall(txt[:si])
    #print(matches);
    for m in matches:
        if m[0] == 'name':
            current_name = m[1].strip('"' + "'" + " " )
            result[current_name] = {}
        else:
            result[current_name][m[0].strip('"' + "'" + " " )] = m[1].strip('"' + "'" + " " )
    return result


def remove_headers(txt):
    start = "<html>"
    end="</html>"
    si = int(str.find(txt, start))
    li = int(str.rfind(txt,end)) + len(end)

    return txt[si:li]

class S(BaseHTTPRequestHandler):
    ctype =  'text/html'

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', self.ctype)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Vary', 'Accept-Encoding')
        self.end_headers()

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

        self.ctype = mimetypes.guess_type(self.path)
        if self.ctype[0] is None:
            self.ctype = 'text/html'
        self._set_response()   
        
        #print(self.ctype)
        if self.path=="/":
            #self.ctype = 'text/html'
            try:
                self.wfile.write(open(default_file , "r").read().encode('utf-8'))
            except:
                 self.wfile.write("No such file".encode('utf-8'))

        else:
            lpath = self.path[1:]
            if os.path.exists(lpath):
                #print("i have one")
                self.wfile.write(open(lpath , "br").read())
        

    def do_POST(self):
        
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        #logging.info("POST request,\nPath: %s\nHeaders:\n %s",
                #str(self.path), str(self.headers)) #post_data.decode('utf-8')
        tw_headers = parse_tw_header(post_data.decode('utf-8'))
        myfilecontent = remove_headers(post_data.decode('utf-8'))
        
        file_to_write = default_file
        #print("before" , tw_headers)
        #print(tw_headers["userfile"]["filename"].strip("/\\"))
        try:
            if tw_headers["userfile"]["filename"].strip("/\\") !="" :
                print("not default file")
                file_to_write = tw_headers["userfile"]["filename"].strip("/\\")
        except:
            print("Bad headers, default filename")

        open(file_to_write , "w").write(remove_headers(myfilecontent))
        #open("raw_content.html" , "w").write(myfilecontent)
        self.ctype = 'text/html'
        self._set_response()
        self.wfile.write("0 - Saved by the bell".encode('utf-8'))
        logging.info("Save complete for " + file_to_write)


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd at port ' + str(port) + "\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
        #logging.info("Listening on port" + int(argv[1]))
    else:
        run(port = default_port)
        #logging.info("Listening on port" + default_port)
