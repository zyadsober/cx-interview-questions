from abc import ABC
from product import Product
from type_validators import validate_type, validate_list_type_and_children_types
from collections import OrderedDict
from utilities import round_half_up


class Offer(ABC):
    """
    Abstract class that defines the base class of all offers
    """
    def get_discount(self, basket_products):
        """
        Given a set of BaksetProducts, get the next best discount
        ---
        Params:
            basket_products: dict, the basket_products to calculate the next best discount from
        ---
        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

class BuyAndGetFreeOffer(Offer):
    """
    The class for the offer of buying a certain defined amount of items to qualify
    getting some more for free
    """
    def __init__(self, product, buy_quantity, free_quantity):
        """
        Constructor of the BuyAndGetFreeOffer
        ---
        Params:
            product: Product, the product that this offer applies to
            buy_quantity: int, the number of items that need to be bought
            free_quantity: int, the number of items that become free from the offer
        """
        validate_type(product, Product)

        self.product = product.name
        self.buy_quantity = buy_quantity
        self.free_quantity = free_quantity

    def get_discount(self, basket_products):
        """
        Given a dict of BaksetProducts, get the next best discount
        ---
        Params:
            basket_products: dict, the basket_products to calculate the next best discount from
        ---
        Returns:
            float, the next best discount
            dict, dict of product names(key) and their quantity(value) used in the discount
        """
        discount = 0
        if (self.product in basket_products and
            basket_products[self.product].quantity >= self.buy_quantity + self.free_quantity):
            discount = basket_products[self.product].product.price * self.free_quantity
            return round_half_up(discount, 2), {self.product: self.buy_quantity + self.free_quantity}
        return discount, {}


class PercentageOffer(Offer):
    """
    The class for the offer of buying a certain defined amount of items to qualify
    getting some more for free
    """
    def __init__(self, product, discount_percent):
        """
        Constructor of the BuyAndGetFreeOffer
        ---
        Params:
            product: Product, the product that this offer applies to
            discount_percent: float, the discount percentage applied to the product on offer
        """
        validate_type(product, Product)

        self.product = product.name
        self.discount_percent = discount_percent

    def get_discount(self, basket_products):
        """
        Given a dict of BaksetProducts, get the next best discount
        ---
        Params:
            basket_products: dict, the basket_products to calculate the next best discount from
        ---
        Returns:
            float, the next best discount
            dict, dict of product names(key) and their quantity(value) used in the discount
        """
        discount = 0
        if (self.product in basket_products and
            basket_products[self.product].quantity >= 1):
            discount = basket_products[self.product].product.price * self.discount_percent
            return round_half_up(discount, 2), {self.product: 1}
        return discount, {}


class BundleOffer(Offer):
    """
    The class for the offer of buying a group of items and getting the cheapest item for free
    """
    def __init__(self, bundle_items, required_items):
        """
        Constructor of the BuyAndGetFreeOffer
        ---
        Params:
            discount_percent: list, the list of products included in the bundle offer
            required_items: int, the required number of items required from the bundle items
        """
        validate_list_type_and_children_types(bundle_items, Product)

        self.bundle_items = [product.name for product in bundle_items]
        self.required_items = required_items

    def get_discount(self, basket_products):
        """
        Given a dict of BaksetProducts, get the next best discount
        ---
        Params:
            basket_products: dict, the basket_products to calculate the next best discount from
        ---
        Returns:
            float, the next best discount
            dict, dict of product names(key) and their quantity(value) used in the discount
        """
        discount = 0
        qualifying_item_count = 0
        qualified_items = dict()
        for product in basket_products:
            if product in self.bundle_items:
                qualifying_item_count += basket_products[product].quantity
                qualified_items[product] = basket_products[product]
        if qualifying_item_count >= self.required_items:
            sorted_basket_products = OrderedDict(sorted(qualified_items.items(), key=lambda kv: kv[1].product.price, reverse=True))
            remaining_items_count = self.required_items
            items_used = dict()
            for product in sorted_basket_products:
                current_product = sorted_basket_products[product]
                if remaining_items_count - current_product.quantity <= 0:
                    discount = current_product.product.price
                    items_used[current_product.product.name] = remaining_items_count
                    remaining_items_count = 0
                else:
                    items_used[current_product.product.name] = current_product.quantity
                    remaining_items_count -= current_product.quantity
                if remaining_items_count <= 0:
                    break
            return discount, items_used
        return discount, {}
