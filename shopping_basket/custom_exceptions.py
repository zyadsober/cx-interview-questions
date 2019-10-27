"""
Contains custom exceptions for invalid operations or assertions
"""

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
