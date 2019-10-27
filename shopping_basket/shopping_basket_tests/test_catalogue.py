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

    def test_construct_catalogue_with_product_lists(self):
        self.test_catalogue = Catalogue(self.test_products)
        self.assertEqual(len(self.test_catalogue.products), len(self.test_products))

    def test_adding_product_to_catalogue(self):
        self.test_catalogue = Catalogue(self.test_products)
        self.test_catalogue.add_product(Product('Additional Product', 1.00))
        self.assertEqual(len(self.test_catalogue.products), len(self.test_products) + 1)

    def test_adding_products_to_catalogue(self):
        self.test_catalogue = Catalogue(self.test_products)
        self.test_catalogue.add_products([
            Product('Additional Product 1', 1.00),
            Product('Additional Product 2', 1.00)
            ]
        )
        self.assertEqual(len(self.test_catalogue.products), len(self.test_products) + 2)

    def test_empty_catalogue(self):
        self.test_catalogue = Catalogue(self.test_products)
        self.test_catalogue.empty()
        self.assertEqual(len(self.test_catalogue.products), 0)
