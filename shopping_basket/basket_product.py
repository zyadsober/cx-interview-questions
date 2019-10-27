from product import Product


class BasketProduct(object):
    """
    Class that defines a product in a basket. Each basket product has a product
    object and a non-negative quantity
    """
    def __init__(self, product, quantity=1):
        """
        Constructor of the basket
        ---
        Params:
            product: Product, the basket product object
            quantity: int, the initial quantity of the product in the basket
        """
        self.product = product
        self.quantity = quantity
