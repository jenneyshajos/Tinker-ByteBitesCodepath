"""

Customer stores a name and a purchase history of Transactions, and
is_real_user() returns True once the customer has made at least one purchase.
Item represents a single food product, with a name, price, category and
popularity rating. Menu holds the full collection of Items and lets you add
items, browse all of them, or filter them by category. Transaction groups one
or more selected Items into a single purchase and computes the total cost.
A Customer makes transactions, while Menu and Transaction each hold Items,
which exist independently of both.
"""

class Item:
    """A single food product sold on ByteBites."""

    def __init__(self, name: str, price: float, category: str, popularity_rating: float):
        self._name = name
        self._price = price
        self._category = category
        self._popularity_rating = popularity_rating

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def category(self) -> str:
        return self._category

    @property
    def popularity_rating(self) -> float:
        return self._popularity_rating


class Menu:
    """The full collection of Items available to browse."""

    def __init__(self):
        self._items: list[Item] = []

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def get_all_items(self) -> list[Item]:
        return list(self._items)

    def filter_by_category(self, category: str) -> list[Item]:
        return [item for item in self._items if item.category == category]


class Transaction:
    """A single purchase grouping one or more selected Items."""

    def __init__(self, items: list[Item]):
        if not items:
            raise ValueError("A transaction must contain at least one item.")
        self._items: list[Item] = list(items)

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def compute_total(self) -> float:
        return sum(item.price for item in self._items)


class Customer:
    """A ByteBites user with a name and a purchase history."""

    def __init__(self, name: str):
        self._name = name
        self._purchase_history: list[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        self._purchase_history.append(transaction)

    def is_real_user(self) -> bool:
        return len(self._purchase_history) > 0
