from lxml import etree
from xml.dom import minidom

domtree = minidom.parse('./imsmanifest2.xml')
rootnode = domtree.documentElement
rootnode.setAttribute("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")
print(rootnode.getAttribute("xmlns:adlnav"))
with open('ims-test.xml','w') as f:
    f.write(rootnode.toxml())
    f.close()


tree = etree.parse('./imsmanifest.xml')
root = tree.getroot()
#print(root.find('organizations', root.nsmap).find('organization', root.nsmap))
ns = root.nsmap


#root.set("xmlns:adlnav", "http://www.adlnet.org/xsd/adlnav_v1p3")

#print(root.tag)
#print(root.attrib)
#xmlstr = etree.tostring(root, encoding='utf8', method='xml')
#print(xmlstr)

def checkOneItemOnly():
    return True if len(root.findall(".//true", ns)) == 1 else False

print(checkOneItemOnly())
