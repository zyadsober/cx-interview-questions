from custom_exceptions import *
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

    def test_negative_pricing(self):
        """
        Tests the case of non-positive pricing on a product
        """
        with self.assertRaises(InvalidProductPriceException):
            Product(self.test_product_name, -1.00)
        with self.assertRaises(InvalidProductPriceException):
            Product(self.test_product_name, -0.01)
        with self.assertRaises(InvalidProductPriceException):
            Product(self.test_product_name, 0)
        with self.assertRaises(InvalidProductPriceException):
            Product(self.test_product_name, 0.00)
        try:
            Product(self.test_product_name, 1.00)
            Product(self.test_product_name, 0.01)
        except InvalidProductPriceException:
            self.fail("InvalidProductPriceException raised for positive value unexpectedly")

    def test_product_change_price(self):
        with self.assertRaises(InvalidProductPriceException):
            self.test_product.price = -1.00
        with self.assertRaises(InvalidProductPriceException):
            self.test_product.price = -0.01
        with self.assertRaises(InvalidProductPriceException):
            self.test_product.price = 0
        with self.assertRaises(InvalidProductPriceException):
            self.test_product.price = 0.00
