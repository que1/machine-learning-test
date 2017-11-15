__author__ = 'admin'

# encoding=utf8

from html.parser import HTMLParser

class MyHtmlParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if data.count('\n') == 0:
            self.data.append(data)


htmlFile = open(r"C:\Users\yidongyun\Downloads\1111.html", 'r', encoding = 'UTF-8')
content = htmlFile.read()

myHtmlParser = MyHtmlParser()
myHtmlParser.feed(content)

for item in myHtmlParser.data:
    print(item)
