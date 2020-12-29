import http.server
import threading
import tkinter as tk
from tkinter import filedialog
import os, sys
import subprocess
import zipfile
import time
import shutil


#**************************************************+++
# Command to build exe:
# pyinstaller --add-data "info.htm;." --onefile --clean -y coursePlayerGui.py
#*****************************************************

# Variables
extracted_scorm_path = ''
# httpd = http.server.HTTPServer
startCwd = os.getcwd()

# Webserver
def startWebServer():
    os.chdir(extracted_scorm_path)
    print("starting server - path name: " + extracted_scorm_path)
    print(os.getcwd())
    httpd = http.server.HTTPServer(('localhost', 8000), http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()

# Find start-html file
def searchStartFile(path):
    for file in os.listdir(path):
        if file == 'story.html':
            return 'story.html'
        elif file == 'start_lm.html':
            return 'start_lm.html'
        elif file == 'index.html':
            return 'index.html'
        elif file == 'index_scorm.html':
            return 'index_scorm.html'
    # check if app runs from exe or dev-env.
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    # copy file to extracted directory
    info_path = os.path.join(base_path, 'info.htm')
    os.chdir(extracted_scorm_path)
    shutil.copyfile(info_path, './info.htm')
    time.sleep(2)
    return 'info.htm'

# Extract SCORM file
def extractScorm(filename):
    # btn_select.config(state="disabled")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        global extracted_scorm_path
        extracted_scorm_path = filename[:-4]
        zip_ref.extractall(extracted_scorm_path)

    # Find Startfile
    start_file = searchStartFile(extracted_scorm_path)
    print("extracted_scorm_path: " + extracted_scorm_path)
    threading.Thread(target=startWebServer).start()
    openBrowser(start_file)

def close_window():
    time.sleep(2)
    root.destroy()

# Executing start file in browser
def openBrowser(start_file):
    print("preparing environment")
    start_path = 'http://localhost:8000/' + start_file
    print("Start Path: " + start_path)
    time.sleep(1)
    print("open browser...")
    time.sleep(1)
    subprocess.call(['start', start_path], shell=True)
    time.sleep(1)
    close_window()

# GUI

def buttonPressed():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    print("filename: " + root.filename)
    # root.title(os.path.splitext(root.filename)[0])
    extractScorm(root.filename)

root = tk.Tk()
root.geometry('340x230')
root.title('SIT | Course Player')
btn_select = tk.Button(root, text="Select SCORM zip file", command=buttonPressed)
# btn_quit = tk.Button(root, text="Quit", command=close_window)
btn_select.place(x=100, y=75, width=140, height=30)
# btn_quit.place(x=125, y=125, width=140, height=30)
root.mainloop()
