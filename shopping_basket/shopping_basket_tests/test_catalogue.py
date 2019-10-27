from unittest import TestCase
from catalogue import Catalogue
from product import Product


class TestCatalogue(TestCase):

    def setUp(self):
        self.test_products = [
            Product('Baked Beans', 0.99),
            Product('Biscuits', 1.20),
            Product('Sardines', 1.89),
            Product('Shampoo (Small)', 2.00),
            Product('Shampoo (Medium)', 2.50),
            Product('Shampoo (Large)', 3.50),
        ]

    def test_construct_empty_catalogue(self):
        self.test_catalogue = Catalogue()
        self.assertEqual(len(self.test_catalogue.products), 0)
        self.test_catalogue = Catalogue([])
        self.assertEqual(len(self.test_catalogue.products), 0)
