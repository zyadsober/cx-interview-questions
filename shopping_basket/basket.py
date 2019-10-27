from custom_exceptions import *
from product import Product
from basket_product import BasketProduct

class Basket(object):
    """
    Class that defines a basket. Each basket has a number of products
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

    def __add_product(self, product, quantity):
        """
        Private method to add a product to the basket.
        ---
        Params:
            product: Product, the product to add to the basket
            quantity: int, the quantity of the product to add to the basket
        """
        if not self.__is_product_in_catalogue(product):
            raise ProductNotInCatalogueException()
        if product.name in self.products:
            self.products[product.name].quantity += quantity
        else:
            self.products[product.name] = BasketProduct(product, quantity)

    def __remove_product(self, product, quantity):
        """
        Private method to remove a product from the basket.
        ---
        Params:
            product: Product, the product to add to the basket
            quantity: int, the quantity of the product to remove from the basket
        """
        if product.name in self.products:
            if self.products[product.name].quantity - quantity < 0:
                print('Warning: products cannot have a negative quantity. '
                      'The basket had {} {} when attempted to remove {}.'.format(
                            product.name,
                            self.products[product.name].quantity,
                            quantity
                ))
                self.products[product.name].quantity = 0
            else:
                self.products[product.name].quantity -= quantity
            if self.products[product.name].quantity == 0:
                del self.products[product.name]
        else:
            print('Warning: attempted to remove product {} that does not exist'.format(
                            product.name
            ))

    def __init__(self, catalogue):
        """
        Constructor of the basket
        ---
        Params:
            catalogue: Catalogue, the catalogue associated with the basket
        """
        self.products = dict()
        self.catalogue = catalogue

    def add_product(self, product, quantity=1):
        """
        Adds a single product to the basket
        ---
        Params:
            product: Product, the product to add to the basket
            quantity: int, the quantity of the product to add to the basket
        """
        self.__add_product(product, quantity)

    def remove_product(self, product, quantity=1):
        """
        Removes a single product from the basket
        ---
        Params:
            product: Product, the product to remove from the basket
            quantity: int, the quantity of the product to remove from the basket
        """
        self.__remove_product(product, quantity)

    def empty(self):
        """
        Clears the products in the basket
        """
        self.products = list()
