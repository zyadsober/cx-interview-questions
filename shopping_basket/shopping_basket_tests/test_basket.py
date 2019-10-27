from custom_exceptions import *
from unittest import TestCase
from basket import Basket
from catalogue import Catalogue
from product import Product
from offer import BuyAndGetFreeOffer, PercentageOffer, BundleOffer
from utilities import round_half_up


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
        self.assertEqual(self.test_basket.products[self.test_products[0].name].quantity, 1)

    def test_add_multi_product_to_basket(self):
        self.test_basket = Basket(self.test_catalouge)
        self.test_basket.add_product(self.test_products[0])
        self.test_basket.add_product(self.test_products[0])
        self.assertEqual(len(self.test_basket.products), 1)
        self.assertEqual(self.test_basket.products[self.test_products[0].name].quantity, 2)

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

    def test_basket_subtotal(self):
        # One of each item
        self.test_basket = Basket(self.test_catalouge)
        for product in self.test_products:
            self.test_basket.add_product(product)
        self.assertEqual(self.test_basket.calculate_subtotal(), 12.08)

        self.test_basket.empty()

        # 4 Baked Beans and 1 Biscuits
        # Add 4 Baked Beans
        self.test_basket.add_product(self.test_products[0], 4)
        # Add 1 Biscuits
        self.test_basket.add_product(self.test_products[1])
        self.assertEqual(self.test_basket.calculate_subtotal(), 5.16)

        self.test_basket.empty()

        # With Sardines 25% discount
        self.test_basket = Basket(self.test_catalouge)
        # Add 2 Baked Beans
        self.test_basket.add_product(self.test_products[0], 2)
        # Add 1 Biscuits
        self.test_basket.add_product(self.test_products[1])
        # Add 2 Sardines
        self.test_basket.add_product(self.test_products[2], 2)
        self.assertEqual(self.test_basket.calculate_subtotal(), 6.96)

    def test_basket_discount_buy_2_get_1_free(self):
        # With Baked Beans buy 2 get 1 free
        self.buy_and_get_free_offer = BuyAndGetFreeOffer(self.test_products[0], 2, 1)
        self.test_basket = Basket(self.test_catalouge, [self.buy_and_get_free_offer])
        # Add 4 Baked Beans
        self.test_basket.add_product(self.test_products[0], 4)
        # Add 1 Biscuits
        self.test_basket.add_product(self.test_products[1])
        self.assertEqual(self.test_basket.calculate_discount(), 0.99)
        # Add 4 Baked Beans
        self.test_basket.add_product(self.test_products[0], 4)
        self.assertEqual(self.test_basket.calculate_discount(), 1.98)
        self.assertEqual(self.test_basket.calculate_total(),
                         round_half_up(self.test_products[0].price * 8 +
                         self.test_products[1].price -
                         self.test_basket.calculate_discount(), 2))

    def test_basket_discount_percent_offer(self):
        # With Sardines 25% discount
        self.percentage_offer = PercentageOffer(self.test_products[2], 0.25)
        self.test_basket = Basket(self.test_catalouge, [self.percentage_offer])
        # Add 2 Baked Beans
        self.test_basket.add_product(self.test_products[0], 2)
        # Add 1 Biscuits
        self.test_basket.add_product(self.test_products[1])
        # Add 2 Sardines
        self.test_basket.add_product(self.test_products[2], 2)
        self.assertEqual(self.test_basket.calculate_discount(), 2 * round_half_up(self.test_products[2].price * 0.25, 2))
        self.assertEqual(self.test_basket.calculate_total(),
                         round_half_up(self.test_products[0].price * 2 +
                         self.test_products[1].price +
                         self.test_products[2].price * 2 -
                         self.test_basket.calculate_discount(), 2))

    def test_basket_discount_percent_and_buy_2_get_1_free_offers(self):
        # With Baked Beans buy 2 get 1 free and 25% discount
        self.buy_and_get_free_offer = BuyAndGetFreeOffer(self.test_products[0], 2, 1)
        self.percentage_offer = PercentageOffer(self.test_products[0], 0.25)
        self.test_basket = Basket(self.test_catalouge, [self.buy_and_get_free_offer, self.percentage_offer])
        # Add 4 Baked Beans
        self.test_basket.add_product(self.test_products[0], 4)
        # Add 1 Biscuits
        self.test_basket.add_product(self.test_products[1])
        # Baked Beans Buy 2 get one free: 0.99
        # Baked Beans 25% percent discount: 0.99 * 0.25 =  0.25
        # Total: 0.99 + 0.25 = 1.24
        self.assertEqual(self.test_basket.calculate_discount(), 1.24)
        self.assertEqual(self.test_basket.calculate_total(),
                         round_half_up(self.test_products[0].price * 4 +
                         self.test_products[1].price -
                         self.test_basket.calculate_discount(), 2))
        # Add 4 Baked Beans
        self.test_basket.add_product(self.test_products[0], 4)
        # Buy 2 get 1 free twice: 0.99 * 2 = 1.98
        # Percentage discount on remaining 2: 0.99 * 0.25 * 2 = 0.50
        # total: 1.98 + 0.50 = 2.48
        self.assertEqual(self.test_basket.calculate_discount(), 2.48)
        self.assertEqual(self.test_basket.calculate_total(),
                         round_half_up(self.test_products[0].price * 8 +
                         self.test_products[1].price -
                         self.test_basket.calculate_discount(), 2))

        # With Baked Beans buy 2 get 1 free and 50% discount
        self.buy_and_get_free_offer = BuyAndGetFreeOffer(self.test_products[0], 2, 1)
        self.percentage_offer = PercentageOffer(self.test_products[0], 0.50)
        self.test_basket = Basket(self.test_catalouge, [self.buy_and_get_free_offer, self.percentage_offer])
        # Add 4 Baked Beans
        self.test_basket.add_product(self.test_products[0], 4)
        # Add 1 Biscuits
        self.test_basket.add_product(self.test_products[1])
        # Baked Beans Buy 2 get one free: 0
        # Baked Beans 50% percent discount: 0.99 * 0.5 = 2.00
        # Total: 2.00
        self.assertEqual(self.test_basket.calculate_discount(), 2.00)
        self.assertEqual(self.test_basket.calculate_total(),
                         round_half_up(self.test_products[0].price * 4 +
                         self.test_products[1].price -
                         self.test_basket.calculate_discount(), 2))

    def test_basket_discount_bundle_offer(self):
        # With bundle offer on all shampoo buy 3 get the cheapest free
        self.test_offer = BundleOffer([self.test_products[3],
                                       self.test_products[4],
                                       self.test_products[5]
                                      ], 3)
        self.test_basket = Basket(self.test_catalouge, [self.test_offer])
        # Add 2 small shampoo
        self.test_basket.add_product(self.test_products[3], 2)
        # Add 1 medium shampoo
        self.test_basket.add_product(self.test_products[4])
        # Add 3 large shampoo
        self.test_basket.add_product(self.test_products[5], 3)
        # One large shampoo for free (3.5) and One small shampoo for free (2.00)
        # Total: 5.5
        self.assertEqual(self.test_basket.calculate_discount(), 5.5)
        self.assertEqual(self.test_basket.calculate_total(),
                         round_half_up(self.test_products[3].price * 2 +
                         self.test_products[4].price +
                         self.test_products[5].price * 3 -
                         self.test_basket.calculate_discount(), 2))

    def test_basket_discount_multiple_bundle_offers(self):
        # With bundle offer on all shampoo buy 3 get the cheapest free
        self.bundle_offer_all_shampoo = BundleOffer([self.test_products[3],
                                       self.test_products[4],
                                       self.test_products[5]
                                      ], 3)
        # With bundle offer on small shampoo and sardines buy 2 get the cheapest free
        self.bundle_offer_small_shampoo_and_sardines = BundleOffer([self.test_products[3],
                                        self.test_products[2]
                                      ], 2)
        self.test_basket = Basket(self.test_catalouge, [
                                        self.bundle_offer_all_shampoo,
                                        self.bundle_offer_small_shampoo_and_sardines
                                    ])
        # Add 1 sardines
        self.test_basket.add_product(self.test_products[2], 1)
        # Add 3 small shampoo
        self.test_basket.add_product(self.test_products[3], 3)
        # Add 2 medium shampoo
        self.test_basket.add_product(self.test_products[4], 2)
        # Add 3 large shampoo
        self.test_basket.add_product(self.test_products[5], 3)
        # One large shampoo for free (3.5)
        # Two small shampoo for free (4.00)
        # Total: 7.5
        self.assertEqual(self.test_basket.calculate_discount(), 7.5)
        self.assertEqual(self.test_basket.calculate_total(),
                         round_half_up(self.test_products[2].price +
                         self.test_products[3].price * 3 +
                         self.test_products[4].price * 2 +
                         self.test_products[5].price * 3 -
                         self.test_basket.calculate_discount(), 2))

    def test_basket_discount_all_offers(self):
        # With bundle offer on all shampoo buy 3 get the cheapest free
        self.bundle_offer_all_shampoo = BundleOffer([self.test_products[3],
                                       self.test_products[4],
                                       self.test_products[5]
                                      ], 3)
        # With bundle offer on small shampoo and sardines buy 2 get the cheapest free
        self.bundle_offer_small_shampoo_and_sardines = BundleOffer([self.test_products[3],
                                        self.test_products[2]
                                      ], 2)

        self.buy_and_get_free_offer_baked_beans = BuyAndGetFreeOffer(self.test_products[0], 2, 1)
        self.percentage_offer_baked_beans = PercentageOffer(self.test_products[0], 0.25)
        self.test_basket = Basket(self.test_catalouge, [
                                        self.bundle_offer_all_shampoo,
                                        self.bundle_offer_small_shampoo_and_sardines,
                                        self.buy_and_get_free_offer_baked_beans,
                                        self.percentage_offer_baked_beans
                                    ])
        # Add 4 Baked Beans
        self.test_basket.add_product(self.test_products[0], 4)
        # Add 1 Biscuits
        self.test_basket.add_product(self.test_products[1])
        # Add 1 sardines
        self.test_basket.add_product(self.test_products[2], 1)
        # Add 3 small shampoo
        self.test_basket.add_product(self.test_products[3], 3)
        # Add 2 medium shampoo
        self.test_basket.add_product(self.test_products[4], 2)
        # Add 3 large shampoo
        self.test_basket.add_product(self.test_products[5], 3)
        # Baked Beans Buy 2 get one free: 0.99
        # Baked Beans 25% percent discount: 0.99 * 0.25 =  0.25
        # One large shampoo for free (3.5)
        # Two small shampoo for free (4.00)
        # Total: 7.5 + 0.99 + 0.25 = 8.74
        self.assertEqual(self.test_basket.calculate_discount(), 8.74)
        self.assertEqual(self.test_basket.calculate_total(),
                         round_half_up(self.test_products[0].price * 4 +
                         self.test_products[1].price +
                         self.test_products[2].price +
                         self.test_products[3].price * 3 +
                         self.test_products[4].price * 2 +
                         self.test_products[5].price * 3 -
                         self.test_basket.calculate_discount(), 2))
