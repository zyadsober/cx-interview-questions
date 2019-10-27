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
        self.products = list()
        self.catalogue = catalogue


    def add_product(self, product):
        """
        Adds a single product to the basket
        ---
        Params:
            product: Product, the product to add to the basket
        """
        self.products.append(product)

    def remove_product(self, product):
        """
        Removes a single product from the basket
        ---
        Params:
            product: Product, the product to remove from the basket
        """
        for _product in self.products:
            if _product.name == product.name:
                self.products.remove(_product)

    def empty(self):
        """
        Clears the products in the basket
        """
        self.products = list()
