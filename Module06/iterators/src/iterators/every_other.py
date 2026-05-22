class EveryOther:
    def __init__(self, iterable):
        self.other_iterator = iter(iterable)

    def __iter__(self):
        return self

    def __next__(self):
        next(self.other_iterator)
        return next(self.other_iterator)


if __name__ == "__main__":
    for i in EveryOther([1, 2, 3, 4, 5]):
        print(i)

# output:
# 2
# 4
# 6
