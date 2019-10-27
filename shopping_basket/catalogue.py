from product import Product


class Catalogue(object):
    """
    Class that defines a catalouge. Each catalouge has a list of products
    """
    def __init__(self, products=[]):
        """
        Constructor of the catalougeroduct
        ---
        Params:
            products: list, a list of products
        """
        self.products = products
