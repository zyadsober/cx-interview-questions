from unittest import TestCase
from product import Product


class TestProduct(TestCase):

    def setUp(self):
        self.test_product_name = 'test_product'
        self.test_product_price = 1.00
        self.test_product = Product(self.test_product_name, self.test_product_price)
    def test_product(self):
        """
        Tests the creation of a valid product
        """
        self.assertEqual(self.test_product.name, self.test_product_name)
        self.assertEqual(self.test_product.price, self.test_product_price)
