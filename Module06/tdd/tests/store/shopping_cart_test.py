from dataclasses import dataclass

import pytest

from store.shopping_cart import ShoppingCart


@pytest.fixture
def cart():
    return ShoppingCart()


@dataclass(frozen=True)
class StockItemFake:
    name: str
    unit_price: int


class TestShoppingCart:
    def test_given_new_then_empty(self, cart):
        "SPEC: a cart is empty when it is first created"
        assert cart.total_item_count == 0

    def test_given_new_then_item_occurrences_zero(self, cart):
        "SPEC: a cart is empty when it is first created"
        assert cart.get_count(None) == 0

    def test_given_new_when_item_added_then_total_count_increases(self, cart):
        "SPEC: adding a stock item correspondingly increases the number of occurrences of [that stock item in the cart] and the total number of items in the cart."
        expected_item_count = 100
        cart.add_item(None, expected_item_count)
        assert cart.total_item_count == expected_item_count

    def test_given_new_when_item_added_then_item_count_increases(self, cart):
        "SPEC: adding a stock item correspondingly increases the number of occurrences of that stock item in the cart [and the total number of items in the cart]."
        item = None
        expected_item_count = 100
        cart.add_item(item, expected_item_count)
        assert cart.get_count(item) == expected_item_count

        additional_quantity = 50
        cart.add_item(item, additional_quantity)
        assert cart.get_count(item) == expected_item_count + additional_quantity

    def test_given_new_when_item_added_then_other_item_zero(self, cart):
        "SPEC: adding a stock item does not impact the number of occurrences of other stock items in the cart."
        item_1 = "item_1"
        item_2 = "item_2"
        expected_item_1_count = 100
        cart.add_item(item_1, expected_item_1_count)
        assert cart.get_count(item_2) == 0

        cart.add_item(item_2, 30)
        assert cart.get_count(item_1) == expected_item_1_count

    def test_given_cart_with_item_when_negative_count_added_then_value_error_and_quantity_unchanged(
        self, cart
    ):
        item_1 = "item_1"
        expected_item_count = 100
        cart.add_item(item_1, expected_item_count)
        with pytest.raises(ValueError):
            cart.add_item(item_1, -50)
        assert (
            cart.get_count(item_1) == expected_item_count
            and cart.total_item_count == expected_item_count
        )

    def test_given_cart_with_item_when_remove_decreases_item_count_and_total_count(
        self, cart
    ):
        item = "item"
        starting_item_count = 100
        cart.add_item(item, starting_item_count)

        quantity_removed = 30
        cart.remove_item(item, quantity_removed)

        assert cart.get_count(item) == starting_item_count - quantity_removed

    def test_given_cart_when_negative_quantity_removed_then_value_error_and_quantity_unchanged(
        self, cart
    ):
        item = "item"
        starting_item_count = 100
        cart.add_item(item, starting_item_count)

        with pytest.raises(ValueError):
            cart.remove_item(item, -10)

        assert cart.get_count(item) == starting_item_count

    def test_given_cart_when_more_than_existing_removed_then_value_error(self, cart):
        item = "item"
        starting_item_count = 100
        cart.add_item(item, starting_item_count)

        with pytest.raises(ValueError):
            cart.remove_item(item, starting_item_count + 1)

    def test_given_cart_with_items_then_total_price_computed(self, cart):
        item_1_count = 10
        item_1_unit_price = 5
        item_1 = StockItemFake("item_1", item_1_unit_price)
        item_2_count = 30
        item_2_unit_price = 2
        item_2 = StockItemFake("item_2", item_2_unit_price)
        cart.add_item(item_1, item_1_count)
        cart.add_item(item_2, item_2_count)

        assert (
            cart.total_price
            == item_1_count * item_1_unit_price + item_2_count * item_2_unit_price
        )

    def test_given_cart_with_items_then_item_counts_reflects_items(self, cart):
        """SPEC: get the list of "item counts", that is, a list containing dictionaries with the following keys,values:
             item -- the StockItem
             count -- the number of occurrences of a StockItem in the cart, must be > 0
             line_price -- the price of count occurrences of this item
        where no two elements of the list have the same StockItem.  This list should be complete and reflect all occurrences of all StockItems added to the cart, even if they were added separately."""
        item_1_count = 10
        item_1_unit_price = 5
        item_1 = StockItemFake("item_1", item_1_unit_price)
        item_2_count = 30
        item_2_unit_price = 2
        item_2 = StockItemFake("item_2", item_2_unit_price)
        cart.add_item(item_1, item_1_count)
        cart.add_item(item_2, item_2_count)

        result = cart.item_counts

        assert len(result) == 2
        item_1_entry = result[0] if result[0]["item"] == item_1 else result[1]
        item_2_entry = result[0] if result[0]["item"] == item_2 else result[1]
        assert item_1_entry["item"] == item_1
        assert item_1_entry["count"] == item_1_count
        assert item_1_entry["line_price"] == item_1_count * item_1_unit_price
        assert item_2_entry["item"] == item_2
        assert item_2_entry["count"] == item_2_count
        assert item_2_entry["line_price"] == item_2_count * item_2_unit_price
