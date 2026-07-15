class ShoppingCart:
    def __init__(self):
        self._item_counts = {}

    @property
    def total_item_count(self):
        return sum([value for value in self._item_counts.values()])

    def get_count(self, item):
        return self._item_counts.get(item, 0)

    def add_item(self, item, count):
        if count < 0:
            raise ValueError("count must be non-negative")
        current = self._item_counts.get(item, 0)
        self._item_counts[item] = current + count

    def remove_item(self, item, count):
        if count < 0:
            raise ValueError("count must be non-negative")
        current = self.get_count(item)
        if count > current:
            raise ValueError("count must be less than or equal to the current quantity")
        self._item_counts[item] = current - count

    @property
    def total_price(self):
        sum = 0
        for item, quantity in self._item_counts.items():
            sum += item.unit_price * quantity
        return sum

    @property
    def item_counts(self):
        return [
            {"item": item, "count": count, "line_price": item.unit_price * count}
            for item, count in self._item_counts.items()
        ]
