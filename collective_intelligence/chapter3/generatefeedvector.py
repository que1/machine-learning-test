import feedparser
import re

def getwordcounts(url):
    # Parse the feed
    d=feedparser.parse(url)
    wc={}

    # Loop over all the entries
    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description

        # Extract a list of words
        words=getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
    return d.feed.title, wc

def getwords(html):
    # Remove all the HTML tagsgit config --global user.email "you@example.com"
    txt = re.compile(r'<[^>]+>').sub('',html)

    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word!='']

if __name__ == '__main__':
    apcount = {}
    wordcounts = {}

    feedlist = ["http://blog.csdn.net/xiaoquantouer/rss/list",
                "http://blog.csdn.net/sunhuaqiang1/rss/list",
                "http://blog.csdn.net/rickiyeat/rss/list",
                "http://blog.csdn.net/qq_40027052/rss/list",
                "http://blog.csdn.net/Leafage_M/article/rss/list",
                "http://blog.csdn.net/huojiao2006/rss/list",
                "http://blog.csdn.net/LEoe_/rss/list",
                "http://blog.csdn.net/fullbug/rss/list",
                "feed://blog.csdn.net/FungLeo/article/rss/list",
                "feed://blog.csdn.net/oopsoom/rss/list"]

    for feedurl in feedlist:
        title, wc = getwordcounts(feedurl)
        wordcounts[title] = wc
        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1

    print(wordcounts)
    print(apcount)

    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc)/len(feedlist)
        if frac > 0.1 and frac < 0.5:
            wordlist.append(w)
    print(wordlist)

    out = open('blogdata.txt', 'w')
    out.write("Blog")
    
    for word in wordlist:
        out.write("\t%s" % word)
    out.write("\n")

    mytitle = 1;
    for blog, wc in wordcounts.items():
        out.write("a" + str(mytitle))
        mytitle += 1
        for word in wordlist:
            if word in wc:
                out.write("\t%s" % wc[word])
            else:
                out.write("\t0")
        out.write("\n")

    out.close()
