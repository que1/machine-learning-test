__author__ = 'admin'

# -*- coding:utf-8 -*-

from xml.dom import minidom
from xml.etree import ElementTree

class XmlParser:
    def __init__(self):
        pass

    def xmlData(self, xmlStr):
        doc = minidom.parseString(xmlStr)
        root = doc.documentElement

        spanList = root.getElementsByTagName("span")
        for span in spanList:
            id = span.getAttribute("id")
            print(id)
            value = span.childNodes[0].data
            print(value)

xmlStr = "<div><span id=\"1\">abc1</span><span id=\"2\">abc2</span></div>"
xmlParser = XmlParser()
xmlParser.xmlData(xmlStr)



