import xml.dom.minidom
from xml.etree import ElementTree as ET
import requests
import re

# Read xml file
url = "./imsmanifest.xml"
#result = requests.get(url)
#domtree = xml.dom.minidom.parseString(result)
domtree = xml.dom.minidom.parse(url)
rootnode = domtree.documentElement

# 1. Check for special characters
xml_string = open(url)
print("1. Valid! - no special characters found" if re.match("""^[a-zA-Z0-9_=.":/<>?_\-\s]*$""", xml_string.read()) else "1. Invalid!!! - special characters found!")

# 2. Find SCORM Version
scorm_schema = str(rootnode.getElementsByTagName('schemaversion')[0].firstChild.data)
print('2. SCORM-VERSION: ' + scorm_schema)

# 4. Check adlnav-schema in manifest root-tag
adlnav = rootnode.getAttribute('xmlns:adlnav')
if adlnav == "http://www.adlnet.org/xsd/adlnav_v1p3":
    print("3. manifest-attribute adlnav is present! " + adlnav)
else:
    print("3. Missing adlnav schema in manifest! " + adlnav)

# 5. Check adlnav elements in item
adlnav_item = rootnode.getElementsByTagName('adlnav:navigationInterface')
if adlnav_item == []:
    print("4. adlnav tags missing in item tag!")
else:
    print("4. adlnav is present in item: " + str(adlnav_item))

# 6. Add adlnav in manifest attribute
# TODO
# 7. Add adlnav elements in item

# 8. Write new imsmanifest.xml
file_handle = open("ims-test.xml","w")
rootnode.writexml(file_handle)
file_handle.close()

