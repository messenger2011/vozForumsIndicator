import re
import urllib.request
from bs4 import BeautifulSoup

class Forum(object):
    def __init__(self, url, title, subForums = []):
        self.url = url
        self.title = title
        self.subForums = subForums

class Link(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title

class VozForums:
    protocol = "https"
    domain = "vozforums.com"
    vozurl = protocol + "://" + domain + "/"
    forum = "forumdisplay.php?f="
    thead = "showthread.php?t="
    ##
    __static_html = ''
    ##
    __forums = []
    __threads = []
    __posts = []
    ##
    @property
    def Forums(self):
        return self.__forums
    def Threads(self):
        return self.__threads
    def Posts(self):
        return self.__posts
    ##
    @classmethod
    def get(self, url):
        req = urllib.request.Request(url=url, method='GET')
        with urllib.request.urlopen(req) as f:
            return self.parseBody(f)

    @classmethod
    def beauti(self, html):
        return BeautifulSoup(html, 'html.parser')

    @classmethod
    def forums(self, f):
        return self.vozurl + self.forum + str(f)

    @classmethod
    def threads(self, t):
        return self.vozurl + self.thread + str(t)
    
    @classmethod
    def link(self, uri):
        return self.vozurl + uri

    @classmethod
    def parseBody(self, response):
        if (response):
            return response.read().decode('utf-8')
    
    @classmethod
    def hasSubForums(self, parser):
        if (parser):
            return len(parser.find_all('td', { "class": "alt1Active" })) > 0
        else:
            return False

    @classmethod
    def extractFid(self, url, fid=None):
        subForums = []
        parser = self.beauti(self.get(self.link(url)))
        e = self.hasSubForums(parser)
        if (e):
            for td in (parser.find_all('td', { "class": "alt1Active" })):
                isSub = len(td.parent.find_all('td', { "class": "alt2" })) > 2
                if (isSub==True):
                    title = "--- " + td.div.a.strong.string
                else:
                    title = td.div.a.strong.string
                subForums.append(Forum(
                    url=self.link(td.div.a.get('href')), 
                    title=title
                ))
        return subForums
    
    @classmethod
    def listForums(self):
        parser = self.beauti(self.get(self.vozurl))
        for td in parser.find_all('td', { "class": "tcat" }):
            fcat = td.find_all('a')
            if (len(fcat) > 1):
                m = re.search('\(\'([^\)]+)\'\)', fcat[0].get('onclick'))
                if m:
                    fid = m.group(1)
                    self.__forums.append(Forum(
                        url=self.link(fcat[1].get('href')), 
                        title=fcat[1].string, 
                        subForums=self.extractFid(url = fcat[1].get('href'), fid = fid)
                    ))
    
    def listThread(self, furl):
        parser = self.beauti(self.get(furl))
        
    def __init__(self):
        self.listForums()
