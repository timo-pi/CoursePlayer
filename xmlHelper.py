from xml.dom import minidom
import os, re
import xlsxwriter
import writeExcel as we

class xmlHelper:

    # Check for special characters (not safe - do not use)
    def checkSpecialCharsGlobal(url):
        xml_string = open(url)
        print("1. Valid! - no special characters found" if re.match("""^[a-zA-Z0-9_=.":/<>?_\-\s]*$""", xml_string.read()) else "1. Invalid!!! - special characters found!")

    """ 
    # Check and write adlnav namespace in manifest
    def adlnavManifestCheck(rootnode):
        try:
            test = rootnode.getAttribute("xmlns:adlnav")
            if test == "":
                print("adlnav-namespace NOT found in manifest tag!")
                rootnode.setAttribute("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")
                print("Created namespace entry: " + rootnode.getAttribute("xmlns:adlnav"))
            return rootnode
        except:
            rootnode.setAttribute("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")
            print("Created namespace entry: " + rootnode.getAttribute("xmlns:adlnav"))
            return rootnode"""

    # Check if only one Item present
    def checkOneItemOnly(rootnode):
        return True if len(rootnode.getElementsByTagName('item')) == 1 else False

    # check filenames for special characters
    def checkSpecialCharsInFileNames(rootnode, path):
        files_handler = rootnode.getElementsByTagName('file')
        report_data = []
        isValid = True
        for t in files_handler:
            if t.hasAttribute('href'):
                # print(t.getAttribute('href'))
                if re.match("""^[a-zA-Z0-9_./\-]*$""", t.getAttribute('href')):
                    pass
                else:
                    isValid = False
                    print("Invalid Special Character in " + str(t.getAttribute('href')))
                    report_data.append('<file href="' + str(t.getAttribute('href')) + '" />')

        if len(report_data) > 0:
            we.createItemsReport(path, report_data)
        return isValid

    # check if adlnav presentation element is already present
    def checkAdlnavPresentation(rootnode):
        try:
            adlnav_pres_handler = rootnode.getElementsByTagName('adlnav:hideLMSUI')
            #print(len(adlnav_pres_handler))
            if len(adlnav_pres_handler) < 1:
                return False
            else:
                return True
        except:
            return False

    # create adlnav presentation element
    def adlnavHideElements(domtree):
        adln_presentation = domtree.createElement('adlnav:presentation')
        adln_navigation = adln_presentation.appendChild(domtree.createElement('adlnav:navigationInterface'))
        hide_continue = domtree.createElement('adlnav:hideLMSUI')
        hide_continue.appendChild(domtree.createTextNode('continue'))
        hide_previous = domtree.createElement('adlnav:hideLMSUI')
        hide_previous.appendChild(domtree.createTextNode('previous'))
        hide_exit = domtree.createElement('adlnav:hideLMSUI')
        hide_exit.appendChild(domtree.createTextNode('exit'))
        hide_exitAll = domtree.createElement('adlnav:hideLMSUI')
        hide_exitAll.appendChild(domtree.createTextNode('exitAll'))
        hide_suspendAll = domtree.createElement('adlnav:hideLMSUI')
        hide_suspendAll.appendChild(domtree.createTextNode('suspendAll'))
        hide_abandonAll = domtree.createElement('adlnav:hideLMSUI')
        hide_abandonAll.appendChild(domtree.createTextNode('abandonAll'))
        adln_navigation.appendChild(hide_continue)
        adln_navigation.appendChild(hide_previous)
        adln_navigation.appendChild(hide_exit)
        adln_navigation.appendChild(hide_exitAll)
        adln_navigation.appendChild(hide_suspendAll)
        adln_navigation.appendChild(hide_abandonAll)
        adln_presentation.appendChild(adln_navigation)

        # Append to domtree
        title_element = domtree.getElementsByTagName('title')[1]
        # title_element.parentNode.appendChild(adln_presentation)
        title_element.parentNode.insertBefore(adln_presentation, title_element)
        return domtree

    # check scorm version
    def checkScormVersion(rootnode):
        schema_node = rootnode.getElementsByTagName('schemaversion')[0].firstChild.data
        return schema_node

    def createExcelReport(path, data):
        workbook = xlsxwriter.Workbook('hello.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write('A1', 'Hello world')

        workbook.close()