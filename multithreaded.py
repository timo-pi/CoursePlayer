import sys
import time
import threading
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

def start_server():
    # server_address = (ip, port)
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()


threading.Thread(target=start_server).start()
print("1.")
time.sleep(2)
webbrowser.open('http://localhost:8000')
(print("2."))
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)