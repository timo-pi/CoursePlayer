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
# pyinstaller --add-data --onefile --clean -y coursePlayer_v2.0.py
#*****************************************************

# Variables

extracted_scorm_path = ''
# httpd = http.server.HTTPServer
startCwd = os.getcwd()

# Webserver
def startWebServer():
    #os.chdir(extracted_scorm_path)
    try:
        path = os.getcwd()
        os.chdir(path[0:3])
        print("starting server - path name: " + extracted_scorm_path)
        print(os.chdir(path[0:3]))
        httpd = http.server.HTTPServer(('localhost', 8000), http.server.SimpleHTTPRequestHandler)
        httpd.serve_forever()
    except:
        path = os.getcwd()
        os.chdir(path[0:3])
        print("starting server - path name: " + extracted_scorm_path)
        print(os.chdir(path[0:3]))
        print("Webserver is running!")

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
        elif file == 'start_am.html':
            return 'start_am.html'
        elif file == 'start_am_scorm.html':
            return 'start_am_scorm.html'
        elif file == "scormcontent":
            return "scormcontent/"
    """    # check if app runs from exe or dev-env.
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        # copy file to extracted directory
        info_path = os.path.join(base_path, 'info.htm')
        os.chdir(extracted_scorm_path)
        shutil.copyfile(info_path, './info.htm')
        time.sleep(2)"""
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
    print("start_file: " + start_file)
    threading.Thread(target=startWebServer).start()
    openBrowser(start_file)

def close_window():
    time.sleep(1)
    root.destroy()
    print("Course loaded: " + extracted_scorm_path)

# Executing start file in browser
def openBrowser(start_file):
    print("preparing environment")
    start_path = 'http://localhost:8000/' + extracted_scorm_path[3:] + '/' + start_file
    print("Start Path: " + start_path)
    time.sleep(1)
    print("open browser...")
    time.sleep(1)
    subprocess.call(['start', start_path], shell=True)
    time.sleep(1)
    #close_window()

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
    label_status.place(x=10, y=50, width=320, height=30)

root = tk.Tk()
root.geometry('340x230')
root.title('SIT | Course Player')
btn_select = tk.Button(root, text="Select SCORM zip file", command=buttonPressed)
btn_quit = tk.Button(root, text="Quit", command=lambda: close_window())
btn_select.place(x=100, y=110, width=140, height=30)
btn_quit.place(x=100, y=145, width=140, height=30)

text_status = tk.StringVar()
text_status.set("Please select a SCORM-File")
label_status = tk.Label(root, textvariable=text_status, borderwidth=2, relief="groove", anchor="c")
label_status.place(x=10, y=50, width=320, height=30)

root.mainloop()



# TODO: Try/ Catch Block for Webserver Thread, change Webserver root to c:, adjust path accordingly, recognize restart with running webserver
# TODO: Add "Delete unpacked files" button and "Close" button
# TODO: Add Label with loaded path/ SCORM package
