from lxml import etree
from xml.dom import minidom
import re, os
from xmlHelper import xmlHelper as xh

domtree = minidom.parse('./imsmanifest2.xml')
rootnode = domtree.documentElement


# Check and write adlnav namespace in manifest
try:
    test = rootnode.getAttribute("xmlns:adlnav")
    if test == "":
        print("adlnav-namespace NOT found in manifest tag!")
        rootnode.setAttribute("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")
        print(rootnode.getAttribute("xmlns:adlnav"))
except:
    rootnode.setAttribute("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")
    #print(rootnode.getAttribute("xmlns:adlnav"))

# check filenames for special characters
files_handler = rootnode.getElementsByTagName('file')
print(files_handler)
valid = True
for t in files_handler:
    if t.hasAttribute('href'):
        #print(t.getAttribute('href'))
        if re.match("""^[a-zA-Z0-9_./\-]*$""", t.getAttribute('href')):
            pass
        else:
            valid = False
print("Special characters check: " + str(valid))

# adlnav presentation
try:
    adlnav_pres_handler = rootnode.getElementsByTagName('adlnav:hideLMSUI')
    print('adlnav:')
    print(adlnav_pres_handler[0].firstChild.data)
except:
    print("No adlnav Tags found!")

# create adlnav-element
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

title_element = domtree.getElementsByTagName('title')[1]
#title_element.parentNode.appendChild(adln_presentation)
title_element.parentNode.insertBefore(adln_presentation, title_element)

def prettyfy(doc):
    with open('kwefjkjf.xml', 'w') as f:
        f.write(doc.toprettyxml())
        f.close()
    """domtree = minidom.parseString('kwefjkjf.xml')
    os.remove('kwefjkjf.xml')
    return domtree"""
test = prettyfy(adln_presentation)

# find scorm version
schema_node = rootnode.getElementsByTagName('schemaversion')[0].firstChild.data
print(schema_node)

# save xml to file
with open('ims-test.xml','w') as f:
    f.write(rootnode.toxml())
    #f.write(adln_presentation.toprettyxml())
    f.close()


"""tree = etree.parse('./imsmanifest.xml')
root = tree.getroot()
#print(root.find('organizations', root.nsmap).find('organization', root.nsmap))
ns = root.nsmap"""

# check if only one item in file
def checkOneItemOnly():
    #return True if len(root.findall(".//item", ns)) == 1 else False
    test = rootnode.getElementsByTagName('item')
    print(test)
    print(len(test))

print(checkOneItemOnly())


