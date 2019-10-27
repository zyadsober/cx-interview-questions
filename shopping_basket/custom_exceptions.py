"""
Contains custom exceptions for invalid operations or assertions
"""

class InvalidProductPriceException(Exception):
    def __init__(self):
        """
        Implements an exception type for invalid pricing of product
        """
        Exception.__init__(
            self,
            "Product prices must be greater than zero"
        )

class DuplicateProductException(Exception):
    def __init__(self):
        """
        Implements an exception type for the duplication of a product
        """
        Exception.__init__(
            self,
            "A catalouge must not contain two of the same product"
        )

class ProductNotInCatalogueException(Exception):
    def __init__(self):
        """
        Implements an exception type for when a product is added to a basket
        but does not exist in it's catalogue
        """
        Exception.__init__(
            self,
            "The product must exist in the catalogue to add it to the basket"
        )
