# -*- coding: utf8 -*-

__author__ = 'admin'

from urllib import request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sqlite3
import re


# Create a list of words to ignore
ignorewords={'the':1,'of':1,'to':1,'and':1,'a':1,'in':1,'is':1,'it':1}

class crawler:

    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getentryid(self, table, field, value, createnew = True):
        cur = self.con.execute("select rowid from %s where %s = '%s'" % (table, field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute("insert into %s(%s) values('%s')" % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]

    def addtoindex(self, url, soup):
        if (self.isindexed(url)):
            return
        print('Indexing %s' % url)

        text = self.gettextonly(soup)
        words = self.separatewords(text)

        urlid = self.getentryid("urllist", "url", url)

        for i in range(len(words)):
            word = words[i]
            if (word in ignorewords):
                continue
            wordid = self.getentryid("wordlist", "word", word)
            self.con.execute("insert into wordlocation(urlid, wordid, location) values(%d, %d, %d)" % (urlid, wordid, i))

    # Extract the text from an HTML page (no tags)
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    def isindexed(self, url):
        u = self.con.execute("select rowid from urllist where url = '%s'" % url).fetchone()
        if u != None:
            v = self.con.execute("select * from wordlocation where urlid = %d" % u[0]).fetchone()
            if v != None:
                return True
        return False

    def addlinkref(self, urlFrom, urlTo, linkText):
        pass

    def crawl(self, pages, depth = 2):
        for i in range(depth):
            newpages = {}
            for page in pages:
                try:
                    c = request.urlopen(page)
                except:
                    print("Could not open %s" % page)
                    continue
                try:
                    soup = BeautifulSoup(c.read(), "html5lib")
                    self.addtoindex(page, soup)

                    links = soup("a")
                    for link in links:
                        if ('href' in dict(link.attrs)):
                            url = urljoin(page, link['href'])
                            if url.find("'") != -1: continue
                            url = url.split('#')[0]  # remove location portion
                            if url[0:4] == 'http' and not self.isindexed(url):
                                newpages[url] = 1
                            linkText = self.gettextonly(link)
                            self.addlinkref(page, url, linkText)

                    self.dbcommit()
                except Exception as e:
                    print("Could not parse page %s" % page)
                    print(e)

            pages = newpages

    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()


class searcher:
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self, q):
        # Strings to build the query
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []

        # Split the words by spaces
        words = q.split(' ')
        tablenumber = 0

        for word in words:
            # Get the word ID
            wordrow = self.con.execute("select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber - 1, tablenumber)
                fieldlist += ',w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' % tablenumber
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1

        # Create the query from the separate parts
        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        print(fullquery)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]

        return rows, wordids


    def getscoredlist(self, rows, wordids):
        totalscores = dict([(row[0], 0) for row in rows])

        # This is where we'll put our scoring functions
        '''
        weights = [(1.0, self.locationscore(rows)),
                   (1.0, self.frequencyscore(rows)),
                   (1.0, self.pagerankscore(rows)),
                   (1.0, self.linktextscore(rows, wordids)),
                   (5.0, self.nnscore(rows, wordids))]
        '''
        weights = []
        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url] += weight * scores[url]

        return totalscores


    def geturlname(self, id):
        return self.con.execute("select url from urllist where rowid = %d" % id).fetchone()[0]


    def query(self, q):
        rows, wordids = self.getmatchrows(q)
        scores = self.getscoredlist(rows, wordids)
        rankedscores = [(score, url) for (url, score) in scores.items()]
        rankedscores.sort()
        rankedscores.reverse()
        for (score, urlid) in rankedscores[0:10]:
            print('%f\t%s' % (score,self.geturlname(urlid)))
        return wordids, [r[1] for r in rankedscores[0:10]]


class Test:

    def test(self):
        '''
        html = request.urlopen("http://bj.lianjia.com/xiaoqu/pg1")
        bsObj = BeautifulSoup(html.read(), "html5lib")
        print(bsObj.head)
        '''
        pagelist = ["https://www.cnblogs.com/lxlx1798/articles/6807782.html"]
        #crawler1 = crawler("searchindex.db")
        #crawler1.createindextables()
        #crawler1.crawl(pagelist)

        searcher1 = searcher("chapter4/searchindex.db")
        #rows, wordids = searcher1.getmatchrows('false self')
        #print(rows)
        #print(wordids)
        wordids, scores = searcher1.query("false self")
        print(wordids)
        print(scores)


if __name__ == '__main__':
    t = Test()
    t.test()


