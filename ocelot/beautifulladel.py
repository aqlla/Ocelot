from bs4 import BeautifulSoup
import urllib.request as urlreq
import urllib.parse as urlparse
from urllib.error import URLError, HTTPError


class BeautifulLadel:
    def __init__(self, url, soup=None):
        self.prev = []
        self.next = []
        self.setpage(url, soup=soup)


    def setpage(self, url, soup=None):
        self.url = url
        self.soup = self.getsoup(url) if soup is None else soup


    def getElements(self, selector=None, sel_type=None, tag='div'):
        elements = self.soup.find_all(attrs={sel_type: selector})
        return elements


    def goback(self):
        self.next.append(self.url)
        prev = self.prev.pop()
        self.setpage(prev)


    def goforward(self):
        self.prev.append(self.url)
        next = self.next.pop()
        self.setpage(next)


    def goto(self, url):
        self.prev.append(self.url)
        self.next = []
        self.setpage(url)


    def getsoup(self, url):
        try:
            res = urlreq.urlopen(urlreq.Request(url))
        except HTTPError as e:
            print('Server could not fulfill request.')
            print('Error code: ', e.code)
            return None
        except URLError as e:
            print('Failed to reach the server.')
            print('Reason: ', e.reason)
            return None
        else:
            return BeautifulSoup(res.read())


    @classmethod
    def pprint(cls, item):
        for i in item:
            print(i.prettify())


    def __str__(self):
        return self.soup.prettify()

