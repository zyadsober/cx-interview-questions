from product import Product

class Basket(object):
    """
    Class that defines a basket
    """
    def __init__(self, catalogue):
        """
        Constructor of the basket
        ---
        Params:
            catalogue: Catalogue, the catalogue associated with the basket
        """
        self.products = dict()
        self.catalogue = catalogue
