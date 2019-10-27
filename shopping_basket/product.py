class Product(object):
    """
    Class that defines a product. Each product has a name and a non-negative price
    """
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
