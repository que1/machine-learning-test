__author__ = 'admin'

import urllib
from bs4 import BeautifulSoup

class crawler:

    def __init__(self, dbName):
        pass

    def __del__(self):
        pass

    def dbCommit(self):
        pass

    def gententryid(self, table, field, value, createnew = True):
        return None

    def addtoindex(self, url, soup):
        print('Indexing %s' % url)

    def gettextonly(self, soup):
        return None

    def separatewords(self, text):
        return None

    def isindexed(self, url):
        return False

    def addlinkref(self, urlFrom, urlTo, linkText):
        pass

    def crawl(self, pages, depth = 2):
        pass

    def createindextables(self):
        pass


class Test:

    def test(self):
        htmlPage = urllib.request.urlopen('http://news.sohu.com/20170425/n490661298.shtml')
        bsObj = BeautifulSoup(htmlPage.read(), "html5lib")
        print(bsObj.head)

#if __name__ == '__main__':
print('1111')
t = Test()
t.test()


