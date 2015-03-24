import os
from .amzn import AmazonWishlist, AmazonItem


class Ocelot:
    amazon_url = 'http://www.amazon.com'

    def __init__(self, save_cfg, omniv_api):
        self.savepath = save_cfg['dir']
        self.saveext = save_cfg['ext']
        AmazonItem.omniv_api = omniv_api
        self.wlists = {}

    def load_wishlist(self, wishlist_id):
        filepath = self.savepath + '/' + wishlist_id + self.saveext
        if os.path.isfile(filepath):
            wishlist = AmazonWishlist(id=wishlist_id, filepath=filepath)
            self.wlists.update({wishlist_id: wishlist})
        else:
            self.add_wishlist(wishlist_id)

    def add_wishlist(self, wishlist_id):
        wishlist = AmazonWishlist(id=wishlist_id)
        self.wlists.update({wishlist_id: wishlist})

    def save(self):
        for k, v in self.wlists.items():
            v.savejson(self.savepath)

    def print_wishlist(self, listID):
        print(self.wlists[listID])