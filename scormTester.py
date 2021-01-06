from xml.dom import minidom
import re, os
import tkinter as tk
from tkinter import filedialog
from xmlHelper import xmlHelper as xhelp
from scormExtractor import ScormExtractor as se

unzip_path = ""

def saveImsmanifest(rootnode, path):
    with open(path, 'w') as f:
        f.write(rootnode.toxml())
        # f.write(adln_presentation.toprettyxml())
        f.close()

def runChecks(imsmanifest):
    # open xml document
    domtree = minidom.parse(imsmanifest)
    rootnode = domtree.documentElement
    new_imsmanifest = False

    # check SCORM version
    scorm_version = xhelp.checkScormVersion(rootnode)
    if "2004 4th Edition" in scorm_version:
        print("SCORM Version: 2004 4th Edition")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#c7d66d')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM Version: 2004 4th Edition')
    elif "CAM 1.3" in scorm_version or "2004 2nd Edition" in scorm_version:
        print("SCORM 2004 2nd Edition")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#fe5f55')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM 2004 2nd Edition')
    elif scorm_version == "1.2":
        print("SCORM Version: SCORM 1.2")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#c7d66d')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM Version: 1.2')
    elif "2004 3rd Edition" in scorm_version:
        print("SCORM 2004 3rd Edition")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#c7d66d')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM Version: 2004 3rd Edition')
    else:
        print("SCORM  Version: unknown")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#fe5f55')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM Version: unknown')

    # check for multiple items
    print(xhelp.checkOneItemOnly(rootnode))
    if xhelp.checkOneItemOnly(rootnode):
        label_item = tk.Label(root, textvariable=text_item, anchor="w", background='#c7d66d')
        label_item.place(x=20, y=80, width=360, height=30)
        text_item.set("Passed: Only one Item element present.")

    # check for adlnav namespace in manifest
    try:
        test = rootnode.getAttribute("xmlns:adlnav")
        if test == "":
            print("adlnav-namespace NOT found in manifest tag!")
            rootnode.setAttribute("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")
            print("Created namespace entry: " + rootnode.getAttribute("xmlns:adlnav"))
            new_imsmanifest = True
    except:
        print("Exception checking adlnav attribute in manifest element")

    # check for adlnav presentation in item element
    if xhelp.checkAdlnavPresentation(rootnode):
        pass
    else:
        domtree = xhelp.adlnavHideElements(domtree)
        new_imsmanifest = True

    # adlnav GUI + file update
    if new_imsmanifest:
        saveImsmanifest(rootnode, unzip_path)
        label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w", background='#ffd275')
        label_namespace.place(x=20, y=50, width=360, height=30)
        text_namespace.set("New imsmanifest.xml has been created!")
    else:
        label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w", background='#c7d66d')
        label_namespace.place(x=20, y=50, width=360, height=30)
        text_namespace.set("Passed: Namespace present")

    # check filenames for special characters
    if xhelp.checkSpecialCharsInFileNames(rootnode):
        label_characters = tk.Label(root, textvariable=text_characters, anchor="w", background='#c7d66d')
        label_characters.place(x=20, y=110, width=360, height=30)
        text_characters.set("Passed: No special characters in file names.")
    else:
        label_characters = tk.Label(root, textvariable=text_characters, anchor="w", background='#fe5f55')
        label_characters.place(x=20, y=110, width=360, height=30)
        text_characters.set("Failed: Special Characters in file names!")

    # check if adlnav presentation is present an create it if not
    print(xhelp.checkAdlnavPresentation(rootnode))
    if xhelp.checkAdlnavPresentation(rootnode):
        print('adlnav presentation is already present!')
        pass
    else:
        xhelp.adlnavHideElements(domtree)
        print('adlnav presentation was created!')

def selectFiles():
    root.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    print(root.filenames)
    if len(root.filenames) == 1:
        global unzip_path
        unzip_path = se.extractScorm(root.filenames[0])
        runChecks(unzip_path)
    # NOT WORKING YET: MULTIPLE FILES SELECTED
    elif len(root.filenames) > 1:
        for i in root.filenames:
            unzip_path = se.extractScorm(i)
            text_scorm.set('Multiple files extracted!')

# GUI
root = tk.Tk()
text_scorm, text_namespace, text_item, text_characters, text_status = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
text_scorm.set("SCORM Version:")
text_namespace.set("Namespace check (adlnav):")
text_item.set("Only one Item present:")
text_characters.set("Special characters check:")
text_status.set("    Overall status:")

root.geometry('400x400')
#root.configure(background='#676767')
root.iconbitmap('./images/schwarz.ico')
root.title('SIT | SCORM Tester')

# Buttons
btn_select = tk.Button(root, text="Select File(s)", command=selectFiles)
btn_quit = tk.Button(root, text="Quit", command=lambda: root.destroy())
btn_select.place(x=130, y=270, width=140, height=30)
btn_quit.place(x=130, y=310, width=140, height=30)

# Labels
label_group = tk.Label(root, borderwidth=2, relief="groove")
label_group.place(x=10, y=10, width=380, height=140)
label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w")
label_scorm.place(x=20, y=20, width=360, height=30)
label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w")
label_namespace.place(x=20, y=50, width=360, height=30)
label_item = tk.Label(root, textvariable=text_item, anchor="w")
label_item.place(x=20, y=80, width=360, height=30)
label_characters = tk.Label(root, textvariable=text_characters, anchor="w")
label_characters.place(x=20, y=110, width=360, height=30)
label_status = tk.Label(root, textvariable=text_status, borderwidth=2, relief="groove", anchor="w")
label_status.place(x=10, y=170, width=380, height=30)

root.mainloop()
