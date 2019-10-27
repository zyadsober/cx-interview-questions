from product import Product
from type_validators import validate_type, validate_list_type_and_children_types


class BasketProduct(object):
    """
    Class that defines a product in a basket. Each basket product has a product
    object and a non-negative quantity
    """
    @staticmethod
    def get_copy(basket_product):
        """
        Static method that takes returns a copy of the supplied BasketProduct
        ---
        Params:
            basket_product: BasketProduct, the basket product to copy
        ---
        Returns:
            BaksetProduct, the copy of the basket product
        """
        validate_type(basket_product, BasketProduct)
        return BasketProduct(Product.get_copy(basket_product.product), basket_product.quantity)

    def __init__(self, product, quantity=1):
        """
        Constructor of the basket
        ---
        Params:
            product: Product, the basket product object
            quantity: int, the initial quantity of the product in the basket
        """
        validate_type(product, Product)

        self.product = product
        self.quantity = quantity
