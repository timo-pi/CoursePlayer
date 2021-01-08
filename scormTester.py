from xml.dom import minidom
import re, os
import tkinter as tk
from tkinter import filedialog
from xmlHelper import xmlHelper as xhelp
from scormExtractor import ScormExtractor as se
import scormZipper as sz
import writeExcel as we

multi_files_select = False
report_path = ""

def saveImsmanifest(rootnode, path):
    with open(path, 'w') as f:
        f.write(rootnode.toxml())
        # f.write(adln_presentation.toprettyxml())
        f.close()
    se.zipScorm(path)

def runChecks(path):
    report_data = [path]
    SCORM_2004_4 = False
    # open xml document
    try:
        domtree = minidom.parse(path + "/imsmanifest.xml")
        rootnode = domtree.documentElement
    except:
        print("Error parsing imsmanifest.xml - not found or faulty.")
        clearLabels()
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#fe5f55')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set("Error parsing imsmanifest.xml - not found or faulty.")
        label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w", background='#fe5f55')
        label_namespace.place(x=20, y=50, width=360, height=30)
        text_namespace.set("Please check your SCORM-File manually.")
        return 0

    # check SCORM version
    clearLabels()
    scorm_version = xhelp.checkScormVersion(rootnode)
    if "2004 4th Edition" in scorm_version:
        print("SCORM Version: 2004 4th Edition")
        SCORM_2004_4 = True
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#c7d66d')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM Version: 2004 4th Edition')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append(scorm_version)
    elif "CAM 1.3" in scorm_version or "2004 2nd Edition" in scorm_version:
        print("SCORM 2004 2nd Edition")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#fe5f55')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM 2004 2nd Edition')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("SCORM 2004 2nd Edition")
    elif scorm_version == "1.2":
        print("SCORM Version: SCORM 1.2")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#c7d66d')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM Version: 1.2')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("SCORM 1.2")
    elif "2004 3rd Edition" in scorm_version:
        print("SCORM 2004 3rd Edition")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#c7d66d')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM Version: 2004 3rd Edition')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append(scorm_version)
    else:
        print("SCORM  Version: unknown")
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#fe5f55')
        label_scorm.place(x=20, y=20, width=360, height=30)
        text_scorm.set('SCORM Version: unknown')
        # write to excel if multiple files selected
        if multi_files_select: report_data.append(scorm_version)

    # check for multiple items
    if xhelp.checkOneItemOnly(rootnode):
        label_item = tk.Label(root, textvariable=text_item, anchor="w", background='#c7d66d')
        label_item.place(x=20, y=80, width=360, height=30)
        text_item.set("Passed: Only one Item element present.")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Passed: Only one Item element present.")
    else:
        label_item = tk.Label(root, textvariable=text_item, anchor="w", background='#fe5f55')
        label_item.place(x=20, y=80, width=360, height=30)
        text_item.set("FAILED: More than one Item element present!")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("FAILED: More than one Item element present!")

    # check for adlnav namespace in manifest
    if SCORM_2004_4:
        global ns_problem_found
        ns_problem_found = False
        test = rootnode.getAttribute("xmlns:adlnav")
        if test == "":
            ns_problem_found = True
            print("adlnav-namespace NOT found in manifest tag!")
            rootnode.setAttribute("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")
            print("Created namespace entry: " + rootnode.getAttribute("xmlns:adlnav"))

        # check for adlnav presentation in item element
        if xhelp.checkAdlnavPresentation(rootnode):
            pass
        else:
            ns_problem_found = True
            xhelp.adlnavHideElements(domtree)
        if ns_problem_found:
            # write to excel if multiple files selected
            if multi_files_select: report_data.append("WARNING: Namespace was missing - new SCORM package has been created!")

        # save manifest.xml
        saveImsmanifest(rootnode, path + "/imsmanifest.xml")

        # zip scorm package
        os.chdir(path)
        file_paths = sz.retrieve_file_paths('./')
        file_name = os.path.basename(os.path.dirname(path + "/imsmanifest.xml")) + '_SF.zip'
        new_zip_file_path = os.path.join(os.path.dirname(path), file_name)
        sz.zipScorm(file_paths, new_zip_file_path)

        label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w", background='#ffd275')
        label_namespace.place(x=20, y=50, width=360, height=30)
        text_namespace.set("New imsmanifest.xml has been created!")
    else:
        label_namespace = tk.Label(root, textvariable=text_namespace, anchor="w", background='#c7d66d')
        label_namespace.place(x=20, y=50, width=360, height=30)
        text_namespace.set("Passed: Namespace not relevant for this SCORM version.")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Passed: Namespace not relevant for this SCORM version.")

    # check filenames for special characters
    if xhelp.checkSpecialCharsInFileNames(rootnode, (os.path.dirname(path + "/imsmanifest.xml") + '_SPECIAL_CHARACTERS.xlsx')):
        label_characters = tk.Label(root, textvariable=text_characters, anchor="w", background='#c7d66d')
        label_characters.place(x=20, y=110, width=360, height=30)
        text_characters.set("Passed: No special characters in file names.")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Passed: No special characters in file names.")
    else:
        label_characters = tk.Label(root, textvariable=text_characters, anchor="w", background='#fe5f55')
        label_characters.place(x=20, y=110, width=360, height=30)
        text_characters.set("Failed: Special Characters in file names!")
        # write to excel if multiple files selected
        if multi_files_select: report_data.append("Failed: Special Characters in file names!")

    # save Report if multiple files selected
    if multi_files_select:
        report_data.append(os.path.dirname(path + "/imsmanifest.xml") + '_SF.zip')
        we.writeReport(report_path, report_data)

def selectFiles():
    root.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    print(root.filenames)
    if len(root.filenames) == 1:
        runChecks(se.extractScorm(root.filenames[0]))
    # MULTIPLE FILES SELECTED
    elif len(root.filenames) > 1:
        global multi_files_select
        multi_files_select = True
        global report_path
        report_path = os.path.dirname(root.filenames[0])
        we.createReport(report_path)
        for i in root.filenames:
            runChecks(se.extractScorm(i))
            clearLabels()
        text_scorm.set('Multiple files selected - pls. check SCORM-Test-Report.xlsx!')
        label_scorm = tk.Label(root, textvariable=text_scorm, anchor="w", background='#ffd275')
        label_scorm.place(x=20, y=20, width=360, height=30)

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

def clearLabels():
    label_scorm = tk.Label(root, textvariable="", anchor="w")
    label_scorm.place(x=20, y=20, width=360, height=30)
    label_namespace = tk.Label(root, textvariable="", anchor="w")
    label_namespace.place(x=20, y=50, width=360, height=30)
    label_item = tk.Label(root, textvariable="", anchor="w")
    label_item.place(x=20, y=80, width=360, height=30)
    label_characters = tk.Label(root, textvariable="", anchor="w")
    label_characters.place(x=20, y=110, width=360, height=30)
    label_status = tk.Label(root, textvariable="", borderwidth=2, relief="groove", anchor="w")
    label_status.place(x=10, y=170, width=380, height=30)

root.mainloop()
