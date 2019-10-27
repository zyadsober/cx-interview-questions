from custom_exceptions import *
from type_validators import validate_type


class Product(object):
    """
    Class that defines a product. Each product has a name and a non-negative price
    """

    @staticmethod
    def get_copy(product):
        """
        Static method that takes returns a copy of the supplied Product
        ---
        Params:
            product: BasketProduct, the product to copy
        ---
        Returns:
            Product, the copy of the product
        """
        validate_type(product, Product)
        return Product(product.name, product.price)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        # Raise an exception if the price is not positive
        Product.__validate_price(value)
        self._price = value

    @staticmethod
    def __validate_price(price):
        """
        Static method that validates that the price of the product is valid.
        A valid product must have a non-negative price
        ---
        Params:
            price: float, the product's price to validate
        ---
        Raises:
            InvalidProductPriceException
        """
        if price <= 0.00:
            raise InvalidProductPriceException()

    def __init__(self, name, price):
        """
        Constructor of the product
        ---
        Params:
            name: str, the name of the product
            price: float, the price of the product
        """
        self.name = name
        self.price = price

    def __repr__(self):
        return str('{} - £{:.2f}'.format(self.name, round_half_up(self.price,2)))
