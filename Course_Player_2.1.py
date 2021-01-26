import http.server
import threading
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import zipfile
import time
from xml.dom import minidom


#**************************************************+++
# Command to build exe:
# pyinstaller --onefile --clean -y --icon=schwarz.ico Course_Player_2.1.py
# pyinstaller --onefile --windowed --clean -y --icon=schwarz.ico Course_Player_2.1.py
#*****************************************************

# Variables
version = 'v2.2'
extracted_scorm_path = ''
# httpd = http.server.HTTPServer
startCwd = os.getcwd()

# Webserver
def startWebServer():
    #os.chdir(extracted_scorm_path)
    try:
        path = os.getcwd()
        # Starting Webserver from root directory
        os.chdir(path[0:3])
        print("starting server...")
        # print(os.chdir(path[0:3]))
        httpd = http.server.HTTPServer(('localhost', 8000), http.server.SimpleHTTPRequestHandler)
        print("Webserver is running!")
        httpd.serve_forever()
    except:
        path = os.getcwd()
        os.chdir(path[0:3])
        print("starting server - path name: " + extracted_scorm_path)
        #print(os.chdir(path[0:3]))
        print("Webserver is running!")

# Find start-html file
def searchStartFile(path):
    for file in os.listdir(path):
        if file == 'story.html':
            return 'story.html'
        elif file == 'index.html':
            return 'index.html'
        elif file == 'start_am.html':
            return 'start_am.html'
        elif file == 'start_lm.html':
            return 'start_lm.html'
        elif file == 'start_lm_scorm.html':
            return 'start_lm_scorm.html'
        elif file == 'start_am_scorm.html':
            return 'start_am_scorm.html'
        elif file == 'index_scorm.html':
            return 'index_scorm.html'
    try:
        domtree = minidom.parse(path + "/imsmanifest.xml")
        rootnode = domtree.documentElement
        resource = rootnode.getElementsByTagName('resource')
        for r in resource:
            if r.hasAttribute('href'):
                print("start-path in imsmanifest.xml: ")
                return r.getAttribute('href')
    except:
        return ''

# Extract SCORM file
def extractScorm(filename):
    # btn_select.config(state="disabled")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        global extracted_scorm_path
        extracted_scorm_path = filename[:-4]
        zip_ref.extractall(extracted_scorm_path)

    # Find Startfile
    start_file = searchStartFile(extracted_scorm_path)
    print(str(start_file))
    threading.Thread(target=startWebServer).start()
    openBrowser(start_file)

def close_window():
    time.sleep(0.5)
    root.destroy()
    print("Course loaded: " + extracted_scorm_path)

# Executing start file in browser
def openBrowser(start_file):
    print("preparing environment")
    start_path = 'http://localhost:8000/' + extracted_scorm_path[3:] + '/' + start_file
    start_path = start_path.replace(" ", "%20")
    print("Start Path: " + start_path)
    time.sleep(1)
    print("open browser...")
    time.sleep(1)
    subprocess.call(['start', start_path], shell=True)
    time.sleep(1)

# GUI

def buttonPressed():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    scorm = os.path.basename(root.filename)
    print("Open SCORM Package: " + scorm)
    setLabelText(scorm)
    # root.title(os.path.splitext(root.filename)[0])
    extractScorm(root.filename)

def setLabelText(text):
    text_status.set(text)
    label_status = tk.Label(root, textvariable=text_status, borderwidth=2, relief="groove", anchor="c")
    label_status.place(x=10, y=70, width=420, height=30)

root = tk.Tk()
root.geometry('440x300')
title_version = 'SIT | Course Player ' + version
root.title(title_version)
print(version)
#root.iconbitmap('./schwarz.ico')
btn_select = tk.Button(root, text="Select SCORM zip-file", command=buttonPressed)
btn_quit = tk.Button(root, text="Quit", command=lambda: close_window())
btn_select.place(x=150, y=140, width=140, height=30)
btn_quit.place(x=150, y=180, width=140, height=30)

text_status = tk.StringVar()
text_status.set("Please select a SCORM-File")
label_status = tk.Label(root, textvariable=text_status, borderwidth=2, relief="groove", anchor="c")
label_status.place(x=10, y=70, width=420, height=30)

root.mainloop()
