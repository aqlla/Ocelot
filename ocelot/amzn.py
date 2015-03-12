import re
import json
import codecs
import requests
from bs4 import BeautifulSoup
from ocelot.beautifulladel import BeautifulLadel

class AmazonWishlist:
    base_url = 'http://www.amazon.com/gp/registry/wishlist'

    def __init__(self, id=None, filepath=None):
        self.id = id
        self.filepath = filepath
        self.items = {}

        if filepath is None:
            self.url = AmazonWishlist.getURL(id)
            self.getitems()
        else:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.url = data['url']
                    for k, v in data['items'].items():
                        self.items.update({k: AmazonItem(self.id, id=k, price=v['price'], name=v['name'], url=v['link'])})
            except IOError as e:
                print(e)


    def getitems(self):
        ladel = BeautifulLadel(self.url)
        items_soup = ladel.getElements(selector=re.compile('^itemInfo_'), sel_type='id')
        for i in items_soup:
            item = AmazonItem(self.id, soup=i)
            self.items.update({item.id: item})


    def savejson(self, path):
        try:
            with codecs.open(path+'/'+self.id+'.json', 'w', encoding="utf-8") as file:
                json_data = json.dump(self.getdata(), fp=file, indent=4, ensure_ascii=False)
        except IOError as e:
            print(e)


    def getdata(self):
        item_data = { v.id : v.getdata() for (k, v) in self.items.items() }
        return {
            'url': self.url,
            'items': item_data
        }


    @classmethod
    def getURL(cls, id):
        return cls.base_url + '/' + id


    def __str__(self):
        string = 'ID: ' + self.id \
                 + '\nURL: ' + self.url \
                 + '\nItems:\n'
        for k, v in self.items.items():
            string += str(v)
        return string


class AmazonItem:
    omniv_api = dict()

    def __init__(self, wishlist, id=None, soup=None, price=[], name=None, url=None):
        self.id = id
        self.url = url
        self.name = name
        self.price = price
        self.wishlist = wishlist
        self.wlist_url = AmazonWishlist.getURL(wishlist)
        self.ladel = BeautifulLadel(self.wlist_url, soup=soup)

        if id is None:
            self.id = soup['id'][len('itemInfo_'):]
            itemNameElement  = soup.find_all(attrs={ 'id': 'itemName_' +self.id })[0]
            self.name = itemNameElement.contents[0].strip()
            self.url = itemNameElement['href']

        self.getprice(ladel=self.ladel)

    def getprice(self, ladel=None):
        self.ladel = BeautifulLadel(self.wlist_url) if ladel is None else ladel
        newprice = self.ladel.getElements(selector='itemPrice_'+self.id, sel_type='id')[0].contents[0].strip()
        pricef = float(newprice[1:])

        if len(self.price) == 0 or pricef != self.price[-1]:
            message = 'Price of ' + self.name + ' changed from ' + str(self.price[-1]) + ' to ' + str(pricef)
            url = 'http://www.amazon.com/' + self.url
            self.sendburst(message, url=url)
            self.price.append(pricef)



    def getdata(self):
        return {
            'name': self.name,
            'link': self.url,
            'price': self.price
        }

    def sendburst(self, message, url=None):
        access_token = AmazonItem.omniv_api['access_token']
        burst_url = AmazonItem.omniv_api['burst url']

        req = requests.post(burst_url, {
            'access_token': access_token,
            'sender'      : 'Amzn Ocelot',
            'recipient'	  : 'aquilleph',
            'message'     : message,
            'url'         : url
        }, verify=True)

    def __str__(self):
        return "ID: " + self.id \
               + "\nName: " + self.name \
               + "\nLink: " + self.url \
               + "\nPrice: " + str(self.price) + "\n"