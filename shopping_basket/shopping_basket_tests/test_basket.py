from custom_exceptions import *
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

    def test_construct_basket_with_product_lists(self):
        self.test_basket = Basket(self.test_catalouge)
        for product in self.test_products:
            self.test_basket.add_product(product)
        self.assertEqual(len(self.test_basket.products), len(self.test_products))

    def test_add_product_to_basket(self):
        self.test_basket = Basket(self.test_catalouge)
        self.test_basket.add_product(self.test_products[0])
        self.assertEqual(len(self.test_basket.products), 1)

    def test_add_multi_product_to_basket(self):
        self.test_basket = Basket(self.test_catalouge)
        self.test_basket.add_product(self.test_products[0])
        self.test_basket.add_product(self.test_products[0])
        self.assertEqual(len(self.test_basket.products), 2)

    def test_add_product_not_in_catalogue_to_basket(self):
        self.test_basket = Basket(self.test_catalouge)
        with self.assertRaises(ProductNotInCatalogueException):
            self.test_basket.add_product(Product('Dummy Product', 1.00))

    def test_removing_product_from_basket(self):
        self.test_basket = Basket(self.test_catalouge)
        for product in self.test_products:
            self.test_basket.add_product(product)
        self.test_basket.remove_product(self.test_products[0])
        self.assertEqual(len(self.test_basket.products), len(self.test_products) - 1)
        self.assertEqual(self.test_products[0].name in self.test_basket.products, False)

    def test_empty_basket(self):
        self.test_basket = Basket(self.test_catalouge)
        for product in self.test_products:
            self.test_basket.add_product(product)
        self.assertEqual(len(self.test_basket.products), len(self.test_products))
        self.test_basket.empty()
        self.assertEqual(len(self.test_basket.products), 0)
