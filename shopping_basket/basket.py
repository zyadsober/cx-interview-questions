from custom_exceptions import *
from product import Product

class Basket(object):
    """
    Class that defines a basket
    """
    def __is_product_in_catalogue(self, product):
        """
        private method to check if the given product exists in the basket's catalogue
        ---
        Params:
            product: Product, the product to check it's existence
        ---
        Returns:
            bool, indication whether the product exists in the basket's catalogue
        """
        if self.catalogue.get_product(product.name):
            return True
        return False

    def __add_product(self, product):
        """
        Private method to add a product to the basket.
        ---
        Params:
            product: Product, the product to add to the basket
        """
        if not self.__is_product_in_catalogue(product):
            raise ProductNotInCatalogueException()
        self.products.append(product)

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
        self.__add_product(product)

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
