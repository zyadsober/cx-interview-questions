from unittest import TestCase
from basket import Basket
from catalogue import Catalogue
from product import Product


class TestBasket(TestCase):

    def setUp(self):
        self.test_products = [
            Product('Baked Beans', 0.99),
            Product('Biscuits', 1.20),
            Product('Sardines', 1.89),
            Product('Shampoo (Small)', 2.00),
            Product('Shampoo (Medium)', 2.50),
            Product('Shampoo (Large)', 3.50),
        ]
        self.test_catalouge = Catalogue(self.test_products)

    def test_construct_basket(self):
        self.test_basket = Basket(self.test_catalouge)
        self.assertEqual(len(self.test_basket.products), 0)
