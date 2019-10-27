from product import Product


class Catalogue(object):
    """
    Class that defines a catalouge. Each catalouge has a list of products
    """
    def __init__(self, products=[]):
        """
        Constructor of the catalougeroduct
        ---
        Params:
            products: list, a list of products
        """
        self.products = products[:]


    def add_product(self, product):
        """
        Adds a single product to the catalouge
        ---
        Params:
            Product: Product, the product to add to the catalouge
        """
        self.products.append(product)

    def add_products(self, products):
        """
        Adds a list of products to the catalouge
        ---
        Params:
            Product: list, the list of products to add to the catalouge
        """
        for product in products:
            self.products.append(product)


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
        for product in self.products:
            if product.name == product_name:
                return product
        return None

    def empty(self):
        """
        Clears the list of products in the catalouge
        """
        self.products = []
