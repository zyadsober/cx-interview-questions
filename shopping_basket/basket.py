from custom_exceptions import *
from product import Product
from basket_product import BasketProduct
from type_validators import validate_type, validate_list_type_and_children_types
from offer import Offer
from utilities import round_half_up


class Basket(object):
    """
    Class that defines a basket. Each basket has a non-negative number of products
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

    def __init__(self, catalogue, offers=[]):
        """
        Constructor of the basket
        ---
        Params:
            catalogue: Catalogue, the catalogue associated with the basket
            offers: list, the list of offers applied to this basket
        """
        validate_list_type_and_children_types(offers, Offer)
        self.products = dict()
        self.catalogue = catalogue
        self.offers = offers[:]

    def add_product(self, product, quantity=1):
        """
        Adds a single product to the basket
        ---
        Params:
            product: Product, the product to add to the basket
            quantity: int, the quantity of the product to add to the basket
        """
        validate_type(product, Product)
        self.__add_product(product, quantity)

    def remove_product(self, product, quantity=1):
        """
        Removes a single product from the basket
        ---
        Params:
            product: Product, the product to remove from the basket
            quantity: int, the quantity of the product to remove from the basket
        """
        validate_type(product, Product)
        self.__remove_product(product, quantity)

    def calculate_subtotal(self):
        """
        Calculates the subtotal for the items currently in the basket
        ---
        Returns:
            float, the subtotal for the items currently in the basket
        """
        subtotal = 0
        for product_name in self.products:
            price = self.products[product_name].product.price
            quantity = self.products[product_name].quantity
            subtotal += price * quantity
        return round_half_up(subtotal, 2)

    def calculate_discount(self):
        """
        Calculates the total discount that applies to the items currently in the basket
        ---
        Returns:
            float, the total discount that applies to the items currently in the basket
        """
        raise NotImplementedError()

    def calculate_total(self):
        """
        Calculates the total that applies to the items currently in the basket after applied discounts
        ---
        Returns:
            float, the total that applies to the items currently in the basket after applied discounts
        """
        return round_half_up(self.calculate_subtotal() - self.calculate_discount(), 2)

    def empty(self):
        """
        Clears the products in the basket
        """
        self.products = dict()
