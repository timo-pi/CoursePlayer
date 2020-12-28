from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time
import webbrowser
import os
import subprocess
from zipfile import ZipFile

# Variables
zip_path = 'c:\\temp\\scorm\\'
zip_file = 'testpaket.zip'
extracted_scorm_path = ''

# Webserver
def startWebserver():
    os.chdir(extracted_scorm_path)
    print("starting server...")
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

# Find start-html
def searchStartFile(path):
    for file in os.listdir(path):
        if file.endswith('.html'):
            if file == 'story.html':
                return 'story.html'

# Extract SCORM file
def extractScorm():
    with ZipFile(zip_path + zip_file, 'r') as zip_ref:
        global extracted_scorm_path
        extracted_scorm_path = zip_path + zip_file[:-4]
        zip_ref.extractall(extracted_scorm_path)

    # Find Startfile
    start_file = searchStartFile(extracted_scorm_path)
    threading.Thread(target=startWebserver).start()
    time.sleep(5)
    openBrowser(start_file)

# Executing start file in browser
def openBrowser(start_file):
    print("open browser...")
    #webbrowser.open('http://localhost:8000/' + start_file)
    #subprocess.call(['start', 'http://localhost:8000'])
    start_path = 'http://localhost:8000/' + start_file
    subprocess.call(['start', start_path], shell=True)


if __name__ == "__main__":
    extractScorm()
