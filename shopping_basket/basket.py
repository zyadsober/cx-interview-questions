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
    @staticmethod
    def get_basket_products_copy(basket_products):
        """
        Private Static method that takes returns a copy of a dict of BasketProducts
        ---
        Params:
            basket_products: dict, the dictionary of basket products to copy
        ---
        Returns:
            dict, the copy of the basket products
        """
        validate_type(basket_products, dict)
        basket_products_copy = dict()
        for product in basket_products:
            basket_products_copy[product] = BasketProduct.get_copy(basket_products[product])
        return basket_products_copy
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

    def __search_best_offer(self, offers, products_for_discount):
        """
        Search for the best offer recursively in a depth first search
        ---
        Params:
            offers: list, the offers that apply to the search
            products_for_discount: dict, the products available to choose offers for
                at this recursion level
        ---
        Returns:
            int, the best discount from this level of recursion
            list, the products used in the combination of offers chosen
        """
        best_discount = 0
        best_products_used = dict()
        for offer in self.offers:
            # Deep copy
            this_offer_products_for_discount = Basket.get_basket_products_copy(products_for_discount)
            next_discount, products_used = offer.get_discount(this_offer_products_for_discount)
            for product_used_name in products_used:
                product_used_quanitity = products_used[product_used_name]
                this_offer_products_for_discount[product_used_name].quantity -= product_used_quanitity
                if this_offer_products_for_discount[product_used_name].quantity == 0:
                    del this_offer_products_for_discount[product_used_name]
            child_discount = 0
            # Base case
            if next_discount != 0:
                child_discount, child_discount_products_used = self.__search_best_offer(offers, this_offer_products_for_discount)
                for child_discount_product in child_discount_products_used:
                    if child_discount_product in products_used:
                        products_used[child_discount_product] += child_discount_products_used[child_discount_product]
                    else:
                        products_used[child_discount_product] = child_discount_products_used[child_discount_product]
            if child_discount + next_discount > best_discount:
                best_discount = child_discount + next_discount
                best_products_used = products_used
        return best_discount, best_products_used

    def calculate_discount(self):
        """
        Calculates the total discount that applies to the items currently in the basket
        ---
        Returns:
            float, the total discount that applies to the items currently in the basket
        """
        products_for_discount = Basket.get_basket_products_copy(self.products)
        best_discount, best_products_used = self.__search_best_offer(self.offers, products_for_discount)
        return round_half_up(best_discount, 2)

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
