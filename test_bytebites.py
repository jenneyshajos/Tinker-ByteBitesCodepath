import unittest

from models import Customer, Item, Menu, Transaction


class TestItem(unittest.TestCase):
    def test_stores_all_attributes(self):
        item = Item("Spicy Burger", 10.0, "Food", 4.6)
        self.assertEqual(item.name, "Spicy Burger")
        self.assertEqual(item.price, 10.0)
        self.assertEqual(item.category, "Food")
        self.assertEqual(item.popularity_rating, 4.6)

    def test_attributes_are_read_only(self):
        item = Item("Large Soda", 5.0, "Drinks", 4.1)
        with self.assertRaises(AttributeError):
            item.price = 0.0


class TestCategoryFiltering(unittest.TestCase):
    def setUp(self):
        self.burger = Item("Spicy Burger", 10.0, "Food", 4.6)
        self.soda = Item("Large Soda", 5.0, "Drinks", 4.1)
        self.tea = Item("Iced Tea", 3.0, "Drinks", 3.9)
        self.brownie = Item("Brownie", 3.0, "Desserts", 4.8)
        self.menu = Menu()
        for item in (self.burger, self.soda, self.tea, self.brownie):
            self.menu.add_item(item)

    # Logic tests
    def test_filter_returns_only_matching_category(self):
        self.assertEqual(self.menu.filter_by_category("Desserts"), [self.brownie])

    def test_filter_returns_all_matches_in_menu_order(self):
        self.assertEqual(self.menu.filter_by_category("Drinks"), [self.soda, self.tea])

    # Edge cases
    def test_filter_with_no_matches_returns_empty_list(self):
        self.assertEqual(self.menu.filter_by_category("Breakfast"), [])

    def test_filter_on_empty_menu_returns_empty_list(self):
        self.assertEqual(Menu().filter_by_category("Drinks"), [])

    def test_filter_ignores_case(self):
        self.assertEqual(self.menu.filter_by_category("drinks"), [self.soda, self.tea])
        self.assertEqual(self.menu.filter_by_category("DESSERTS"), [self.brownie])

    def test_filter_does_not_remove_items_from_menu(self):
        self.menu.filter_by_category("Drinks")
        self.assertEqual(len(self.menu.get_all_items()), 4)


class TestSorting(unittest.TestCase):
    def setUp(self):
        self.burger = Item("Spicy Burger", 10.0, "Food", 4.6)
        self.soda = Item("Large Soda", 5.0, "Drinks", 4.1)
        self.brownie = Item("Brownie", 3.0, "Desserts", 4.8)
        self.menu = Menu()
        for item in (self.burger, self.soda, self.brownie):
            self.menu.add_item(item)

    # Logic tests
    def test_sort_by_price_cheapest_first(self):
        self.assertEqual(self.menu.sort_by_price(), [self.brownie, self.soda, self.burger])

    def test_sort_by_price_most_expensive_first(self):
        self.assertEqual(self.menu.sort_by_price(descending=True), [self.burger, self.soda, self.brownie])

    def test_sort_by_popularity_highest_first(self):
        self.assertEqual(self.menu.sort_by_popularity(), [self.brownie, self.burger, self.soda])

    def test_sort_by_popularity_lowest_first(self):
        self.assertEqual(self.menu.sort_by_popularity(descending=False), [self.soda, self.burger, self.brownie])

    # Edge cases
    def test_sort_empty_menu_returns_empty_list(self):
        self.assertEqual(Menu().sort_by_price(), [])
        self.assertEqual(Menu().sort_by_popularity(), [])

    def test_sort_single_item_menu(self):
        menu = Menu()
        menu.add_item(self.soda)
        self.assertEqual(menu.sort_by_price(), [self.soda])

    def test_sort_ties_keep_original_order(self):
        tea = Item("Iced Tea", 3.0, "Drinks", 4.8)
        self.menu.add_item(tea)
        self.assertEqual(self.menu.sort_by_price()[:2], [self.brownie, tea])
        self.assertEqual(self.menu.sort_by_popularity()[:2], [self.brownie, tea])

    def test_sort_does_not_reorder_menu(self):
        self.menu.sort_by_price()
        self.menu.sort_by_popularity()
        self.assertEqual(self.menu.get_all_items(), [self.burger, self.soda, self.brownie])


class TestTotalCalculation(unittest.TestCase):
    def setUp(self):
        self.burger = Item("Spicy Burger", 10.0, "Food", 4.6)
        self.soda = Item("Large Soda", 5.0, "Drinks", 4.1)

    # Logic tests
    def test_calculate_total_with_multiple_items(self):
        self.assertAlmostEqual(Transaction([self.burger, self.soda]).compute_total(), 15.0)

    def test_calculate_total_with_single_item(self):
        self.assertAlmostEqual(Transaction([self.burger]).compute_total(), 10.0)

    def test_total_updates_after_add_item(self):
        transaction = Transaction([self.burger])
        transaction.add_item(self.soda)
        self.assertAlmostEqual(transaction.compute_total(), 15.0)

    def test_same_item_twice_is_charged_twice(self):
        self.assertAlmostEqual(Transaction([self.soda, self.soda]).compute_total(), 10.0)

    # Edge cases
    def test_empty_order_is_rejected(self):
        # The design requires at least one item per transaction (1..*),
        # so an empty order raises an error instead of totaling $0.
        with self.assertRaises(ValueError):
            Transaction([])

    def test_total_is_zero_when_all_items_are_free(self):
        water = Item("Cup of Water", 0.0, "Drinks", 3.0)
        self.assertEqual(Transaction([water]).compute_total(), 0.0)

    def test_total_handles_decimal_prices(self):
        a = Item("Cookie", 0.1, "Desserts", 4.0)
        b = Item("Mint", 0.2, "Desserts", 3.5)
        self.assertAlmostEqual(Transaction([a, b]).compute_total(), 0.3)

    def test_changing_original_list_does_not_change_total(self):
        items = [self.burger]
        transaction = Transaction(items)
        items.append(self.soda)
        self.assertAlmostEqual(transaction.compute_total(), 10.0)


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.soda = Item("Large Soda", 5.0, "Drinks", 4.1)

    # Logic tests
    def test_customer_with_purchase_is_real_user(self):
        customer = Customer("Alex")
        customer.add_transaction(Transaction([self.soda]))
        self.assertTrue(customer.is_real_user())

    def test_customer_with_many_purchases_is_real_user(self):
        customer = Customer("Alex")
        customer.add_transaction(Transaction([self.soda]))
        customer.add_transaction(Transaction([self.soda, self.soda]))
        self.assertTrue(customer.is_real_user())

    # Edge cases
    def test_new_customer_is_not_real_user(self):
        self.assertFalse(Customer("Alex").is_real_user())


if __name__ == "__main__":
    unittest.main()
