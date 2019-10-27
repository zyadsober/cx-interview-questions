from custom_exceptions import *
from product import Product


class Catalogue(object):
    """
    Class that defines a catalouge. Each catalouge has a list of products
    """
    def __add_product(self, product):
        """
        Private method to add a product to the catalouge. Checks for duplicates
        before adding the product
        ---
        Params:
            product: Product, the product to add to the catalouge
        ---
        Raises:
            DuplicateProductException
        """
        if product.name in self.products:
            raise DuplicateProductException()
        self.products[product.name] = product

    def __init__(self, products=[]):
        """
        Constructor of the catalougeroduct
        ---
        Params:
            products: list, a list of products
        """
        self.products = dict()
        for product in products:
            self.__add_product(product)

    def add_product(self, product):
        """
        Adds a single product to the catalouge
        ---
        Params:
            Product: Product, the product to add to the catalouge
        """
        self.__add_product(product)

    def add_products(self, products):
        """
        Adds a list of products to the catalouge
        ---
        Params:
            Product: list, the list of products to add to the catalouge
        """
        for product in products:
            self.__add_product(product)

    def remove_product(self, product):
        """
        Removes a single product to the catalouge
        ---
        Params:
            Product: Product, the product to remove from the catalouge
        """
        del self.products[product.name]

    def remove_products(self, products):
        """
        Removes a list of products to the catalouge
        ---
        Params:
            Product: list, the list of products to remove from the catalouge
        """
        for product in products:
            del self.products[product.name]

    def get_product(self, product_name):
        """
        Gets a product from the catalogue based on its name
        ---
        Params:
            product_name: str, the name of the product to return
        ---
        Returns:
            Product, the found product. If not found returns None
        """
        if product_name in self.products:
            return self.products[product_name]
        return None

    def empty(self):
        """
        Clears the list of products in the catalouge
        """
        self.products = []
