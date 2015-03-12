from config import saves, omniv_api
from ocelot.ocelot import Ocelot

def test():
    app = Ocelot(saves, omniv_api)
    app.load_wishlist('1XXG8EJLHDMNV')
    app.save()

