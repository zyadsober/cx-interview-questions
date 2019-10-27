from unittest import TestCase
from basket import Basket
from product import Product
from catalogue import Catalogue
from offer import BuyAndGetFreeOffer, PercentageOffer, BundleOffer
from utilities import round_half_up


class TestOffer(TestCase):

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

    def test_buy_and_get_free_offer(self):
        """
        Tests the creation of a valid buy and get free offer
        """
        # Baked Beans buy one get one free
        self.test_offer = BuyAndGetFreeOffer(self.test_products[0], 1, 1)
        self.assertEqual(self.test_offer.product, self.test_products[0].name)
        self.assertEqual(self.test_offer.buy_quantity, 1)
        self.assertEqual(self.test_offer.free_quantity, 1)

    def test_buy_and_get_free_offer_discount(self):
        # Baked Beans buy one get one free
        self.test_offer = BuyAndGetFreeOffer(self.test_products[0], 1, 1)
        self.test_basket = Basket(self.test_catalouge)
        self.test_basket.add_product(self.test_products[0], 1)
        self.assertEqual(self.test_offer.get_discount(self.test_basket.products)[0], 0.00)
        # Add 1 more Baked Beans for a total of 2
        self.test_basket.add_product(self.test_products[0], 1)
        self.assertEqual(self.test_offer.get_discount(self.test_basket.products)[0], self.test_products[0].price)

    def test_percentage_offer(self):
        """
        Tests the creation of a valid percentage offer
        """
        # Baked Beans 25% off
        self.test_offer = PercentageOffer(self.test_products[0], 0.25)
        self.assertEqual(self.test_offer.product, self.test_products[0].name)
        self.assertEqual(self.test_offer.discount_percent, 0.25)

    def test_percentage_offer_discount(self):
        # Baked Beans buy one get one free
        self.test_offer = PercentageOffer(self.test_products[0], 0.25)
        self.test_basket = Basket(self.test_catalouge)
        self.assertEqual(self.test_offer.get_discount(self.test_basket.products)[0], 0.00)
        self.test_basket.add_product(self.test_products[0], 1)
        self.assertEqual(self.test_offer.get_discount(
            self.test_basket.products)[0],
            round_half_up(self.test_products[0].price * 0.25, 2)
        )
        # Add 1 more Baked Beans for a total of 2
        self.test_basket.add_product(self.test_products[0], 1)
        self.assertEqual(self.test_offer.get_discount(
            self.test_basket.products)[0],
            round_half_up(self.test_products[0].price * 0.25, 2)
        )

    def test_bundle_offer(self):
        """
        Tests the creation of a valid percentage offer
        """
        # Baked Beans, Biscuits, Sardines
        self.test_offer = BundleOffer([self.test_products[0],
                                           self.test_products[1],
                                           self.test_products[2]
                                          ], 3)
        self.assertEqual(len(self.test_offer.bundle_items), 3)
        self.assertEqual(type(self.test_offer.bundle_items), list)
        self.assertEqual(type(self.test_offer.bundle_items[0]), str)
        self.assertEqual(self.test_offer.required_items, 3)

    def test_bundle_offer_discount(self):
        # Baked Beans, Biscuits, Sardines
        self.test_offer = BundleOffer([self.test_products[0],
                                           self.test_products[1],
                                           self.test_products[2]
                                          ], 3)
        self.test_basket = Basket(self.test_catalouge)
        self.assertEqual(self.test_offer.get_discount(self.test_basket.products)[0], 0.00)
        self.test_basket.add_product(self.test_products[0], 1)
        self.assertEqual(self.test_offer.get_discount(self.test_basket.products)[0], 0.00)
        self.test_basket.add_product(self.test_products[1], 1)
        self.test_basket.add_product(self.test_products[2], 1)
        self.test_basket.add_product(self.test_products[3], 1)
        self.assertEqual(self.test_offer.get_discount(self.test_basket.products)[0], self.test_products[0].price)
        # Add 1 more Baked Beans for a total of 2
        self.test_basket.add_product(self.test_products[0], 1)
        self.assertEqual(self.test_offer.get_discount(self.test_basket.products)[0], self.test_products[0].price)
        # Add 1 more Biscuits for a total of 2
        self.test_basket.add_product(self.test_products[1], 1)
        self.assertEqual(self.test_offer.get_discount(self.test_basket.products)[0], self.test_products[1].price)
